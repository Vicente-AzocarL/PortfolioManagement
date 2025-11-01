from classes import Stock, Portfolio
import os
import platform
import random

def clear_screen():
    """Clear the terminal screen."""
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

def print_menu(stocks):
    print("Current stocks:")
    for sym, stock in stocks.items():
        print(f"- {sym}: ${stock.get_price():.2f}\n")
    print("\n--- Portfolio Manager CLI ---")
    print("1. Create a new portfolio")
    print("2. Switch portfolio")
    print("3. Show current portfolio summary")
    print("4. Add stock to portfolio")
    print("5. Sell stock from portfolio")
    print("6. Set target allocation")
    print("7. Show allocation")
    print("8. Rebalance portfolio")
    print("9. List portfolios")
    print("X. Modify Stocks")
    print("0. Exit")
    print("-----------------------------")


def select_portfolio(portfolios, current_portfolio_name):
    if not portfolios:
        print("No portfolios created yet.")
        return None
    print("\nAvailable portfolios:")
    for name in portfolios.keys():
        mark = "*" if name == current_portfolio_name else ""
        print(f"- {name} {mark}")
    selected = input("Enter portfolio name to switch to: ").strip()
    if selected in portfolios:
        print(f"Switched to portfolio '{selected}'.")
        return selected
    else:
        print("Portfolio not found.")
        return current_portfolio_name


def create_test_data(portfolios, stocks):
    """Creates a demo scenario for testing."""
    print("Creating test scenario...")
    portfolios["Demo"] = Portfolio()
    demo_portfolio = portfolios["Demo"]

    demo_portfolio.add_stock(stocks["AAPL"], random.randint(10, 50))
    demo_portfolio.add_stock(stocks["MSFT"], random.randint(5, 30))
    demo_portfolio.add_stock(stocks["GOOG"], random.randint(2, 20))

    demo_portfolio.set_allocation({
        stocks["AAPL"]: 50,
        stocks["MSFT"]: 30,
        stocks["GOOG"]: 20
    })

    print("Test portfolio 'Demo' created successfully.")
    return "Demo"


def modify_stocks(stocks):
    """Menu to view, add, or update stocks."""
    while True:
        print("\n--- Modify Stocks ---")
        print("Current stocks:")
        for sym, stock in stocks.items():
            print(f"- {sym}: ${stock.get_price():.2f}")
        print("\nOptions:")
        print("1. Add new stock")
        print("2. Update existing stock price")
        print("0. Back to main menu")
        choice = input("Select an option: ").strip()

        if choice == "0":
            break
        elif choice == "1":
            symbol = input("Enter new stock symbol: ").upper()
            if symbol in stocks:
                print("Stock already exists.")
            else:
                try:
                    price = float(input("Enter initial price: "))
                    stocks[symbol] = Stock(symbol, price)
                    print(f"Added stock {symbol} with price ${price:.2f}.")
                except ValueError:
                    print("Invalid price entered.")
        elif choice == "2":
            symbol = input("Enter stock symbol to update: ").upper()
            if symbol not in stocks:
                print("Stock not found.")
            else:
                try:
                    new_price = float(input(f"Enter new price for {symbol}: "))
                    stocks[symbol].current_price(new_price)
                    print(f"Updated {symbol} price to ${new_price:.2f}.")
                except ValueError as e:
                    print(e)
        else:
            print("Invalid option.")


def show_portfolio_summary(portfolios, current_portfolio_name, stocks):
    """Displays all portfolio details in one command."""
    if not current_portfolio_name:
        print("No portfolio selected.")
        return

    portfolio = portfolios[current_portfolio_name]
    print(f"\n=== Portfolio: {current_portfolio_name} ===")

    stocks_list = portfolio.get_stocks()
    if not stocks_list:
        print("No stocks in this portfolio.")
        return

    total_value = portfolio.total_value()
    print("\nStocks:")
    for sym, shares in stocks_list.items():
        price = stocks[sym].get_price()
        value = shares * price
        print(f"- {sym}: {shares} shares @ ${price:.2f} → ${value:.2f}")

    print(f"\nTotal portfolio value: ${total_value:.2f}")

    allocations = portfolio.get_allocation()
    if allocations:
        print("\nTarget Allocation:")
        for sym, alloc in allocations.items():
            print(f"- {sym}: {alloc}")
    else:
        print("\nNo allocation set yet.")


