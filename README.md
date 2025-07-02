# Blockchain Income Monitor Bot

## Features
- Monitor BTC, ETH, USDT (ERC-20, TRC-20, BEP-20), TRX, BNB addresses
- Notify Telegram group when new incoming/outgoing transactions are detected
- Multiple groups and addresses supported

## Setup

1. Clone the repo:
```bash
git clone <your_repo_url>
cd <your_repo>
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set environment variables:
```bash
export BOT_TOKEN=xxx
export CHAT_ID=xxx
export BTC_ADDRESSES=addr1,addr2,...
export ETHERSCAN_API_KEY=xxx
```

4. Run the bot:
```bash
python main.py
```

Make sure to set your addresses and keys in environment variables or use `.env` management.
