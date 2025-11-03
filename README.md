# 💸 Crypto Price Bot

A simple and user-friendly Telegram bot that converts any amount in USD to its real-time equivalent in cryptocurrency using the CoinGecko API.

---

## 🚀 Features

- Real-time crypto price conversion
- Supports both major and lesser-known coins
- Input via buttons or custom coin/ticker name
- Handles input errors gracefully
- Clean structure, easy to extend

---

## 🛠 Requirements

- Python 3.8 or higher
- Telegram bot token from [@BotFather](https://t.me/botfather)

---

## ⚙️ Setup Instructions

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/crypto-price-bot.git
   cd crypto-price-bot
   ```

2. **Create and activate a virtual environment:**

   On **Windows**:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

   On **macOS/Linux**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**

   Create a `.env` file (or copy from `.env.example`) and add your bot token:

   ```
   API_KEY=your_telegram_bot_token_here
   ```

5. **Run the bot:**

   ```bash
   python main.py
   ```

---

## 📁 Project Structure

```
crypto-price-bot/
├── main.py           # main bot logic
├── .env.example      # sample environment config
├── requirements.txt  # Python dependencies
└── README.md         # documentation
```

---

## 🧪 Example Usage

- Start the bot with `/start`
- Enter a USD amount (e.g., `100`)
- Choose from preset currencies or type any coin/ticker (e.g., `solana`, `toncoin`, `trx`)
- Receive instant real-time conversion

---

## 🔐 Notes

- `.env` is **not committed** to the repo and should be created manually.
- The bot uses **CoinGecko's public API** — no API key required.

---

## 📄 License

This project is licensed under the MIT License.
