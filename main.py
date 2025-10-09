from flask import Flask, request
import requests
import os

app = Flask(__name__)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def send_telegram(text):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("❌ Faltan credenciales")
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    requests.post(url, json=payload)

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json()
        side = data.get("side", "N/A")
        symbol = data.get("symbol", "N/A")
        price = data.get("price", "N/A")
        tf = data.get("tf", "N/A")
        
        emoji = "🟢" if side == "BUY" else "🔴"
        msg = (
            f"{emoji} <b>XTB - SEÑAL {side}</b>\n"
            f"📊 <code>{symbol}</code>\n"
            f"💰 Precio: {price}\n"
            f"⏱️ Timeframe: {tf}\n"
            f"📍 Activos: Oro, Petróleo, Gas, USD/JPY, etc."
        )
        send_telegram(msg)
        return "OK", 200
    except Exception as e:
        print("Error:", e)
        return "Error", 500

@app.route('/')
def home():
    return "✅ XTB Commodities Bot - Activo"