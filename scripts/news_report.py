import feedparser
import requests
import os
import time
from datetime import datetime

# ============================================================
# ✏️  在這裡設定你想追蹤的新聞主題（可自由新增或刪除）
# ============================================================
TOPICS = [
    "台幣兌換美金利率"
    "AI 人工智慧",
    "台積電",
    "美國總統",
    "晶片"
    "關稅"
    "美股消息"
]

# 每個主題最多抓幾則新聞
MAX_NEWS_PER_TOPIC = 5

# Gemini 使用的模型（免費）
GEMINI_MODEL = "gemini-2.5-flash"


def fetch_news(topic: str) -> list[dict]:
    """從 Google News RSS 撈指定主題的新聞"""
    url = (
        f"https://news.google.com/rss/search"
        f"?q={requests.utils.quote(topic)}"
        f"&hl=zh-TW&gl=TW&ceid=TW:zh-Hant"
    )
    feed = feedparser.parse(url)
    articles = []
    for entry in feed.entries[:MAX_NEWS_PER_TOPIC]:
        articles.append({
            "title": entry.get("title", "（無標題）"),
            "link": entry.get("link", ""),
            "published": entry.get("published", ""),
        })
    return articles


def summarize_with_gemini(topic: str, articles: list[dict]) -> str:
    """將新聞標題餵給 Gemini API，整理成繁體中文摘要報告"""
    api_key = os.environ["GEMINI_API_KEY"]

    news_text = "\n".join([
        f"- {a['title']} ({a['published']})\n  {a['link']}"
        for a in articles
    ])

    prompt = (
        f"以下是關於「{topic}」的最新新聞標題，\n"
        f"請用繁體中文整理成一份簡短的重點摘要報告（3～5點），\n"
        f"並指出最值得關注的趨勢。\n\n"
        f"新聞列表：\n{news_text}"
    )

    url = (
        f"https://generativelanguage.googleapis.com/v1beta/models/"
        f"{GEMINI_MODEL}:generateContent?key={api_key}"
    )

    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    # 最多重試 3 次（應對 429/503 暫時性錯誤）
    for attempt in range(3):
        res = requests.post(url, json=payload)

        if res.status_code == 200:
            data = res.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]
        elif res.status_code in (429, 503):
            wait = (attempt + 1) * 10  # 第1次等10秒，第2次等20秒，第3次等30秒
            print(f"⚠️ Gemini 暫時無法使用（{res.status_code}），{wait} 秒後重試（第 {attempt + 1} 次）...")
            time.sleep(wait)
        else:
            print(f"❌ Gemini API 錯誤：{res.status_code} {res.text}")
            return "（摘要產生失敗，請檢查 API Key）"

    print(f"❌ Gemini 重試 3 次仍失敗，跳過此主題")
    return "（Gemini 伺服器忙碌，請稍後再試）"


def send_line(message: str) -> None:
    """透過 LINE Messaging API 推送訊息"""
    token = os.environ["LINE_CHANNEL_TOKEN"]
    user_id = os.environ["LINE_USER_ID"]

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    # LINE 單則文字訊息上限 5000 字，超過則分段傳送
    max_len = 5000
    for i in range(0, len(message), max_len):
        payload = {
            "to": user_id,
            "messages": [
                {
                    "type": "text",
                    "text": message[i:i + max_len],
                }
            ],
        }
        res = requests.post(
            "https://api.line.me/v2/bot/message/push",
            headers=headers,
            json=payload,
        )
        if res.status_code == 200:
            print(f"✅ LINE 傳送成功（第 {i // max_len + 1} 段）")
        else:
            print(f"❌ LINE 傳送失敗：{res.status_code} {res.text}")


def main() -> None:
    today = datetime.now().strftime("%Y/%m/%d")
    report = f"📰 每日新聞報告 {today}\n\n"

    for topic in TOPICS:
        print(f"🔍 正在處理主題：{topic}")
        articles = fetch_news(topic)

        if not articles:
            print(f"  ⚠️ 找不到相關新聞，跳過")
            continue

        summary = summarize_with_gemini(topic, articles)
        report += "━" * 20 + "\n"
        report += f"🔍 {topic}\n\n"
        report += f"{summary}\n\n"

    print("\n📤 傳送報告到 LINE...")
    send_line(report)
    print("✅ 完成！")


if __name__ == "__main__":
    main()
