import random
import matplotlib.pyplot as plt
import yfinance as yf
from datetime import datetime, timedelta

def create_prices(initial_price, volatility, days):
    prices = [initial_price]
    current_price = initial_price
    for _ in range(390 * days - 1): #390 minutes in a trading day
        drift = 0.05 * (initial_price - current_price) / initial_price  # mean reversion factor
        shock = volatility * random.uniform(-1, 1)  # random shock
        next_price = current_price * (1 + drift) + shock
        next_price = round(next_price, 3)
        next_price = max(0, next_price)  # ensure stock does not drop below 0
        prices.append(next_price)
        current_price = next_price
    return prices

def test_prices(symbol, date):
    prices = []
    # Set start and end time for fetching data
    start_time = datetime.combine(date, datetime.min.time())
    end_time = start_time + timedelta(days=1)
    # Fetch intraday data
    data = yf.download(symbol, start=start_time, end=end_time, interval="1m")
    # Extract close prices from data
    for index, row in data.iterrows():
        prices.append(row['Close'])
    return prices

def stock_bot(prices, shares):
    plot = [shares * prices[0]]
    bought = True
    prev_price = prices[0]
    current_money = 0

    for i in range(1, len(prices)):
        stock_price = prices[i]
        #print (stock_price - prev_price)
        if bought:
            if stock_price - prev_price > 0: #if goes up
                bought = False
                current_money = stock_price * shares
                shares = 0
        else:
            if stock_price - prev_price < 0: # if goes down
                bought = True
                shares = current_money / stock_price

        
        prev_price = stock_price
        plot.append(max(current_money, shares * stock_price))
        #print(i, bought)
    current_money = max(current_money, shares * stock_price)
    return [shares, plot]


def main():
    money = 3
    volitality = 0.005
    prices = create_prices(money, volitality, 10)

    symbol = "AAPL"  # Replace with your desired stock symbol
    date = datetime.now().date()
    #prices = test_prices(symbol, date)

    #money = prices[0]
    bot = stock_bot(prices, 1)

    money = bot[0]
    print(money)
    
    # Plot the stock prices
    plt.plot(range(1, len(prices) + 1), prices, color='blue')
    plt.plot(range(1, len(prices) + 1), bot[1], color='red')
    plt.plot
    plt.title('Stock Prices')
    plt.xlabel('Minutes')
    plt.ylabel('Price ($)')
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()
