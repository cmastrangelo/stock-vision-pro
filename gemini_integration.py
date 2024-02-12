import pathlib
import textwrap

import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown


def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))


genai.configure(api_key='AIzaSyCdUu2kedN8CtuJyGiNwkmVzTTc-J8suaI')

model = genai.GenerativeModel('gemini-pro')

stock_data = "Financial Summary for AAPL\nTicker: AAPL\nLast Close: 188.85\nAnnual High: 199.62\nAnnual Low: 143.9\nAverage Volume: 57147076.8\nMost Recent Price: 188.85\nMost Recent Volume: 45099900\nDividend Yield: 0.51%\nP/E Ratio: 29.18\nEPS: 6.44\nMarket Cap: 2902150610944\nBeta: 1.31"

response = model.generate_content("Data to be used to make decisions:" + stock_data + "Your response should be in json format. Response should contain the following fields: 'summary':, 'sentiment': (positive, negative, neutral), 'positives aspects': [(list of positive aspects for stock)], 'negative aspects': [(list of positive aspects for stock)].")

print(response.text)
