from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import numpy as np

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
