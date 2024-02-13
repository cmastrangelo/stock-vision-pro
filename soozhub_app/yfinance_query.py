import yfinance as yf
import pandas as pd


def download_yfinance_data(symbol):
    print('downloading data for', symbol)
    # Download the stock data since its inception (no start date specified)
    market_data = yf.download(symbol)

    # Fetch additional info (as before)
    ticker_info = yf.Ticker(symbol)
    sector = ticker_info.info.get('sector', 'N/A')
    industry = ticker_info.info.get('industry', 'N/A')
    dividend_yield = round(ticker_info.info.get('dividendYield', 0) * 100, 2)
    pe_ratio = round(ticker_info.info.get('trailingPE', 0), 2)
    eps = round(ticker_info.info.get('trailingEps', 0), 2)
    market_cap = round(ticker_info.info.get('marketCap', 0), 2)
    beta = round(ticker_info.info.get('beta', 0), 2)

    data = {
        'sector': sector,
        'industry': industry,
        'market_data': market_data,
        'dividend_yield': dividend_yield,
        'pe_ratio': pe_ratio,
        'eps': eps,
        'market_cap': market_cap,
        'beta': beta
    }
    return data


def analyse_data(data, symbol):
    # Calculate additional metrics with rounding
    all_time_high = round(data['market_data']['High'].max(), 2)
    all_time_low = round(data['market_data']['Low'].min(), 2)

    # For year high and year low, filter data for the last year
    end_date = data['market_data'].index.max()  # Use the last available date in the dataset
    start_date = end_date - pd.Timedelta(days=365)
    last_year_data = data['market_data'].loc[start_date:end_date]

    year_high = round(last_year_data['High'].max(), 2)
    year_low = round(last_year_data['Low'].min(), 2)

    # Continue with previous calculations for most recent metrics
    last_close = round(data['market_data']['Close'].iloc[-1], 2)
    average_volume = round(data['market_data']['Volume'].mean(), 2)
    most_recent_price = round(data['market_data']['Close'].iloc[-1], 2)
    most_recent_volume = round(data['market_data']['Volume'].iloc[-1], 2)

    # Update the summary to include all-time and last year metrics
    summary_text = f"""Financial Summary for {symbol}
    Ticker: {symbol}
    Sector: {data['sector']}
    Industry: {data['industry']}
    Last Close: {last_close}
    All-Time High: {all_time_high}
    All-Time Low: {all_time_low}
    Year High (Last 365 Days): {year_high}
    Year Low (Last 365 Days): {year_low}
    Average Volume: {average_volume}
    Most Recent Price: {most_recent_price}
    Most Recent Volume: {most_recent_volume}
    Dividend Yield: {data['dividend_yield']}%
    P/E Ratio: {data['pe_ratio']}
    EPS: {data['eps']}
    Market Cap: {data['market_cap']}
    Beta: {data['beta']}
    """
    return summary_text
