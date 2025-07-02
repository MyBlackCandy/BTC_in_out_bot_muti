import os
import time
import requests

def send_telegram(text, token, chat_ids):
    for chat_id in chat_ids:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        data = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
        try:
            requests.post(url, data=data)
        except Exception as e:
            print("Telegram Error:", e)

def get_latest_btc_tx(address):
    try:
        url = f"https://blockchain.info/rawaddr/{address}"
        res = requests.get(url).json()
        txs = res.get("txs", [])
        for tx in txs:
            for out in tx["out"]:
                if out.get("addr") == address:
                    return tx
    except Exception as e:
        print("BTC Error:", e)
    return None

def get_price(symbol):
    try:
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
        return float(requests.get(url).json()["price"])
    except:
        return 0

def start_monitoring():
    token = os.getenv("BOT_TOKEN")
    chat_ids = os.getenv("CHAT_ID", "").split(",")
    btc_addresses = os.getenv("BTC_ADDRESSES", "").split(",")
    last_seen = {}

    while True:
        btc_price = get_price("BTCUSDT")

        for addr in btc_addresses:
            addr = addr.strip()
            if not addr:
                continue
            tx = get_latest_btc_tx(addr)
            if tx and tx["hash"] != last_seen.get(addr):
                value = sum([out["value"] for out in tx["out"] if out.get("addr") == addr]) / 1e8
                from_addr = tx["inputs"][0]["prev_out"].get("addr", "N/A") if tx.get("inputs") else "N/A"
                usd = value * btc_price
                msg = f"""🟢 *BTC 入金*
👤 从: `{from_addr}`
👥 到: `{addr}`
💰 {value:.8f} BTC ≈ ${usd:,.2f}"""
                send_telegram(msg, token, chat_ids)
                last_seen[addr] = tx["hash"]

        time.sleep(10)
