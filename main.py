import yfinance as yf
from datetime import datetime, timedelta

# Define the ticker symbol
ticker = "AAPL"

# Fetch data for the last year
end_date = datetime.today()
start_date = end_date - timedelta(days=365)

# Download the stock data
data = yf.download(ticker, start=start_date, end=end_date)

# Calculate additional metrics with rounding
last_close = round(data['Close'].iloc[-1], 2)
annual_high = round(data['High'].max(), 2)
annual_low = round(data['Low'].min(), 2)
average_volume = round(data['Volume'].mean(), 2)
most_recent_price = round(data['Close'].iloc[-1], 2)
most_recent_volume = round(data['Volume'].iloc[-1], 2)

# Fetch additional info
ticker_info = yf.Ticker(ticker)
# Make sure to check if these keys exist and have non-null values before accessing them
dividend_yield = round(ticker_info.info.get('dividendYield', 0) * 100, 2)  # Assuming it's provided as a fraction, convert to percentage
pe_ratio = round(ticker_info.info.get('trailingPE', 0), 2)
eps = round(ticker_info.info.get('trailingEps', 0), 2)
market_cap = round(ticker_info.info.get('marketCap', 0), 2)
beta = round(ticker_info.info.get('beta', 0), 2)

# Prepare the enhanced financial summary with rounded values
summary_text = f"""Enhanced Financial Summary for {ticker}
Ticker: {ticker}
Last Close: {last_close}
Annual High: {annual_high}
Annual Low: {annual_low}
Average Volume: {average_volume}
Most Recent Price: {most_recent_price}
Most Recent Volume: {most_recent_volume}
Dividend Yield: {dividend_yield}%
P/E Ratio: {pe_ratio}
EPS: {eps}
Market Cap: {market_cap}
Beta: {beta}
"""

# Save the summary to a .txt file
file_path_txt = 'enhanced_financial_summary_aapl.txt'
with open(file_path_txt, 'w') as txt_file:
    txt_file.write(summary_text)
