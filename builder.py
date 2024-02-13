import yfinance as yf

# Define the ticker symbol
ticker_symbol = "AAPL"
ticker = yf.Ticker(ticker_symbol)

# Fetch the company info
info = ticker.info

# Extract sector and industry
sector = info.get('sector', 'N/A')
industry = info.get('industry', 'N/A')

print(f"Sector: {sector}")
print(f"Industry: {industry}")
