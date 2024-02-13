import textwrap
import google.generativeai as genai
from IPython.display import Markdown
import time
import random
from google.api_core.exceptions import InternalServerError


def to_markdown(text):
    text = text.replace('•', '  *')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))


class Gemini:
    def __init__(self):
        genai.configure(api_key='AIzaSyCdUu2kedN8CtuJyGiNwkmVzTTc-J8suaI')
        self.model = genai.GenerativeModel('gemini-pro')

    def get_response(self, data, instruction_set, max_retries=3, initial_wait=2):
        retry_count = 0
        while retry_count < max_retries:
            try:
                response = self.model.generate_content("Data to be used to make decisions:" + data + instruction_set)
                return response.text
            except InternalServerError as e:
                print(f"Caught InternalServerError, retrying... (Attempt {retry_count + 1}/{max_retries})")
                time.sleep(initial_wait * 2 ** retry_count + random.uniform(0, 1))  # Exponential backoff + jitter
                retry_count += 1
            except ValueError as e:
                # Handle the specific ValueError for non-simple text responses as previously discussed
                if "The `response.text` quick accessor only works for simple" in str(e):
                    print("Caught ValueError for non-simple text response. Attempting to process complex response...")
                    # Here, add your logic to handle complex responses
                    break
                else:
                    raise  # Re-raise the exception if it's not the specific error we're handling
        raise Exception("Max retries reached. Unable to get a valid response.")
