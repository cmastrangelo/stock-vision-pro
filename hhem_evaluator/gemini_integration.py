import textwrap
import google.generativeai as genai
from IPython.display import Markdown


def to_markdown(text):
    text = text.replace('•', '  *')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))


def create_gemini_model_instance():
    genai.configure(api_key='AIzaSyCdUu2kedN8CtuJyGiNwkmVzTTc-J8suaI')

    return genai.GenerativeModel('gemini-pro')


def get_response(model, data, instruction_set):
    response = model.generate_content("Data to be used to make decisions:" + data + instruction_set)
    return response.text
