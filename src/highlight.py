import openai
import PyPDF2
import fitz
from transformers import GPT2TokenizerFast
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from io import BytesIO
import streamlit as st
from fuzzywuzzy import fuzz
import re

def extract_important_points(text):
    try:

        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": """
                    Provide the important points in the text such that
                    it can be used by a program to highlight the essential
                    points in the research paper. Do not mark general points,
                    focus on key points of the text.
                    Do not change the capitalization of the text,
                    only take the exact sentences and represent it in the form
                    ["sentence_1", "sentence_2",..., "sentence_n"]
                """},
                {"role": "user", "content": text}
            ],
        )

        important_points = response.choices[0].message.content
        return important_points.strip()
    except Exception as e:
        return f"An error occurred: {e}"

def split_text_to_fit_token_limit(text, max_tokens=3500):
    """
    Splits text into chunks that fit within the token limit for the OpenAI API.

    Inputs:
    - text: The text to split.
    - max_tokens: The maximum number of tokens allowed in a chunk.

    Returns:
    - text_chunks: List of text chunks.
    """
    tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")
    tokens = tokenizer.encode(text)
    chunks = [tokens[i:i + max_tokens] for i in range(0, len(tokens), max_tokens)]
    text_chunks = [tokenizer.decode(chunk) for chunk in chunks]
    return text_chunks

# def extract_text_from_pdf(pdf_path):
#     """
#     Extracts text from a PDF file using PyPDF2.

#     Inputs:
#     - pdf_path: Path to the PDF file.

#     Returns:
#     - extracted_text: Extracted text as a single string.
#     """
#     extracted_text = ""
#     try:
#         with open(pdf_path, "rb") as file:
#             pdf_reader = PyPDF2.PdfReader(file)
#             for page in pdf_reader.pages:
#                 text = page.extract_text()
#                 if text:
#                     extracted_text += text + "\n"
#     except Exception as e:
#         raise RuntimeError(f"Error extracting text from PDF: {e}")
#     return extracted_text.strip()

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF file using PyPDF2, stopping when the exact section 'References' is encountered.

    Inputs:
    - pdf_path: Path to the PDF file.

    Returns:
    - extracted_text: Extracted text before the 'References' section as a single string.
    """
    extracted_text = ""
    references_pattern = re.compile(r"^\s*References\s*$", re.IGNORECASE)  # Matches "References" as a standalone heading
    
    try:
        with open(pdf_path, "rb") as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text = page.extract_text()
                if text:
                    lines = text.splitlines()
                    for line in lines:
                        if references_pattern.match(line):  # Check if the line is exactly "References"
                            return extracted_text.strip()  # Stop extraction and return collected text
                        extracted_text += line + "\n"
    except Exception as e:
        raise RuntimeError(f"Error extracting text from PDF: {e}")
    
    return extracted_text.strip()


def highlight_pdf(input_pdf, output_pdf, sentences):
    """
    Highlights important sentences in the PDF using PyMuPDF (fitz).
    
    Optimized to handle large PDFs and minimize blocking in Streamlit.
    
    Inputs:
    - input_pdf: Path to the input PDF file.
    - output_pdf: Path to save the output PDF file.
    - sentences: List of sentences to highlight.

    Returns:
    - None
    """
    try:
        doc = fitz.open(input_pdf)  # Open the input PDF

        # Iterate through each page
        for page_num in range(len(doc)):
            page = doc[page_num]
            
            # Provide Streamlit feedback for long operations
            st.write(f"Processing page {page_num + 1} of {len(doc)}...")
            
            # Search for each sentence on the page
            for sentence in sentences:
                instances = page.search_for(sentence)

                if instances:
                    for inst in instances:
                        # Add highlight annotations
                        highlight = page.add_highlight_annot(inst)
                        highlight.update()

        # Save the output PDF
        doc.save(output_pdf)
        doc.close()
        st.success(f"Highlighted PDF saved to: {output_pdf}")

    except Exception as e:
        st.error(f"Error in highlighting PDF: {e}")
        raise RuntimeError(f"Error in highlighting PDF: {e}")

# def highlight_pdf(input_pdf, output_pdf, sentences, threshold=85):
#     """
#     Highlights important sentences in the PDF using PyMuPDF (fitz) with fuzzy matching.
    
#     Optimized to handle large PDFs and minimize blocking in Streamlit.

#     Inputs:
#     - input_pdf: Path to the input PDF file.
#     - output_pdf: Path to save the output PDF file.
#     - sentences: List of sentences to highlight.
#     - threshold: Fuzzy matching threshold (default: 85).

#     Returns:
#     - None
#     """
#     try:
#         doc = fitz.open(input_pdf)  # Open the input PDF

#         # Iterate through each page
#         for page_num in range(len(doc)):
#             page = doc[page_num]
            
#             # Provide Streamlit feedback for long operations
#             st.write(f"Processing page {page_num + 1} of {len(doc)}...")

#             # Extract the text from the page
#             page_text = page.get_text("text")  # Extract raw text from the page
            
#             # Break the page text into lines for easier matching
#             page_lines = page_text.splitlines()

#             # Check each line for a fuzzy match to the sentences
#             for sentence in sentences:
#                 for line in page_lines:
#                     # Perform fuzzy matching
#                     match_ratio = fuzz.token_set_ratio(sentence, line)
#                     if match_ratio >= threshold:
#                         # Get bounding boxes for the matched text
#                         instances = page.search_for(line)

#                         if instances:
#                             for inst in instances:
#                                 # Add highlight annotations
#                                 highlight = page.add_highlight_annot(inst)
#                                 highlight.update()

#         # Save the output PDF
#         doc.save(output_pdf)
#         doc.close()
#         st.success(f"Highlighted PDF saved to: {output_pdf}")

#     except Exception as e:
#         st.error(f"An error occurred: {e}")