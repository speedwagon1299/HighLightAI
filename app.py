import streamlit as st
from src.highlight import extract_text_from_pdf, split_text_to_fit_token_limit, extract_important_points, highlight_pdf
import os
import ast
import openai
import tempfile

openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="PDF Highlighter", layout="centered", initial_sidebar_state="expanded")

st.title("📚 AI-Powered PDF Highlighter")
st.write("Upload a PDF, and this tool will highlight important points for you!")

uploaded_pdf = st.file_uploader("Upload your PDF file", type=["pdf"])
if uploaded_pdf:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
        tmp_pdf.write(uploaded_pdf.read())
        pdf_path = tmp_pdf.name

    # Extract text
    st.write("🔄 Extracting text from the PDF...")
    text = extract_text_from_pdf(pdf_path)
    st.success("Text extracted successfully!")

    # Split into chunks
    st.write("📝 Splitting text to fit token limits...")
    text_chunks = split_text_to_fit_token_limit(text, max_tokens=2000)
    st.success(f"Split into {len(text_chunks)} chunks.")

    # Extract important points
    st.write("✨ Extracting important points from the text...")
    sentences = []
    for chunk in text_chunks:
        important_points = extract_important_points(chunk) 
        sentences.extend(ast.literal_eval(important_points))
    st.success("Important points extracted!")

    # Highlight PDF
    st.write("💡 Highlighting important points in the PDF...")
    output_pdf_path = pdf_path.replace(".pdf", "_highlighted.pdf")
    highlight_pdf(pdf_path, output_pdf_path, sentences)
    st.success("PDF annotated successfully!")

    # Provide download link
    with open(output_pdf_path, "rb") as f:
        st.download_button(
            label="📥 Download Highlighted PDF",
            data=f,
            file_name="highlighted.pdf",
            mime="application/pdf",
        )
