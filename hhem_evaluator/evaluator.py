from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import numpy as np
from gemini_handler import Gemini
from gpt_4_turbo_handler import GPT4Turbo
from yfinance_query import download_yfinance_data, analyse_data
import json
from tqdm import tqdm
from tabulate import tabulate


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

        return np.mean(scores)


def load_and_prepare_data():
    symbols = ['AAPL', 'WPC', 'TSLA', 'MSFT', 'GOOGL', 'AMZN', 'NFLX', 'NVDA', 'PYPL', 'ADBE', 'INTC', 'CSCO', 'CMCSA',
               'PEP', 'COST', 'TMUS', 'AVGO', 'TXN', 'QCOM', 'SBUX', 'INTU', 'AMD', 'ISRG', 'MU', 'AMAT', 'ADP', 'LRCX',
               'GILD', 'BIIB', 'REGN', 'VRTX', 'ILMN', 'IDXX', 'DXCM', 'ALGN', 'SNPS', 'CDNS', 'MELI', 'ASML', 'ANSS',
               'SPLK', 'DOCU', 'PTON', 'OKTA', 'ZM', 'CRWD', 'TWLO', 'FSLY', 'NET', 'DDOG', 'BILL', 'ZS', 'PINS', 'MDB',
               'ESTC', 'NOW']

    # Load instruction sets from JSON
    with open('instruction_sets.json', 'r') as file:
        instruction_sets = json.load(file)

    # Initialize a dictionary to hold the data for each symbol
    data_dict = {}
    for symbol in symbols:
        data_dict[symbol] = download_yfinance_data(symbol)

    return data_dict, instruction_sets


def perform_evaluations(data_dict, instruction_sets):
    gemini = Gemini()
    gpt4turbo = GPT4Turbo()
    llm_models = [("Gemini", gemini), ("GPT4Turbo", gpt4turbo)]
    results = []
    model_scores = {model_name: [] for model_name, _ in llm_models}
    instruction_set_scores = {version: [] for version in instruction_sets}

    total_iterations = len(llm_models) * len(instruction_sets) * len(data_dict)
    with tqdm(total=total_iterations, desc="Evaluating", unit="iteration") as pbar:
        for model_name, model in llm_models:
            for version, instruction_set in instruction_sets.items():
                for symbol, data in data_dict.items():
                    crunched_data = analyse_data(data, symbol)
                    response = model.get_response(crunched_data, instruction_set)
                    pairs = [[crunched_data, response]]
                    score = evaluate_performance(pairs)
                    results.append({"Model": model_name, "Instruction Set": version, "Score": score})
                    model_scores[model_name].append(score)
                    instruction_set_scores[version].append(score)
                    pbar.update(1)  # Update progress bar

    # Sort results by Score in descending order
    sorted_results = sorted(results, key=lambda x: x['Score'], reverse=True)

    # Calculate averages for each model
    for model_name in model_scores:
        avg_score = sum(model_scores[model_name]) / len(model_scores[model_name])
        print(f"Average for {model_name}: {round(avg_score, 7)}")

    # Calculate averages for each instruction set
    for version in instruction_set_scores:
        avg_score = sum(instruction_set_scores[version]) / len(instruction_set_scores[version])
        print(f"Average for Instruction Set {version}: {round(avg_score, 7)}")

    # Tabulate results
    print(tabulate(sorted_results, headers="keys", tablefmt="grid"))


if __name__ == '__main__':
    data_dict, instruction_sets = load_and_prepare_data()
    perform_evaluations(data_dict, instruction_sets)
