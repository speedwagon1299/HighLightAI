import openai
import PyPDF2
import fitz 
from transformers import GPT2TokenizerFast

def extract_important_points(text):
    """
    Extracts important points from the text using the OpenAI Chat API.
    
    Inputs:
    - text: The text to process.

    Returns:
    - important_points: The important points extracted from the text.
    """
    
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": """
                    Provide the important points in the text such that
                    it can be used by a program to highlight the essential 
                    points in the research paper. Do not change the capitalization of the text,
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
    Splits into tokens of 3500 to ensure context is not lost

    Inputs:
    - text: The text to split.

    Returns:
    - text_chunks: List of text chunks.
    """
    tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")
    tokens = tokenizer.encode(text)
    chunks = [tokens[i:i + max_tokens] for i in range(0, len(tokens), max_tokens)]
    text_chunks = [tokenizer.decode(chunk) for chunk in chunks]
    return text_chunks

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF file using PyPDF2

    Inputs:
    - pdf_path: Path to the PDF file.
    
    Returns:
    - extracted_text: Extracted text as a single string.
    """

    extracted_text = ""
    with open(pdf_path, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            extracted_text += page.extract_text() + "\n" 
    return extracted_text

def highlight_pdf(input_pdf, output_pdf, highlights):
    """
    Highlights text in a PDF using PyMuPDF.

    Inputs:
    - input_pdf: Path to the input PDF file.
    - output_pdf: Path to save the output PDF file.
    - highlights: List of text strings to highlight.

    Returns:
    - None
    """
    doc = fitz.open(input_pdf)

    for page_num in range(len(doc)):
        page = doc[page_num]
        
        for term in highlights:
            instances = page.search_for(term)
            
            for inst in instances:
                highlight = page.add_highlight_annot(inst)
                highlight.update()
    
    doc.save(output_pdf)