def rebalance_portfolio(portfolio: Portfolio, threshold: float = 0.01):
    """Interactive rebalance: suggests and optionally applies rebalancing actions."""
    total_value = portfolio.total_value()
    if total_value == 0:
        print("Cannot rebalance an empty portfolio.")
        return

    if not portfolio.allocated_stocks:
        print("No allocation set for this portfolio.")
        return

    print("\n--- Rebalance Suggestions ---")
    actions = []

    for stock, target_allocation in portfolio.allocated_stocks.items():
        target_value = (target_allocation / 100) * total_value
        current_value = stock.get_price() * portfolio.stocks.get(stock, 0)
        difference = target_value - current_value

        if abs(difference) / total_value > threshold:
            shares_to_trade = difference / stock.get_price()
            action = "Buy" if shares_to_trade > 0 else "Sell"
            print(f"{action} {abs(shares_to_trade):.2f} shares of {stock.get_symbol()}")
            actions.append((stock, shares_to_trade))
        else:
            print(f"No action needed for {stock.get_symbol()}")

    if not actions:
        print("All allocations within threshold.")
        return

    confirm = input("\nApply these rebalancing actions automatically? (y/n): ").strip().lower()
    if confirm == "y":
        for stock, shares_to_trade in actions:
            current_shares = portfolio.stocks.get(stock, 0)
            new_shares = current_shares + shares_to_trade
            if new_shares < 0:
                new_shares = 0
            portfolio.stocks[stock] = new_shares
        print("✅ Portfolio rebalanced successfully.")
    else:
        print("❌ Rebalance canceled.")

def main():
    # --- Initialize with some default stocks ---
    stocks = {
        "AAPL": Stock("AAPL", 190.0),
        "MSFT": Stock("MSFT", 320.0),
        "GOOG": Stock("GOOG", 140.0),
        "TSLA": Stock("TSLA", 250.0),
        "AMZN": Stock("AMZN", 130.0),
    }

    portfolios = {}
    current_portfolio_name = None


    clear_screen()
    print("Welcome to the Portfolio Management CLI.")
    print("Type 'test' at any time to create a demo portfolio with sample data.")

    while True:
        print_menu(stocks)
        choice = input("Select an option: ").strip()

        clear_screen()

        if choice.lower() == "test":
            current_portfolio_name = create_test_data(portfolios, stocks)
            continue

        if choice == "0":
            print("Exiting Portfolio Manager. Goodbye!")
            break

        elif choice == "1":
            name = input("Enter portfolio name: ").strip()
            if name in portfolios:
                print("Portfolio already exists.")
            else:
                portfolios[name] = Portfolio()
                current_portfolio_name = name
                print(f"Portfolio '{name}' created and selected.")

        elif choice == "2":
            current_portfolio_name = select_portfolio(portfolios, current_portfolio_name)

        elif choice == "3":
            show_portfolio_summary(portfolios, current_portfolio_name, stocks)

        elif choice == "4":
            if not current_portfolio_name:
                print("No portfolio selected.")
                continue
            symbol = input("Enter stock symbol: ").upper()
            if symbol not in stocks:
                print("Stock not found. Please add it first using 'Modify Stocks'.")
                continue
            try:
                shares = float(input("Enter number of shares to add: "))
                portfolios[current_portfolio_name].add_stock(stocks[symbol], shares)
                print(f"Added {shares} shares of {symbol}.")
            except ValueError as e:
                print(e)

        elif choice == "5":
            if not current_portfolio_name:
                print("No portfolio selected.")
                continue
            symbol = input("Enter stock symbol to sell: ").upper()
            if symbol not in stocks:
                print("Stock not found.")
                continue
            try:
                shares = float(input("Enter number of shares to sell: "))
                portfolios[current_portfolio_name].sell_stock(stocks[symbol], shares)
                print(f"Sold {shares} shares of {symbol}.")
            except ValueError as e:
                print(e)

        elif choice == "6":
            if not current_portfolio_name:
                print("No portfolio selected.")
                continue
            portfolio = portfolios[current_portfolio_name]
            stocks_in_portfolio = portfolio.get_stocks()
            if not stocks_in_portfolio:
                print("No stocks in portfolio.")
                continue
            allocation_dict = {}
            total_alloc = 0
            print("Set allocation percentages (must total 100%)")
            for sym in stocks_in_portfolio.keys():
                try:
                    alloc = float(input(f"{sym}: "))
                    allocation_dict[stocks[sym]] = alloc
                    total_alloc += alloc
                except ValueError:
                    print("Invalid input.")
                    break
            try:
                portfolio.set_allocation(allocation_dict)
                print("Allocations set successfully.")
            except ValueError as e:
                print(e)

        elif choice == "7":
            if not current_portfolio_name:
                print("No portfolio selected.")
                continue
            allocations = portfolios[current_portfolio_name].get_allocation()
            if not allocations:
                print("No allocations set.")
            else:
                print("\nCurrent Allocations:")
                for sym, alloc in allocations.items():
                    print(f"- {sym}: {alloc}")

        elif choice == "8":
            if not current_portfolio_name:
                print("No portfolio selected.")
                continue
            try:
                threshold = float(input("Enter rebalance threshold (default=0.01): ") or 0.01)
                rebalance_portfolio(portfolios[current_portfolio_name], threshold)
            except ValueError:
                print("Invalid threshold.")

        elif choice == "9":
            if portfolios:
                print("\nAvailable portfolios:")
                for name in portfolios.keys():
                    mark = "*" if name == current_portfolio_name else ""
                    print(f"- {name} {mark}")
            else:
                print("No portfolios created.")

        elif choice.lower() == "x":
            modify_stocks(stocks)

        else:
            print("Invalid option, please try again.")


if __name__ == "__main__":
    main()
