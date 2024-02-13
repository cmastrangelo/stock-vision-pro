from django.shortcuts import render
from soozhub_app.gemini_handler import Gemini
from soozhub_app.yfinance_query import download_yfinance_data, analyse_data
from django.http import JsonResponse
# Create your views here.
import requests


def markdown_to_html(markdown_text):
    import re
    # This regex finds all occurrences of text enclosed in **, including the ** markers
    bold_pattern = re.compile(r'\*\*(.*?)\*\*')

    # Function to wrap matched text with <strong> tags, excluding the ** markers
    def replace_with_strong(match):
        return f'<strong>{match.group(1)}</strong>'

    # Replace all occurrences of **text** with <strong>text</strong>
    html_text = re.sub(bold_pattern, replace_with_strong, markdown_text)

    # Convert newlines to <br> for HTML
    html_text = html_text.replace("\n", "<br>")

    return html_text


def form_view(request):
    return render(request, 'soozhub_app/index.html', {})


def submit_view(request):
    if request.method == 'POST':
        stock_symbol = request.POST.get("stock_symbol", "")

        try:
            # Attempt to download and analyze stock data
            data = download_yfinance_data(stock_symbol)
            crunched_data = analyse_data(data, stock_symbol)
        except Exception as e:
            # Generate HTML markup for the data download/analysis error message
            error_message = "<p>There was an error downloading stock data, please make sure the stock symbol exists.</p>"
            return JsonResponse({'markup': error_message})

        try:
            # Attempt to get the response from Gemini
            gemini = Gemini()
            response = gemini.get_response(crunched_data,
                                           "Your task is to evaluate a specific stock. Begin with a 'summary' providing a concise overview, including its current price, market cap, and a brief on its recent performance. Then, move on to 'financial_health', where you will analyze key metrics such as the Debt to Equity ratio, Current ratio, Earnings per Share (EPS), and the Price to Earnings (P/E) ratio to gauge the company's financial stability and profitability. Next, assess the 'growth_potential' by evaluating indicators like Revenue growth year-over-year, Earnings growth projections, and any signs of market expansion or product innovation. Address 'risks' by considering factors such as market volatility, regulatory changes, and the intensity of competition. Conduct a 'sector_analysis' to provide an overview of the sector or industry, including trends, challenges, and growth outlook, and identify major competitors, comparing the company's performance and position relative to them. Finally, offer a 'recommendation' based on your analysis. You should decide whether to Buy, Hold, or Sell, providing a justification for your recommendation. This comprehensive evaluation will help users make informed investment decisions.")
            # Convert markdown-style bold to HTML
            markup_response = markdown_to_html(response)
        except Exception as e:
            # Generate HTML markup for the Gemini communication error message
            error_message = "<p>There was an error communicating with Gemini, please retry.</p>"
            return JsonResponse({'markup': error_message})

        return JsonResponse({'markup': markup_response})
