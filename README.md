# 鑫喜文創 Gold Joy — 舊站完整備份

來源：https://goldjoy.com.tw/ （備份日期：2026-11-12）

這是舊網站的「靜態備份」：每一頁都已經是做好的 HTML 檔，不需要資料庫或後台程式，
放到任何靜態網站主機上，網址和外觀都會跟舊站一樣。

## 資料夾說明

| 路徑 | 內容 |
|---|---|
| `site/` | 整個網站，直接把這個資料夾上傳到主機即可 |
| `site/index.html` | 首頁 |
| `site/about/index.html` | 對應舊網址 `/about`（其他頁面同理，共 47 頁） |
| `site/uploads/` | 後台上傳的圖片 |
| `site/assets/` | 版型用的 CSS、JS、字型、圖示 |
| `site/sitemap.xml`、`site/robots.txt` | 搜尋引擎用的網站地圖與規則（照舊站保留） |
| `tools/mirror.py` | 備份程式，舊站有更新時可重跑：`python3 tools/mirror.py` |
| `tools/mirror-report.txt` | 下載不到的檔案清單（都是舊站本身就不存在的檔案，外觀不受影響） |

## 在自己電腦預覽

```bash
cd site
python3 -m http.server 8000
```

然後用瀏覽器開 http://localhost:8000 。
（直接雙擊 index.html 會跑版，因為網頁裡的連結是用 `/` 開頭的「根目錄路徑」，需要透過伺服器開。）

## 注意事項

- 仍然連到外部的資源（舊站原本就是這樣）：Bootstrap、jQuery、Font Awesome（CDN）、Google Fonts、
  Google 地圖、LINE、Facebook、Instagram 連結。
- 舊站沒有表單，所以搬成靜態站不會有功能遺失。
- 頁面裡的 og:image（分享到 FB/LINE 時的縮圖）仍寫 `https://goldjoy.com.tw/...`，
  網域搬過去後就會自動對上。
