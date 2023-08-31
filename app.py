from datetime import datetime
import yfinance as yf
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Pre-fetch treasury yield and market data
treasury_ticker = yf.Ticker('^TNX')
market_ticker = yf.Ticker('^GSPC')
risk_free_rate = treasury_ticker.history(period='max')['Close'].iloc[-1] / 100
market_history = market_ticker.history(period='max')['Close']

# Function to fetch shared data for a stock


def fetch_stock_data(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info
    financials = stock.financials
    income_statement = stock.income_stmt
    balance_sheet = stock.balance_sheet
    cash_flow = stock.cash_flow
    dividends = stock.dividends
    return info, financials, income_statement, balance_sheet, cash_flow, dividends

# Function to calculate discount rate


def discount_rate(stock_data):
    info, financials, _, balance_sheet, _, _ = stock_data
    E = info['marketCap']
    D = balance_sheet.loc['Total Debt'].iloc[-1]
    V = E + D
    Tc = 0.21

    Interest_Expense = financials.loc['Interest Expense'].iloc[0]
    Rd = Interest_Expense / D * (1 - Tc)

    Re = cost_of_equity(stock_data)

    return (E/V) * Re + (D/V) * Rd * (1-Tc)

# Function to calculate cost of equity


def cost_of_equity(stock_data):
    info, _, _, _, _, _ = stock_data
    Beta = info['beta']

    last_date = market_history.index[-1]
    start_date = last_date - pd.DateOffset(years=5)
    filtered_data = market_history[start_date:last_date]
    daily_change = filtered_data.pct_change().dropna()
    annualized_return = ((1 + daily_change.mean()) ** 252 - 1)

    return risk_free_rate + Beta * (annualized_return - risk_free_rate)

# Function to get Free Cash Flow


def get_FCF(stock_data):
    _, financials, _, _, cash_flow, _ = stock_data
    CFO = cash_flow.loc['Operating Cash Flow'].iloc[0]
    IE = financials.loc['Interest Expense'].iloc[0]
    CAPEX = cash_flow.loc['Capital Expenditure'].iloc[0]
    return CFO + IE * (1 - 0.21) - CAPEX

# Function to calculate Terminal Value


def Terminal_Value(stock_data):
    info, _, income_statement, balance_sheet, _, dividends = stock_data
    FCFF = get_FCF(stock_data)
    dividend_paid = dividends.iloc[-1] if not dividends.empty else 0
    net_income = income_statement.loc['Net Income'].iloc[0]
    retention_rate = 1 - dividend_paid / net_income

    debt = balance_sheet.loc['Total Debt'].iloc[0]
    equity = info['marketCap']
    ROIC = (net_income - dividend_paid) / (debt + equity)

    g = retention_rate * ROIC
    r = discount_rate(stock_data)

    return FCFF * (1 + g) / (r - g)

# Main DCF function


def DCF(ticker, forecast_period=5):
    stock_data = fetch_stock_data(ticker)
    WACC = discount_rate(stock_data)
    FCFFn = get_FCF(stock_data)
    TV = Terminal_Value(stock_data)
    PV_TV = TV / (1 + WACC) ** forecast_period

    PV_FCFF = sum(FCFFn / (1 + WACC) **
                  i for i in range(1, forecast_period + 1))

    EV = PV_TV + PV_FCFF
    info = stock_data[0]
    Implied_Share_Price = EV / info['sharesOutstanding']
    return Implied_Share_Price

# Function to determine valuation


def trade(stock: str, end_date: str = None):
    # Use current date if end_date is not provided
    if end_date is None:
        end_date = datetime.now().strftime('%Y-%m-%d')

    # if stock is not a valid ticker, return False
    if not yf.Ticker(stock).info:
        print('Invalid stock ticker. Try Again!')

    # Calculate valuated price using DCF method
    valuated_price = DCF(stock)
    if valuated_price is None:
        print('DCF calculation cannot be done.')

    # Download stock's adjusted close price
    try:
        current_price = yf.download(
            stock, start='2020-01-01', end=end_date)['Adj Close'].iloc[-1]
    except Exception as e:
        print(f"Failed to download stock data: {e}")

    # Truncate prices to the second decimal place
    truncated_current_price = np.trunc(current_price * 100) / 100
    truncated_valuated_price = np.trunc(valuated_price * 100) / 100

    # return a dictionary with the current price, valuated price, and valuation
    if truncated_current_price > truncated_valuated_price:
        return {"current_price": truncated_current_price, "valuated_price": truncated_valuated_price, "valuation": "overvalued. Sell it!"}
    elif truncated_current_price < truncated_valuated_price:
        return {"current_price": truncated_current_price, "valuated_price": truncated_valuated_price, "valuation": "undervalued. Buy it!"}
    else:
        return {"current_price": truncated_current_price, "valuated_price": truncated_valuated_price, "valuation": "fairly valued"}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/valuation', methods=['GET'])
def get_valuation():
    ticker = request.args.get('ticker')

    # Run your Python code to get the stock valuation
    # Replace this with your actual function
    valuation_result = trade(ticker)

    return jsonify(valuation_result)


if __name__ == '__main__':
    app.run(debug=True)
