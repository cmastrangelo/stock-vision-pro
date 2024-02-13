import textwrap

import google.generativeai as genai

from IPython.display import Markdown
from main import download_yfinance_data, analyse_data
from evaluator import evaluate_performance


def to_markdown(text):
    text = text.replace('•', '  *')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))


genai.configure(api_key='AIzaSyCdUu2kedN8CtuJyGiNwkmVzTTc-J8suaI')

model = genai.GenerativeModel('gemini-pro')

symbols = ['AAPL', 'WPC', 'TSLA', 'MSFT', 'GOOGL', 'AMZN', 'NFLX', 'NVDA', 'PYPL', 'ADBE', 'INTC', 'CSCO', 'CMCSA', 'PEP', 'COST', 'TMUS', 'AVGO', 'TXN', 'QCOM', 'SBUX', 'INTU', 'AMD', 'ISRG', 'MU', 'AMAT', 'ADP', 'LRCX', 'GILD', 'BIIB', 'REGN', 'VRTX', 'ILMN', 'IDXX', 'DXCM', 'ALGN', 'SNPS', 'CDNS', 'MELI', 'ASML', 'ANSS', 'SPLK', 'DOCU', 'PTON', 'OKTA', 'ZM', 'CRWD', 'TWLO', 'FSLY', 'NET', 'DDOG', 'BILL', 'ZS', 'PINS', 'MDB', 'ESTC', 'NOW', 'SPLK']

evaluation_results = []
for symbol in symbols:
    data = download_yfinance_data(symbol)
    crunched_data = analyse_data(data, symbol)
    # print(crunched_data)

    response = model.generate_content("Data to be used to make decisions:" + crunched_data + "Your response should be in json format. Response should contain the following fields: 'summary':, 'positives_aspects': [(list of positive aspects for stock)], 'negative_aspects': [(list of positive aspects for stock)], competitors: [(major players in that sector)]")

    # print(response.text)

    pairs = [[crunched_data, response.text]]

    evaluation_results.append(evaluate_performance(pairs))

print(evaluation_results)
print(sum(evaluation_results))
print(len(evaluation_results))
print(round(sum(evaluation_results) / len(evaluation_results), 7))
