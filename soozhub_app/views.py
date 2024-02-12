from django.shortcuts import render

# Create your views here.
import requests

def form_view(request):
    error_message = None
    if request.method == 'POST':
        stock_symbol = request.POST["stock_symbol"]
        timeframe = request.POST["timeframe"]
        print(stock_symbol)
        print(timeframe)
        result = stock_symbol + timeframe
        
        # response = requests.post('http://api.example.com/predict', json={'stock_symbol': stock_symbol})
        # if response.status_code == 200:
        #     result = response.json().get('result', '')
        # else:
        #     error_message = "Failed to get result from the AI model."
        #     result = None
    else:
        result = None
    return render(request, 'soozhub_app/index.html', {'result': result, 'error_message': error_message})