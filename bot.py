import logging
import os
from binance.client import Client
from dotenv import load_dotenv

class BasicBot:
    """
    BasicBot for Binance Futures Testnet trading.
    Handles connection, symbol validation, and order placement.
    """
    def __init__(self):
        load_dotenv()
        api_key = os.getenv('BINANCE_API_KEY')
        api_secret = os.getenv('BINANCE_API_SECRET')
        self.client = Client(api_key, api_secret, testnet=True)
        self.symbols = self._fetch_symbols()

    def _fetch_symbols(self):
        try:
            info = self.client.futures_exchange_info()
            return {s['symbol']: s for s in info['symbols']}
        except Exception as e:
            logging.error(f"Failed to fetch symbols: {e}")
            return {}

    def is_valid_symbol(self, symbol: str) -> bool:
        return symbol.upper() in self.symbols

    def get_symbol_filters(self, symbol: str):
        """Return the filters for a given symbol (step size, tick size, min qty, etc)."""
        symbol_info = self.symbols.get(symbol.upper())
        if not symbol_info:
            return None
        filters = {f['filterType']: f for f in symbol_info['filters']}
        return filters

    def adjust_to_step(self, value: float, step: float) -> float:
        """Adjust value down to the nearest step size allowed by the exchange."""
        from math import floor
        return floor(value / step) * step

    def validate_order_precision(self, symbol: str, quantity: float, price: float = None) -> dict:
        """Validate and adjust quantity and price to allowed precision for the symbol."""
        filters = self.get_symbol_filters(symbol)
        if not filters:
            return {"error": f"Symbol info not found for {symbol}"}
        lot_size = filters.get('LOT_SIZE')
        price_filter = filters.get('PRICE_FILTER')
        if lot_size:
            step_size = float(lot_size['stepSize'])
            min_qty = float(lot_size['minQty'])
            quantity = self.adjust_to_step(quantity, step_size)
            if quantity < min_qty:
                return {"error": f"Quantity {quantity} is below minimum {min_qty} for {symbol}"}
        if price is not None and price_filter:
            tick_size = float(price_filter['tickSize'])
            min_price = float(price_filter['minPrice'])
            price = self.adjust_to_step(price, tick_size)
            if price < min_price:
                return {"error": f"Price {price} is below minimum {min_price} for {symbol}"}
        return {"quantity": quantity, "price": price}

    def place_market_order(self, symbol: str, side: str, quantity: float):
        """Place a market order after validating input."""
        if not self.is_valid_symbol(symbol):
            logging.error(f"Invalid symbol: {symbol}")
            return {"error": f"Invalid symbol: {symbol}"}
        if side.upper() not in ["BUY", "SELL"]:
            logging.error(f"Invalid side: {side}")
            return {"error": f"Invalid side: {side}"}
        if quantity <= 0:
            logging.error(f"Invalid quantity: {quantity}")
            return {"error": f"Invalid quantity: {quantity}"}
        precision_check = self.validate_order_precision(symbol, quantity)
        if 'error' in precision_check:
            logging.error(precision_check['error'])
            return {"error": precision_check['error']}
        quantity = precision_check['quantity']
        try:
            logging.info(f"Placing MARKET order: {symbol} {side} {quantity}")
            order = self.client.futures_create_order(
                symbol=symbol.upper(),
                side=side.upper(),
                type="MARKET",
                quantity=quantity
            )
            logging.info(f"Order response: {order}")
            return order
        except Exception as e:
            logging.error(f"Market order failed: {e}")
            return {"error": str(e)}

    def place_limit_order(self, symbol: str, side: str, quantity: float, price: float):
        """Place a limit order after validating input."""
        if not self.is_valid_symbol(symbol):
            logging.error(f"Invalid symbol: {symbol}")
            return {"error": f"Invalid symbol: {symbol}"}
        if side.upper() not in ["BUY", "SELL"]:
            logging.error(f"Invalid side: {side}")
            return {"error": f"Invalid side: {side}"}
        if quantity <= 0 or price <= 0:
            logging.error(f"Invalid quantity or price: {quantity}, {price}")
            return {"error": f"Invalid quantity or price: {quantity}, {price}"}
        precision_check = self.validate_order_precision(symbol, quantity, price)
        if 'error' in precision_check:
            logging.error(precision_check['error'])
            return {"error": precision_check['error']}
        quantity = precision_check['quantity']
        price = precision_check['price']
        try:
            logging.info(f"Placing LIMIT order: {symbol} {side} {quantity} @ {price}")
            order = self.client.futures_create_order(
                symbol=symbol.upper(),
                side=side.upper(),
                type="LIMIT",
                quantity=quantity,
                price=price,
                timeInForce="GTC"
            )
            logging.info(f"Order response: {order}")
            return order
        except Exception as e:
            logging.error(f"Limit order failed: {e}")
            return {"error": str(e)}

    def place_stop_limit_order(self, symbol: str, side: str, quantity: float, price: float, stop_price: float):
        """
        Place a stop-limit order (type='STOP') on Binance Futures.
        :param symbol: Trading pair symbol (e.g., BTCUSDT)
        :param side: 'BUY' or 'SELL'
        :param quantity: Order quantity
        :param price: Limit price (the price at which the limit order will be placed after stop is triggered)
        :param stop_price: Stop price (the trigger price)
        :return: API response dict or error dict
        """
        if not self.is_valid_symbol(symbol):
            logging.error(f"Invalid symbol: {symbol}")
            return {"error": f"Invalid symbol: {symbol}"}
        if side.upper() not in ["BUY", "SELL"]:
            logging.error(f"Invalid side: {side}")
            return {"error": f"Invalid side: {side}"}
        if quantity <= 0 or price <= 0 or stop_price <= 0:
            logging.error(f"Invalid quantity/price/stop_price: {quantity}, {price}, {stop_price}")
            return {"error": "Quantity, price, and stop price must be positive numbers."}
        precision_check = self.validate_order_precision(symbol, quantity, price)
        if 'error' in precision_check:
            logging.error(precision_check['error'])
            return {"error": precision_check['error']}
        quantity = precision_check['quantity']
        price = precision_check['price']
        try:
            logging.info(f"Placing STOP (stop-limit) order: {symbol} {side} qty={quantity} price={price} stop={stop_price}")
            order = self.client.futures_create_order(
                symbol=symbol.upper(),
                side=side.upper(),
                type="STOP",
                quantity=quantity,
                price=price,
                stopPrice=stop_price,
                timeInForce="GTC"
            )
            logging.info(f"Order response: {order}")
            return order
        except Exception as e:
            logging.error(f"Error placing STOP (stop-limit) order: {e}")
            return {"error": str(e)}
