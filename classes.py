from typing import Dict

class Stock():
    # Reperesents a stock with symbol and price
    def __init__(self, symbol: str, price: float):
        self.symbol = symbol
        self.price = price

    # Update the current price of the stock
    def current_price(self, new_price: float) -> None:
        if new_price < 0:
            raise ValueError("Price cannot be negative.")
        self.price = new_price
    
    def get_symbol(self) -> str:
        return self.symbol
    
    def get_price(self) -> float:
        return self.price
    


class Portfolio():
    # Represents a portfolio with a dictionary with current stocks and their shares, and also a dictionary with allocated stocks and their target percentages
    def __init__(self):
        self.stocks: Dict[Stock, float] = {}
        self.allocated_stocks: Dict[Stock, float] = {}
    
    # Add shares of a stock to the portfolio
    def add_stock(self, stock: Stock, shares: float) -> None:
        if shares <= 0:
            raise ValueError("Number of shares must be positive.")
        if stock in self.stocks:
            self.stocks[stock] += shares
        else:
            self.stocks[stock] = shares
    # Sell shares of a stock from the portfolio
    def sell_stock(self, stock: Stock, shares: float) -> None:
        if stock not in self.stocks:
            raise ValueError("Stock not in portfolio.")
        if shares <= 0:
            raise ValueError("Number of shares must be positive.")
        if shares > self.stocks[stock]:
            raise ValueError("Not enough shares to sell.")
        self.stocks[stock] -= shares
        if self.stocks[stock] == 0:
            del self.stocks[stock]
    
    # Get the current stocks and their shares in the portfolio
    def get_stocks(self) -> Dict[str, float]:
        stocks = {stock.get_symbol(): shares for stock, shares in self.stocks.items()}
        return stocks
    
    # Set the target allocation percentages for the stocks in the portfolio
    def set_allocation(self, stocks: Dict[Stock, float]) -> None:
        total_allocation = sum(stocks.values())
        if total_allocation != 100:
            raise ValueError("Total allocation must equal 100%.")
        for stock in stocks.keys():
            if stock not in self.stocks:
                raise ValueError(f"Stock {stock.get_symbol()} not in portfolio.")
        self.allocated_stocks = stocks
    
    # Get the target allocation percentages for the stocks in the portfolio
    def get_allocation(self) -> Dict[Stock, float]:
        stocks = {stock.get_symbol(): f"{allocation}%" for stock, allocation in self.allocated_stocks.items()}
        return stocks
    
    # Calculate the total value of the portfolio
    def total_value(self) -> float:
        total = 0.0
        for stock, shares in self.stocks.items():
            total += stock.get_price() * shares
        return total
    
    def rebalance(self, theshold: float = 0.01) -> None:
        # Calculates the number of shares to buy/sell to achieve the desired allocation with a given threshold
        # It prints out the actions needed to rebalance the portfolio
        total_value = self.total_value()
        for stock, target_allocation in self.allocated_stocks.items():
            target_value = (target_allocation / 100) * total_value
            current_value = stock.get_price() * self.stocks[stock]
            difference = target_value - current_value
            if abs(difference) / total_value > theshold:
                shares_to_trade = difference / stock.get_price()
                action = "Buy" if shares_to_trade > 0 else "Sell"
                print(f"{action} {abs(shares_to_trade):.2f} shares of {stock.get_symbol()}")
            else:
                print(f"No action needed for {stock.get_symbol()}")




