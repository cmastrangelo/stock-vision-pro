from django.shortcuts import render
from soozhub_app.gemini_handler import Gemini
from soozhub_app.yfinance_query import download_yfinance_data, analyse_data
from django.http import JsonResponse
# Create your views here.
import requests


def form_view(request):
    return render(request, 'soozhub_app/index.html', {})


def submit_view(request):
    print('WE IN BROTHA')
    if request.method == 'POST':
        stock_symbol = request.POST["stock_symbol"]
        print(stock_symbol)

    gemini = Gemini()

    data = download_yfinance_data('AAPL')
    crunched_data = analyse_data(data, 'AAPL')

    response = gemini.get_response(crunched_data,
                                   " Your task is to evaluate a specific stock. Begin with a 'summary' providing a concise overview, including its current price, market cap, and a brief on its recent performance. Then, move on to 'financial_health', where you will analyze key metrics such as the Debt to Equity ratio, Current ratio, Earnings per Share (EPS), and the Price to Earnings (P/E) ratio to gauge the company's financial stability and profitability. Next, assess the 'growth_potential' by evaluating indicators like Revenue growth year-over-year, Earnings growth projections, and any signs of market expansion or product innovation. Address 'risks' by considering factors such as market volatility, regulatory changes, and the intensity of competition. Conduct a 'sector_analysis' to provide an overview of the sector or industry, including trends, challenges, and growth outlook, and identify major competitors, comparing the company's performance and position relative to them. Finally, offer a 'recommendation' based on your analysis. You should decide whether to Buy, Hold, or Sell, providing a justification for your recommendation. This comprehensive evaluation will help users make informed investment decisions.")

    # Print the response and how long it took to get it
    print(response)

    # Perform your processing to generate the Markup string
    markup_response = response

    # Return a JsonResponse with the Markup string
    return JsonResponse({'markup': markup_response})
