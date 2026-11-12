# 鑫喜文創 Gold Joy — 舊站完整備份

來源：https://goldjoy.com.tw/ （備份日期：2026-11-12）

這是舊網站的「靜態備份」：每一頁都已經是做好的 HTML 檔，不需要資料庫或後台程式，
放到任何靜態網站主機上，網址和外觀都會跟舊站一樣。

## 資料夾說明

| 路徑 | 內容 |
|---|---|
| `docs/` | 整個網站，直接把這個資料夾上傳到主機即可 |
| `docs/index.html` | 首頁 |
| `docs/about/index.html` | 對應舊網址 `/about`（其他頁面同理，共 87 頁，含部落格分類頁） |
| `docs/uploads/` | 後台上傳的圖片 |
| `docs/assets/` | 版型用的 CSS、JS、字型、圖示 |
| `docs/sitemap.xml`、`docs/robots.txt` | 搜尋引擎用的網站地圖與規則（照舊站保留） |
| `tools/mirror.py` | 備份程式，舊站有更新時可重跑：`python3 tools/mirror.py` |
| `tools/relativize.py` | 把站內路徑改成相對路徑，讓網站放在子資料夾（如 GitHub Pages）也能運作。重跑 mirror.py 之後一定要接著跑 |
| `tools/mirror-report.txt` | 下載不到的檔案清單（都是舊站本身就不存在的檔案，外觀不受影響） |

## GitHub Pages 網址

**https://zealchou.github.io/GoldJoy/**

發布方式：GitHub Pages 讀的是 `gh-pages` 分支，這個分支裡只放 `docs/` 資料夾的內容。
`docs/` 有更新時，用下面的指令同步到 `gh-pages`，1～2 分鐘後網站就會更新：

```bash
git subtree split --prefix docs -b gh-pages-new
git push -f origin gh-pages-new:gh-pages
git branch -D gh-pages-new
```

（`docs/.nojekyll` 這個空檔案是告訴 GitHub 不要用 Jekyll 加工網頁，原封不動發布。）

## 更新備份的步驟

```bash
python3 tools/mirror.py      # 從舊站重新下載
python3 tools/relativize.py  # 轉成相對路徑
```

## 在自己電腦預覽

```bash
cd docs
python3 -m http.server 8000
```

然後用瀏覽器開 http://localhost:8000 。
（建議透過伺服器開；直接雙擊 index.html 時，點連結會打開資料夾而不是頁面。）

## 注意事項

- 仍然連到外部的資源（舊站原本就是這樣）：Bootstrap、jQuery、Font Awesome（CDN）、Google Fonts、
  Google 地圖、LINE、Facebook、Instagram 連結。
- 舊站本身有個小 bug：部落格分類頁上的分類標籤會連到 `/xxx/category/A/category/B` 這種重複的網址，
  舊站伺服器照樣顯示頁面。為了點起來跟舊站一樣，這些頁面也一併保留。
- 舊站沒有表單，所以搬成靜態站不會有功能遺失。
- 頁面裡的 og:image（分享到 FB/LINE 時的縮圖）仍寫 `https://goldjoy.com.tw/...`，
  網域搬過去後就會自動對上。
