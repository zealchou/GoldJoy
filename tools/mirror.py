#!/usr/bin/env python3
"""
鑫喜文創舊站整站備份程式（goldjoy.com.tw）

做的事：
1. 從 sitemap.xml 與每頁裡的站內連結，找出所有頁面並下載
2. 下載每頁用到的圖片、CSS、JS、字型（包含 CSS 裡再引用的檔案）
3. 外部 CDN 的 CSS/JS（Bootstrap、Font Awesome 等）也抓回本地 /vendor/，
   讓新家不依賴別人的伺服器（Google Fonts 例外，保留原連結）
4. 把頁面存成「乾淨網址」結構：/about -> about/index.html，
   放到任何靜態主機（Netlify、GitHub Pages、Nginx…）網址都跟舊站一樣

用法：python3 tools/mirror.py
"""
import html
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from collections import deque

SITE = "https://goldjoy.com.tw"
HOSTS = {"goldjoy.com.tw", "www.goldjoy.com.tw"}
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "site")
OUT = os.path.abspath(OUT)
# 想把外部 CDN 的 CSS/JS 也抓回本地時，把網域加進這裡（會存到 /vendor/）。
# 目前留空：Bootstrap、jQuery、Font Awesome、Google Fonts 維持舊站原本的 CDN 連結。
VENDOR_HOSTS = set()
UA = "Mozilla/5.0 (site-migration-backup)"
ASSET_EXT = re.compile(
    r"\.(png|jpe?g|gif|svg|webp|ico|bmp|avif|css|js|json|map|woff2?|ttf|eot|otf|mp4|webm|mp3|pdf)$",
    re.I,
)

pages_done = set()
assets_done = {}  # url -> local path or None
failed = []


def encode_url(url):
    """把網址裡的中文、空白轉成 %XX（percent-encoding），伺服器才看得懂"""
    p = urllib.parse.urlsplit(url)
    path = urllib.parse.quote(urllib.parse.unquote(p.path), safe="/-_.~()!$&'*+,;=:@")
    return urllib.parse.urlunsplit(p._replace(path=path))


def fetch(url):
    req = urllib.request.Request(encode_url(url), headers={"User-Agent": UA})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read(), r.headers.get("Content-Type", "")
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None, str(e.code)
            err = str(e)
        except Exception as e:  # noqa
            err = str(e)
        time.sleep(1 + attempt * 2)
    return None, err


def norm(url, base):
    """把網址轉成絕對網址，並把 HTML 實體（&#x...;）解碼"""
    url = html.unescape(url.strip())
    if not url or url.startswith(("data:", "javascript:", "mailto:", "tel:", "#", "about:")):
        return None
    if url.startswith("//"):
        url = "https:" + url
    return urllib.parse.urljoin(base, url)


def is_site(u):
    return urllib.parse.urlsplit(u).hostname in HOSTS


def is_vendor(u):
    return urllib.parse.urlsplit(u).hostname in VENDOR_HOSTS


def local_asset_path(u):
    """網址 -> 本地相對路徑（去掉 ?v= 這類快取參數）"""
    p = urllib.parse.urlsplit(u)
    path = urllib.parse.unquote(p.path)
    if is_site(u):
        rel = path.lstrip("/")
    else:
        rel = "vendor/" + p.hostname + path
    if rel.endswith("/") or not rel:
        rel += "index"
    return rel


def public_url(rel):
    """本地路徑 -> 網頁中要寫的網址（中文、空白會被 % 編碼）"""
    return "/" + urllib.parse.quote(rel, safe="/-_.~()")


def local_page_path(u):
    p = urllib.parse.urlsplit(u)
    path = urllib.parse.unquote(p.path).strip("/")
    return os.path.join(path, "index.html") if path else "index.html"


def save(rel, data):
    full = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "wb") as f:
        f.write(data)


CSS_URL = re.compile(r"""url\(\s*(['"]?)([^'")]+)\1\s*\)""")
CSS_IMPORT = re.compile(r"""@import\s+(['"])([^'"]+)\1""")


def get_asset(u):
    """下載資源，回傳它在新站的網址（失敗則回傳 None）"""
    key = u.split("#")[0]
    if key in assets_done:
        return assets_done[key]
    if not (is_site(key) or is_vendor(key)):
        return None
    rel = local_asset_path(key)
    assets_done[key] = public_url(rel)  # 先佔位，避免循環引用
    full = os.path.join(OUT, rel)
    if os.path.exists(full) and not rel.endswith(".css") and os.path.getsize(full) > 0:
        return assets_done[key]  # 之前已下載過，略過（加快重跑速度）
    data, ctype = fetch(key)
    if data is None:
        failed.append((key, ctype))
        assets_done[key] = None
        return None
    if rel.endswith(".css") or "text/css" in ctype:
        data = process_css(data.decode("utf-8", "replace"), key).encode("utf-8")
    save(rel, data)
    return assets_done[key]


