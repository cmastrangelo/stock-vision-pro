import yfinance as yf
import json

ticker = "AAPL"
data = yf.Ticker(ticker)
hist = data.history(period="1mo")

# Preparing data for Vectara format
vectara_data = {
  "documentId": ticker,
  "title": f"Financial Summary for {ticker}",
  "metadataJson": json.dumps({
    "ticker": ticker,
    "period": "1 month",
    "description": "A summary of financial performance for the ticker over the last month."
  }),
  "section": [
    {
      "title": "Monthly Performance",
      "text": f"Last Close: {hist.iloc[-1]['Close']}\nMonthly High: {hist['High'].max()}\nMonthly Low: {hist['Low'].min()}",
      "metadataJson": json.dumps({
        "last_close": hist.iloc[-1]['Close'].item(),
        "monthly_high": hist['High'].max().item(),
        "monthly_low": hist['Low'].min().item()
      })
    }
  ]
}

# Define the file path
file_path = 'vectara_financial_data.json'

# Dump vectara_data to a JSON file
with open(file_path, 'w') as json_file:
    json.dump(vectara_data, json_file, indent=4)
