import requests
from bs4 import BeautifulSoup
import time

URL = "https://lopmoi.giasutrithuc.net/covua"
BOT_TOKEN = "8009452196:AAEpTgVa3gfbS1qUfXTg3IrcnQdCmmjF1UE"
CHAT_ID = "7193701944"
CHECK_INTERVAL = 300
seen_ids = set()

def get_class_info():
    try:
        soup = BeautifulSoup(requests.get(URL).text, "html.parser")
        class_divs = soup.find_all("div", class_="col-md-4 col-sm-6 col-xs-12")
        class_data = {}
        for div in class_divs:
            text = div.get_text(separator="\n").strip()
            lines = text.split("\n")
            class_id_line = next((line for line in lines if "Mã lớp:" in line), "")
            if class_id_line:
                class_id = class_id_line.split("Mã lớp:")[-1].strip()
                class_data[class_id] = text
        return class_data
    except Exception as e:
        print("❌ Lỗi:", e)
        return {}

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        r = requests.post(url, data={"chat_id": CHAT_ID, "text": msg})
        if r.status_code != 200:
            print("❌ Telegram lỗi:", r.text)
    except Exception as e:
        print("❌ Gửi lỗi:", e)

send_telegram("🤖 Bot lớp CỜ VUA đã chạy trên Render!")

while True:
    class_info = get_class_info()
    new_ids = set(class_info.keys()) - seen_ids
    for class_id in new_ids:
        send_telegram(f"📢 Lớp mới:\n{class_info[class_id]}")
    seen_ids.update(new_ids)
    time.sleep(CHECK_INTERVAL)