def process_css(css, base):
    def rep(m):
        q, raw = m.group(1), m.group(2)
        u = norm(raw, base)
        if not u:
            return m.group(0)
        new = get_asset(u)
        return f"url({q}{new}{q})" if new else m.group(0)

    def rep_imp(m):
        u = norm(m.group(2), base)
        new = get_asset(u) if u else None
        return f'@import "{new}"' if new else m.group(0)

    css = CSS_IMPORT.sub(rep_imp, css)
    return CSS_URL.sub(rep, css)


# HTML 屬性：抓出 屬性="值"
ATTR = re.compile(r"""(\s)([a-zA-Z_:][-a-zA-Z0-9_:.]*)\s*=\s*("([^"]*)"|'([^']*)')""")
ASSET_ATTRS = {"src", "data-src", "data-image", "data-imagemobile", "data-bg", "poster",
               "data-background", "data-original", "data-lazy"}
STYLE_BLOCK = re.compile(r"(<style[^>]*>)(.*?)(</style>)", re.S | re.I)


def process_html(text, page_url, page_queue):
    def handle_value(name, raw):
        lname = name.lower()
        val = html.unescape(raw)
        if lname == "style":
            return process_css(val, page_url)
        if lname in ("srcset", "data-srcset"):
            parts = []
            for item in val.split(","):
                bits = item.strip().split()
                if not bits:
                    continue
                u = norm(bits[0], page_url)
                new = get_asset(u) if u else None
                parts.append(" ".join([new or bits[0]] + bits[1:]))
            return ", ".join(parts)
        if lname == "href":
            u = norm(val, page_url)
            if not u:
                return None
            path = urllib.parse.urlsplit(u).path
            if (is_site(u) and ASSET_EXT.search(path)) or (
                is_vendor(u) and ASSET_EXT.search(path)
            ):
                return get_asset(u)
            if is_site(u):
                clean = urllib.parse.urlunsplit(urllib.parse.urlsplit(u)._replace(fragment=""))
                page_queue.append(clean)
                sp = urllib.parse.urlsplit(u)
                rel = sp.path or "/"
                if sp.query:
                    rel += "?" + sp.query
                if sp.fragment:
                    rel += "#" + sp.fragment
                return rel  # 站內連結統一寫成 /path（不帶網域）
            return None
        if lname in ASSET_ATTRS or (lname == "content" and "/uploads/" in val):
            u = norm(val, page_url)
            if not u:
                return None
            if lname == "content":  # og:image 等需保留完整網址
                new = get_asset(u)
                return (SITE + new) if new else None
            path = urllib.parse.urlsplit(u).path
            if is_site(u) or (is_vendor(u) and ASSET_EXT.search(path)):
                return get_asset(u)
        return None

    def rep_attr(m):
        lead, name, _, dq, sq = m.groups()
        raw = dq if dq is not None else sq
        new = handle_value(name, raw)
        if new is None:
            return m.group(0)
        q = '"' if dq is not None else "'"
        esc = new.replace("&", "&amp;").replace(q, "&quot;" if q == '"' else "&#39;")
        return f"{lead}{name}={q}{esc}{q}"

    text = STYLE_BLOCK.sub(
        lambda m: m.group(1) + process_css(m.group(2), page_url) + m.group(3), text
    )
    # 只處理標籤內部的屬性，避免改到內文
    text = re.sub(r"<[a-zA-Z][^<>]*>", lambda m: ATTR.sub(rep_attr, m.group(0)), text)
    return text


def main():
    os.makedirs(OUT, exist_ok=True)
    queue = deque([SITE + "/"])
    sm, _ = fetch(SITE + "/sitemap.xml")
    if sm:
        save("sitemap.xml", sm)
        for loc in re.findall(r"<loc>([^<]+)</loc>", sm.decode("utf-8", "replace")):
            queue.append(html.unescape(loc.strip()))
    rb, _ = fetch(SITE + "/robots.txt")
    if rb:
        save("robots.txt", rb)

    while queue:
        u = queue.popleft()
        sp = urllib.parse.urlsplit(u)
        key = (sp.path.rstrip("/") or "/") + ("?" + sp.query if sp.query else "")
        if key in pages_done:
            continue
        pages_done.add(key)
        if sp.query:
            # 靜態主機無法依「?參數」回傳不同頁面，記錄下來不下載
            failed.append((u, "skipped: query-string page"))
            continue
        data, ctype = fetch(SITE + (sp.path or "/"))
        if data is None:
            failed.append((u, ctype))
            continue
        if "text/html" not in ctype:
            get_asset(u)
            continue
        text = data.decode("utf-8", "replace")
        new_q = []
        text = process_html(text, SITE + (sp.path or "/"), new_q)
        queue.extend(new_q)
        save(local_page_path(u), text.encode("utf-8"))
        print(f"[page] {key}", flush=True)
        time.sleep(0.2)

    print(f"\n頁面：{len(pages_done)}  資源：{len(assets_done)}  失敗/略過：{len(failed)}")
    with open(os.path.join(OUT, "..", "tools", "mirror-report.txt"), "w") as f:
        f.write("# 下載失敗或略過的網址\n")
        for u, why in failed:
            f.write(f"{why}\t{u}\n")


if __name__ == "__main__":
    sys.exit(main())
