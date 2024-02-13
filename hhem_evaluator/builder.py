from gpt_4_turbo_handler import GPT4Turbo
from gemini_handler import Gemini
from yfinance_query import download_yfinance_data, analyse_data
import time

gpt4turbo = GPT4Turbo()
gemini = Gemini()

data = download_yfinance_data('AAPL')
crunched_data = analyse_data(data, 'AAPL')


# Record the start time
start_time = time.time()

response = gemini.get_response(crunched_data, " Your task is to evaluate a specific stock. Begin with a 'summary' providing a concise overview, including its current price, market cap, and a brief on its recent performance. Then, move on to 'financial_health', where you will analyze key metrics such as the Debt to Equity ratio, Current ratio, Earnings per Share (EPS), and the Price to Earnings (P/E) ratio to gauge the company's financial stability and profitability. Next, assess the 'growth_potential' by evaluating indicators like Revenue growth year-over-year, Earnings growth projections, and any signs of market expansion or product innovation. Address 'risks' by considering factors such as market volatility, regulatory changes, and the intensity of competition. Conduct a 'sector_analysis' to provide an overview of the sector or industry, including trends, challenges, and growth outlook, and identify major competitors, comparing the company's performance and position relative to them. Finally, offer a 'recommendation' based on your analysis. You should decide whether to Buy, Hold, or Sell, providing a justification for your recommendation. This comprehensive evaluation will help users make informed investment decisions.")

# Record the end time
end_time = time.time()

# Calculate the duration
duration = end_time - start_time

# Print the response and how long it took to get it
print(response)
print(f"Response time: {duration} seconds")