import json
import requests


'AIzaSyCdUu2kedN8CtuJyGiNwkmVzTTc-J8suaI'
api_key_header = {
    "customer-id": '3338800947',
    "x-api-key": 'zqt_xwIPMxkmF32BvT3ibQjIzvRMjGAF-ZiKEaCYJw'
}

data_dict = {
    "query": [
        {
            "query": "Give me a review of AAPL stock",
            "num_results": 10,
            "corpus_key": [
                {
                    "customer_id": '3338800947',
                    "corpus_id": '1'
                }
            ]
        }
    ]
}
payload = json.dumps(data_dict)
response = requests.post(
    "https://api.vectara.io/v1/query",
    data=payload,
    verify=True,
    headers=api_key_header)

# Assuming `response` is your JSON data as a string
response_data = json.loads(response.text)

# indented json data
print(json.dumps(response_data, indent=4))

# Navigate through the JSON structure to extract the text
response_texts = [resp['text'] for resp_set in response_data['responseSet'] for resp in resp_set['response']]

# Now `response_texts` contains all the response texts
for text in response_texts:
    print(text)
