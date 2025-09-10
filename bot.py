# bot.py
import os, json, sys, requests
from datetime import datetime, time
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise SystemExit("TELEGRAM_BOT_TOKEN not set")

with open("config.json", "r", encoding="utf-8") as f:
    cfg = json.load(f)

chat_id = cfg["chat_id"]

def set_permissions(can_send_messages):
    url = f"https://api.telegram.org/bot{TOKEN}/setChatPermissions"
    payload = {
        "chat_id": chat_id,
        "permissions": {
            "can_send_messages": can_send_messages,
            "can_send_media_messages": can_send_messages,
            "can_send_polls": can_send_messages,
            "can_send_other_messages": can_send_messages,
            "can_add_web_page_previews": can_send_messages,
            "can_change_info": False,
            "can_invite_users": False,
            "can_pin_messages": False
        }
    }
    r = requests.post(url, json=payload)
    print(r.status_code, r.text)
    return r.json()

def close_chat():
    print("Closing chat:", chat_id)
    return set_permissions(False)

def open_chat():
    print("Opening chat:", chat_id)
    return set_permissions(True)

if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else ""
    if arg == "close":
        close_chat()
    elif arg == "open":
        open_chat()
    else:
        # По умолчанию: использовать время из config.json
        tz = cfg.get("timezone","UTC")
        now = datetime.utcnow().time()  # workflow запускает по UTC; если вы указали другую timezone — скорректируйте cron
        open_t = time.fromisoformat(cfg["open_time"])
        close_t = time.fromisoformat(cfg["close_time"])
        if open_t <= now < close_t:
            open_chat()
        else:
            close_chat()
