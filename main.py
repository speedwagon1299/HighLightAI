import ast
from fuzzywuzzy import fuzz
import os
import openai
from src.highlight import (  
    extract_text_from_pdf,
    extract_important_points,
    split_text_to_fit_token_limit,
    highlight_pdf,
)

openai.api_key = os.environ.get("OPEN_API_KEY_SEC")
pdf_path = "Papers/TestText.pdf" # Path to the PDF file
output_pdf_path = pdf_path.split('.pdf')[0] + "_highlighted.pdf" # Path to save the highlighted PDF

text = extract_text_from_pdf(pdf_path)

text_chunks = split_text_to_fit_token_limit(text, max_tokens=3500)

sentences = []

for i, chunk in enumerate(text_chunks):
    important_points = extract_important_points(chunk)  # Replace with your processing logic
    sentences.extend(ast.literal_eval(important_points))

highlight_pdf(pdf_path, output_pdf_path, sentences)
