# Binance Futures Testnet Trading Bot

A robust, menu-driven Python trading bot for Binance USDT-M Futures Testnet. Supports market, limit, and true stop-limit orders with full input validation, logging, and error handling.

---

## Features
- **Market, Limit, and Stop-Limit Orders**: Place buy/sell orders for any supported symbol.
- **Immediate Input Validation**: Symbol, side, quantity, price, and stop price are validated as you enter them.
- **Precision & Step-Size Handling**: Bot auto-adjusts and validates your input to match Binance's requirements for each symbol.
- **Comprehensive Logging**: All API requests, responses, and errors are logged to `bot.log` and the console.
- **User-Friendly CLI**: Menu-driven, with clear prompts and confirmations.
- **API Key Security**: Uses `.env` file and `python-dotenv` for secure credential management.

---

## Setup

### 1. Clone the Repository
```
git clone <your-repo-url>
cd <repo-folder>
```

### 2. Create and Activate a Virtual Environment
```
python -m venv venv
.\venv\Scripts\activate  # On Windows
# Or
source venv/bin/activate  # On Mac/Linux
```

### 3. Install Dependencies
```
pip install -r requirements.txt
```

### 4. Configure API Keys
- Register for a Binance Futures Testnet account: https://testnet.binancefuture.com
- Generate API Key and Secret.
- Create a `.env` file in the project root:
```
BINANCE_API_KEY=your_api_key_here
BINANCE_API_SECRET=your_api_secret_here
```

---

## Usage
```
python main.py
```
- Follow the menu prompts to place market, limit, or stop-limit orders.
- All actions and errors are logged in `bot.log`.

### Example: Place a Stop-Limit Order
```
3
Enter symbol (e.g., BTCUSDT): BTCUSDT
Enter side (BUY/SELL): SELL
Enter quantity: 0.01
Enter stop price: 70000
Enter limit price: 69900
Confirm STOP-LIMIT order SELL 0.01 BTCUSDT stop @ 70000 limit @ 69900? (y/n): y
```

---

## Notes & Best Practices
- **Precision**: The bot auto-adjusts your input to the correct step size and tick size for each symbol.
- **Minimum Notional**: Binance requires a minimum notional value (e.g., $5). If your order is too small, you'll get a clear error.
- **Order Would Immediately Trigger**: For stop-limit orders, ensure your stop price is not already reached by the market.
- **API Key Security**: Never commit your `.env` file or API keys to public repositories.

---

## Logging
- All API requests, responses, and errors are logged to `bot.log`.
- You can review this file for troubleshooting and audit purposes.

---

## Project Structure
```
main.py         # CLI entry point
bot.py          # Core bot logic
requirements.txt
.env            # Your API keys (not to be committed)
bot.log         # Log file (generated at runtime)
```

---

## Troubleshooting
- **Precision/Step Size Errors**: Use the suggested values or let the bot auto-adjust.
- **Order Would Immediately Trigger**: Adjust your stop price so it is not already reached by the market.
- **API/Network Errors**: Check your internet connection and API key permissions.

---

## License
MIT License

---

## Author
Open Source Community
