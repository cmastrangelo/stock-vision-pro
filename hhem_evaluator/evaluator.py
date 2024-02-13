from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import numpy as np
from gemini_integration import create_gemini_model_instance, get_response
from yfinance_query import download_yfinance_data, analyse_data


model = AutoModelForSequenceClassification.from_pretrained('vectara/hallucination_evaluation_model')
tokenizer = AutoTokenizer.from_pretrained('vectara/hallucination_evaluation_model')


def evaluate_performance(pairs):
    inputs = tokenizer.batch_encode_plus(pairs, return_tensors='pt', padding=True)

    model.eval()
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits.cpu().detach().numpy()
        # convert logits to probabilities
        scores = 1 / (1 + np.exp(-logits)).flatten()
        # Set print options
        np.set_printoptions(precision=8, suppress=True)

        print(scores)
        print("Average Score:", np.mean(scores))
        return np.mean(scores)


def full_evaluator():
    symbols = ['AAPL', 'WPC', 'TSLA', 'MSFT', 'GOOGL', 'AMZN', 'NFLX', 'NVDA', 'PYPL', 'ADBE', 'INTC', 'CSCO', 'CMCSA',
               'PEP', 'COST', 'TMUS', 'AVGO', 'TXN', 'QCOM', 'SBUX', 'INTU', 'AMD', 'ISRG', 'MU', 'AMAT', 'ADP', 'LRCX',
               'GILD', 'BIIB', 'REGN', 'VRTX', 'ILMN', 'IDXX', 'DXCM', 'ALGN', 'SNPS', 'CDNS', 'MELI', 'ASML', 'ANSS',
               'SPLK', 'DOCU', 'PTON', 'OKTA', 'ZM', 'CRWD', 'TWLO', 'FSLY', 'NET', 'DDOG', 'BILL', 'ZS', 'PINS', 'MDB',
               'ESTC', 'NOW', 'SPLK']  # Repeated 'SPLK', you might want to check if this is intentional

    # Initialize a dictionary to hold the data for each symbol
    data_dict = {}

    # Download and store data for each symbol
    for symbol in symbols:
        data_dict[symbol] = download_yfinance_data(symbol)

    llm_models = [create_gemini_model_instance()]
    instruction_set = "Your response should be in json format. Response should contain the following fields: 'summary', 'positive_aspects' (list of positive aspects for stock), 'negative_aspects' (list of negative aspects for stock), 'competitors' (major players in sector/industry)."

    evaluation_results = []

    for symbol in symbols:
        crunched_data = analyse_data(data_dict[symbol], symbol)  # Use the pre-downloaded data

        response = get_response(llm_models[0], crunched_data, instruction_set)

        pairs = [[crunched_data, response]]

        evaluation_results.append(evaluate_performance(pairs))

    # Calculate and print the average performance
    average_performance = sum(evaluation_results) / len(evaluation_results)
    print(round(average_performance, 7))


if __name__ == '__main__':
    full_evaluator()
