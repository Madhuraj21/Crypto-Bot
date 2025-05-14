import logging
from bot import BasicBot

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s',
        handlers=[
            logging.FileHandler('bot.log'),
            logging.StreamHandler()
        ]
    )

def get_float_input(prompt: str) -> float:
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("Value must be positive.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a number.")

def get_symbol_input(bot: BasicBot) -> str:
    while True:
        symbol = input("Enter symbol (e.g., BTCUSDT): ").upper()
        if bot.is_valid_symbol(symbol):
            return symbol
        print("Invalid symbol. Please enter a valid symbol supported by Binance Futures.")

def get_side_input() -> str:
    while True:
        side = input("Enter side (BUY/SELL): ").upper()
        if side in ["BUY", "SELL"]:
            return side
        print("Invalid side. Please enter 'BUY' or 'SELL'.")

def print_order_result(order: dict):
    if 'error' in order:
        print(f"Error: {order['error']}")
        return
    # Display key order details in a user-friendly way
    print("\nOrder Result:")
    print(f"  Order ID:     {order.get('orderId')}")
    print(f"  Symbol:       {order.get('symbol')}")
    print(f"  Side:         {order.get('side')}")
    print(f"  Type:         {order.get('type')}")
    print(f"  Status:       {order.get('status')}")
    print(f"  Quantity:     {order.get('origQty')}")
    print(f"  Executed Qty: {order.get('executedQty')}")
    print(f"  Price:        {order.get('price')}")
    print(f"  Avg Price:    {order.get('avgPrice')}")
    if order.get('type') == 'STOP_MARKET':
        print(f"  Stop Price:   {order.get('stopPrice')}")
    print(f"  Time in Force:{order.get('timeInForce')}")
    print(f"  Client Order ID: {order.get('clientOrderId')}")
    print()

def main():
    setup_logging()
    bot = BasicBot()
    print("Binance Futures Testnet Trading Bot Initialized.")
    while True:
        print("\n1. Place Market Order\n2. Place Limit Order\n3. Place Stop-Limit Order\n4. Exit")
        choice = input("Select an option: ")
        if choice == "1":
            symbol = get_symbol_input(bot)
            side = get_side_input()
            quantity = get_float_input("Enter quantity: ")
            confirm = input(f"Confirm MARKET order {side} {quantity} {symbol}? (y/n): ").lower()
            if confirm == 'y':
                result = bot.place_market_order(symbol, side, quantity)
                print_order_result(result)
        elif choice == "2":
            symbol = get_symbol_input(bot)
            side = get_side_input()
            quantity = get_float_input("Enter quantity: ")
            price = get_float_input("Enter price: ")
            confirm = input(f"Confirm LIMIT order {side} {quantity} {symbol} @ {price}? (y/n): ").lower()
            if confirm == 'y':
                result = bot.place_limit_order(symbol, side, quantity, price)
                print_order_result(result)
        elif choice == "3":
            symbol = get_symbol_input(bot)
            side = get_side_input()
            quantity = get_float_input("Enter quantity: ")
            stop_price = get_float_input("Enter stop price: ")
            price = get_float_input("Enter limit price: ")
            confirm = input(f"Confirm STOP-LIMIT order {side} {quantity} {symbol} stop @ {stop_price} limit @ {price}? (y/n): ").lower()
            if confirm == 'y':
                result = bot.place_stop_limit_order(symbol, side, quantity, price, stop_price)
                print_order_result(result)
        elif choice == "4":
            print("Exiting bot.")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
