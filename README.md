# 📰 LINE 每日新聞報告機器人（Gemini 免費版）

每天早上 8 點（台灣時間）自動搜尋指定主題的新聞，
由 Google Gemini AI 整理成摘要報告，並透過 LINE 傳送給你。
**完全免費！**

---

## 專案結構

```
line-news-bot/
├── .github/
│   └── workflows/
│       └── news_report.yml   # GitHub Actions 排程設定
├── scripts/
│   └── news_report.py        # 主要執行腳本
├── requirements.txt           # Python 套件清單
└── README.md
```

---

## 設定步驟

### 1. 取得 Gemini API Key（免費）

1. 前往 https://aistudio.google.com/app/apikey
2. 登入 Google 帳號
3. 點「**Create API Key**」
4. 複製產生的 API Key

> 免費額度：每天 1500 次請求，每分鐘 15 次，完全夠用！

### 2. 取得 LINE Messaging API 憑證

1. 前往 https://developers.line.biz/
2. 登入 LINE 帳號，建立 Provider
3. 建立 **Messaging API Channel**
4. 取得：
   - **Channel Access Token**（Messaging API 分頁 → 最下方 Issue）
   - **Your User ID**（Basic Settings 分頁）
5. 用 LINE 掃描 Bot 的 QR Code **加入好友**

### 3. 設定 GitHub Secrets

在你的 GitHub repo → **Settings → Secrets and variables → Actions**，新增：

| Secret 名稱 | 說明 |
|------------|------|
| `GEMINI_API_KEY` | Google Gemini API 金鑰（免費）|
| `LINE_CHANNEL_TOKEN` | LINE Channel Access Token |
| `LINE_USER_ID` | 你的 LINE User ID |

### 4. 自訂新聞主題

編輯 `scripts/news_report.py` 第 10～14 行的 `TOPICS` 清單：

```python
TOPICS = [
    "AI 人工智慧",
    "台灣科技",
    "Android 開發",
]
```

### 5. 上傳到 GitHub

```bash
git init
git add .
git commit -m "初始化新聞報告機器人"
git remote add origin https://github.com/你的帳號/line-news-bot.git
git push -u origin main
```

---

## 手動觸發

在 GitHub repo → **Actions → 每日新聞報告 → Run workflow**，可立即測試。

---

## 費用說明

| 服務 | 費用 |
|------|------|
| GitHub Actions | 公開 repo 完全免費 |
| Google Gemini API | 每天 1500 次請求免費，**完全免費** |
| LINE Messaging API | 每月 200 則免費（每天 1 則綽綽有餘）|

**👉 整個專案零費用！**
