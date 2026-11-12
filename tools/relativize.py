#!/usr/bin/env python3
"""
把 docs/ 裡所有「/ 開頭的站內路徑」改成「相對路徑」。

為什麼：GitHub Pages 的網址是 https://<帳號>.github.io/<repo名>/，多了一層子資料夾，
/about 這種根目錄路徑會指到錯的地方。改成相對路徑（例如 ../about/）後，
網站放在網域根目錄或任何子資料夾都能正常運作。

用法：python3 tools/relativize.py   （重跑 mirror.py 之後要再跑一次）
"""
import html
import os
import posixpath
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "docs"))
URL_ATTRS = {"href", "src", "data-src", "data-image", "data-imagemobile", "data-bg", "poster",
             "data-background", "data-original", "data-lazy", "action", "data-href"}


def all_paths():
    out = set()
    for d, _, fs in os.walk(ROOT):
        for f in fs:
            out.add(os.path.relpath(os.path.join(d, f), ROOT).replace(os.sep, "/"))
    return out


FILES = all_paths()


def rel(target, from_dir):
    """target 是像 /about?x#y 的根目錄路徑；from_dir 是目前檔案所在的資料夾（相對 docs/）"""
    from urllib.parse import unquote
    path = re.match(r"[^?#]*", target).group(0)
    rest = target[len(path):]
    clean = path.strip("/")
    # 存在的檔案、或最後一段有副檔名（如 .png）就當作檔案，否則當作頁面
    is_file = bool(clean) and (unquote(clean) in FILES or re.search(r"\.[A-Za-z0-9]{2,5}$", clean) is not None)
    r = posixpath.relpath("/" + clean, "/" + from_dir)
    if not is_file:  # 頁面：指向資料夾（裡面的 index.html）
        r = "./" if r == "." else r + "/"
    return r + rest


def fix_url(val, from_dir):
    if val.startswith("/") and not val.startswith("//"):
        return rel(val, from_dir)
    return None


CSS_URL = re.compile(r"""url\(\s*(['"]?)([^'")]+)\1\s*\)""")


def fix_css(css, from_dir):
    def rep(m):
        new = fix_url(html.unescape(m.group(2)).strip(), from_dir)
        return f"url({m.group(1)}{new}{m.group(1)})" if new else m.group(0)
    return CSS_URL.sub(rep, css)


# 屬性="值"、屬性='值'、屬性=值（沒加引號）三種寫法都處理
ATTR = re.compile(r"""(\s)([a-zA-Z_:][-a-zA-Z0-9_:.]*)\s*=\s*("([^"]*)"|'([^']*)'|([^\s"'=<>`]+))""")


def fix_html(text, from_dir):
    def rep_attr(m):
        lead, name, _, dq, sq, uq = m.groups()
        raw = dq if dq is not None else (sq if sq is not None else uq)
        lname = name.lower()
        val = html.unescape(raw)
        new = None
        if lname in URL_ATTRS:
            new = fix_url(val, from_dir)
        elif lname in ("srcset", "data-srcset"):
            parts, changed = [], False
            for item in val.split(","):
                bits = item.strip().split()
                if not bits:
                    continue
                n = fix_url(bits[0], from_dir)
                changed |= bool(n)
                parts.append(" ".join([n or bits[0]] + bits[1:]))
            new = ", ".join(parts) if changed else None
        elif lname.startswith("on"):  # onclick="location.href='/xxx'" 這類 JS 跳頁
            n = re.sub(r"""(location(?:\.href)?\s*=\s*)(['"])(/(?!/)[^'"]*)\2""",
                       lambda k: k.group(1) + k.group(2) + rel(k.group(3), from_dir) + k.group(2), val)
            new = n if n != val else None
        elif lname == "style":
            n = fix_css(val, from_dir)
            new = n if n != val else None
        if new is None:
            return m.group(0)
        q = "'" if sq is not None else '"'
        esc = new.replace("&", "&amp;").replace(q, "&quot;" if q == '"' else "&#39;")
        return f"{lead}{name}={q}{esc}{q}"

    # <script> 裡的字串路徑："/uploads/..."、"/psychology-blog/category/" + x、"/" + permalink
    top = {f.split("/")[0] for f in FILES}

    def fix_js_str(k):
        q, v = k.group(1), k.group(2)
        after = text_js[k.end():k.end() + 5].lstrip()
        if v == "/":
            if not after.startswith("+"):
                return k.group(0)
        else:
            from urllib.parse import unquote
            if unquote(v.lstrip("/").split("/")[0].split("?")[0]) not in top:
                return k.group(0)
        return q + rel(v, from_dir) + q

    def fix_script(m):
        nonlocal text_js
        text_js = m.group(2)
        body = re.sub(r"""(["'])(/(?!/)[^"'\n]*)\1""", fix_js_str, text_js)
        return m.group(1) + body + m.group(3)

    text_js = ""
    text = re.sub(r"(<script(?![^>]*\bsrc=)[^>]*>)(.*?)(</script>)", fix_script, text, flags=re.S | re.I)

    text = re.sub(r"(<style[^>]*>)(.*?)(</style>)",
                  lambda m: m.group(1) + fix_css(m.group(2), from_dir) + m.group(3), text,
                  flags=re.S | re.I)
    return re.sub(r"<[a-zA-Z][^<>]*>", lambda m: ATTR.sub(rep_attr, m.group(0)), text)


def main():
    n = 0
    for p in sorted(FILES):
        from_dir = posixpath.dirname(p)
        full = os.path.join(ROOT, p)
        if p.endswith(".html"):
            fn = fix_html
        elif p.endswith(".css"):
            fn = fix_css
        else:
            continue
        s = open(full, encoding="utf-8").read()
        t = fn(s, from_dir)
        if t != s:
            open(full, "w", encoding="utf-8").write(t)
            n += 1
    print(f"已改寫 {n} 個檔案")


if __name__ == "__main__":
    main()
