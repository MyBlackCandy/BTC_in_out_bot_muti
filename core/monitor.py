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

def get_btc_tx(address):
    try:
        url = f"https://mempool.space/api/address/{address}"
        res = requests.get(url).json()
        return res.get("txs", [])[0] if res.get("txs") else None
    except Exception as e:
        print("BTC Error:", e)
    return None

def get_eth_tx(address, api_key):
    try:
        url = f"https://api.etherscan.io/api?module=account&action=txlist&address={address}&sort=desc&apikey={api_key}"
        res = requests.get(url).json()
        return res.get("result", [])[0] if res.get("result") else None
    except Exception as e:
        print("ETH Error:", e)
    return None

def get_price(symbol):
    try:
        r = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}").json()
        return float(r["price"])
    except:
        return 0

def start_monitoring():
    token = os.getenv("BOT_TOKEN")
    chat_ids = os.getenv("CHAT_ID", "").split(",")
    btc_addresses = os.getenv("BTC_ADDRESSES", "").split(",")
    eth_addresses = os.getenv("ETH_ADDRESSES", "").split(",")
    etherscan_api = os.getenv("ETHERSCAN_API_KEY", "")
    seen = {}

    while True:
        btc_price = get_price("BTCUSDT")
        eth_price = get_price("ETHUSDT")

        for addr in btc_addresses:
            addr = addr.strip()
            if not addr:
                continue
            tx = get_btc_tx(addr)
            if isinstance(tx, dict) and tx.get("txid") and tx["txid"] != seen.get(addr):
                is_incoming = any(out.get("scriptpubkey_address") == addr for out in tx.get("vout", []))
                value = sum(out.get("value", 0) for out in tx.get("vout", []) if out.get("scriptpubkey_address") == addr) / 1e8
                from_addr = tx.get("vin", [{}])[0].get("prevout", {}).get("scriptpubkey_address", "N/A")
                direction = "入金" if is_incoming else "出金"
                usd = value * btc_price
                msg = f"🟢 *BTC {direction}*
👤 从: `{from_addr}`
👥 到: `{addr}`
💰 {value:.8f} BTC ≈ ${usd:,.2f}"
                send_telegram(msg, token, chat_ids)
                seen[addr] = tx["txid"]

        for addr in eth_addresses:
            addr = addr.strip()
            if not addr:
                continue
            tx = get_eth_tx(addr, etherscan_api)
            if isinstance(tx, dict) and tx.get("hash") and tx["hash"] != seen.get(addr):
                value = int(tx["value"]) / 1e18
                direction = "入金" if tx["to"].lower() == addr.lower() else "出金"
                usd = value * eth_price
                msg = f"🟢 *ETH {direction}*
👤 从: `{tx['from']}`
👥 到: `{tx['to']}`
💰 {value:.6f} ETH ≈ ${usd:,.2f}"
                send_telegram(msg, token, chat_ids)
                seen[addr] = tx["hash"]

        time.sleep(30)
