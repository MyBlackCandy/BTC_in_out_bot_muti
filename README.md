# Blockchain Monitor Bot (BTC & ETH)

## Features
- ✅ Monitor BTC (via mempool.space) and ETH (via Etherscan)
- ✅ Notify only new transactions per address
- ✅ Distinguish Incoming (入金) vs Outgoing (出金)
- ✅ Notify multiple Telegram groups
- ✅ Support multiple wallet addresses
- ✅ Runs every 30 seconds

## Environment Variables

- `BOT_TOKEN`: Telegram Bot Token
- `CHAT_ID`: Comma-separated Telegram Chat IDs
- `BTC_ADDRESSES`: Comma-separated BTC wallet addresses
- `ETH_ADDRESSES`: Comma-separated ETH wallet addresses
- `ETHERSCAN_API_KEY`: Etherscan API Key

## Usage

```bash
pip install -r requirements.txt
python main.py
```
