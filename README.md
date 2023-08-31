# Stock Valuator: DCF Analysis and Trading Signals

## Table of Contents
1. [Introduction](#introduction)
2. [Features](#features)
3. [Installation](#installation)
4. [Usage](#usage)
5. [API Endpoints](#api-endpoints)
6. [Code Overview](#code-overview)
7. [Contributing](#contributing)
8. [License](#license)

---

## Introduction

This stock valuator is a Python web application that uses Flask to offer an API endpoint for Discounted Cash Flow (DCF) analysis. The application evaluates a given stock ticker to determine whether it's overvalued, undervalued, or fairly valued based on financial data fetched from Yahoo Finance.

---

## Features

- **DCF Analysis**: Performs DCF analysis using data like risk-free rate, cost of equity, and free cash flows.
- **WACC Calculation**: Computes the Weighted Average Cost of Capital.
- **Terminal Value**: Estimates the terminal value of the stock.
- **Trade Signal**: Provides trading signals based on the DCF evaluation (Buy, Sell, or Hold).
- **Flask API**: Offers a RESTful API endpoint to fetch valuation.
- **Web Interface**: Simple web front-end for user input and output display.

---

## Installation

1. **Clone the Repository**
    ```bash
    git clone https://github.com/kyungphillee/kyungphilleestockvaluator.git
    ```

2. **Install Required Packages**
    ```bash
    pip install -r requirements.txt
    ```

3. **Run the Application**
    ```bash
    python app.py
    ```

---

## Usage

- **Web Interface**: Navigate to `http://127.0.0.1:5000/` and enter the stock ticker. Click on "Get Valuation" to see the result.
- **API Endpoint**: To get the valuation of a stock ticker, use the API endpoint `/api/valuation?ticker=<ticker>`.

---

## API Endpoints

| Endpoint              | Description                      |
| --------------------- | -------------------------------- |
| `GET /api/valuation`  | Returns the valuation of a stock |

Example:

```bash
GET /api/valuation?ticker=AAPL
```

---

## Code Overview

- `fetch_stock_data`: Fetches necessary stock data from Yahoo Finance.
- `discount_rate`: Calculates the discount rate based on equity, debt, and taxes.
- `cost_of_equity`: Computes the cost of equity.
- `get_FCF`: Gets the Free Cash Flow for the stock.
- `Terminal_Value`: Calculates the Terminal Value.
- `DCF`: Main function that performs the DCF analysis.
- `trade`: Provides a trade recommendation based on the valuation.

---

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

---

For more details on the implementation and potential improvements, refer to inline comments in the code. Pull requests are welcome.

*Disclaimer: This application is for educational purposes only. Please do your own due diligence before making any investment decisions.*
