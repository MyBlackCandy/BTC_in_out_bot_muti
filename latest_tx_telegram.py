import os
import requests

# ✅ ตั้งค่า
TG_TOKEN = os.getenv("BOT_TOKEN", "ใส่_TOKEN_ของคุณ")
CHAT_ID = os.getenv("CHAT_ID", "ใส่_CHATID_ของคุณ")
ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY", "ใส่_คีย์_etherscan")
ETH_ADDRESSES = os.getenv("ETH_ADDRESSES", "").split(",")
BTC_ADDRESSES = os.getenv("BTC_ADDRESSES", "").split(",")

# ✅ ฟังก์ชันส่งข้อความ
def send_telegram(text):
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print("Telegram Error:", e)

# ✅ ตรวจ ETH
def get_latest_eth_tx(address):
    try:
        url = f"https://api.etherscan.io/api?module=account&action=txlist&address={address}&sort=desc&apikey={ETHERSCAN_API_KEY}"
        res = requests.get(url).json()
        txs = res.get("result", [])
        if txs:
            return txs[0]
    except Exception as e:
        print(f"ETH Error {address}:", e)
    return None

# ✅ ตรวจ BTC
def get_latest_btc_tx(address):
    try:
        url = f"https://mempool.space/api/address/{address}/txs"
        res = requests.get(url).json()
        if res:
            return res[0]
    except Exception as e:
        print(f"BTC Error {address}:", e)
    return None

# ✅ แสดงรายการล่าสุดทั้งหมด + ส่ง Telegram
def notify_latest_transactions():
    eth_price = get_price("ETHUSDT")
    btc_price = get_price("BTCUSDT")

    for eth in ETH_ADDRESSES:
        eth = eth.strip()
        tx = get_latest_eth_tx(eth)
        if tx:
            val = int(tx["value"]) / 1e18
            usd = val * eth_price
            direction = "入" if tx["to"].lower() == eth.lower() else "出"
            msg = f"""📌 *รายการล่าสุด (ETH {direction})*
👤 จาก: `{tx['from']}`
👥 ถึง: `{tx['to']}`
💰 {val:.6f} ETH ≈ ${usd:,.2f}
🔗 TxHash: `{tx['hash']}`"""
            send_telegram(msg)

    for btc in BTC_ADDRESSES:
        btc = btc.strip()
        tx = get_latest_btc_tx(btc)
        if tx:
            val = sum(out["value"] for out in tx["vout"] if out.get("scriptpubkey_address") == btc) / 1e8
            usd = val * btc_price
            from_addr = "N/A"
            if tx["vin"] and tx["vin"][0].get("prevout"):
                from_addr = tx["vin"][0]["prevout"].get("scriptpubkey_address", "ไม่ทราบ")
            msg = f"""📌 *รายการล่าสุด (BTC 入金)*
👤 จาก: `{from_addr}`
👥 ถึง: `{btc}`
💰 {val:.8f} BTC ≈ ${usd:,.2f}
🔗 TxID: `{tx['txid']}`"""
            send_telegram(msg)

# ✅ ฟังก์ชันดึงราคา
def get_price(symbol="BTCUSDT"):
    try:
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
        res = requests.get(url).json()
        return float(res["price"])
    except:
        return 0

if __name__ == "__main__":
    notify_latest_transactions()
