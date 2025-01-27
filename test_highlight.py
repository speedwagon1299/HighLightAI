import pytest
import os
from src.highlight import (  # Replace `your_module_name` with the actual filename without `.py`
    extract_text_from_pdf,
    split_text_to_fit_token_limit,
    highlight_pdf,
)

test_pdf_path = "../Papers/Tester/test.pdf"  # Use a small dummy PDF file for testing
output_pdf_path = "../Papers/Tester/test_highlighted.pdf"  # Output path for highlighted PDF

# Fixtures for setup
@pytest.fixture
def setup_test_environment(tmpdir):
    """
    Sets up a temporary directory with a small test PDF file for testing.
    """
    # Create a dummy PDF for testing
    dummy_pdf_content = """
    This is a test PDF file.
    It contains some text that we can use to test the highlight functionality.
    A is for Apple.
    B is for Banana.
    C is for Cherry.
    D is for Dragonfruit.
    E is for Elderberry.
    F is for Fig.
    G is for Grape.
    H is for Honeydew.
    I is for Ice Cream.
    J is for Jackfruit.
    K is for Kiwi.
    L is for Lemon.
    M is for Massive
    LOW TAPER FADEEEEE
    """ 
    dummy_pdf_path = os.path.join(tmpdir, "test.pdf")
    with open(dummy_pdf_path, "wb") as f:
        from reportlab.pdfgen import canvas

        c = canvas.Canvas(f)
        c.drawString(100, 750, dummy_pdf_content)
        c.save()
    return dummy_pdf_path

def test_extract_text_from_pdf(setup_test_environment):
    """
    Test for extracting text from a PDF without raising exceptions.
    """
    pdf_path = setup_test_environment
    try:
        text = extract_text_from_pdf(pdf_path)
        assert isinstance(text, str)
    except Exception as e:
        pytest.fail(f"Exception occurred during extract_text_from_pdf: {e}")

def test_split_text_to_fit_token_limit():
    """
    Test for splitting text into token chunks without raising exceptions.
    """
    text = "This is a test. " * 500
    try:
        chunks = split_text_to_fit_token_limit(text, max_tokens=50)
        assert isinstance(chunks, list)
        assert all(isinstance(chunk, str) for chunk in chunks)
    except Exception as e:
        pytest.fail(f"Exception occurred during split_text_to_fit_token_limit: {e}")

def test_highlight_pdf(setup_test_environment):
    """
    Test for adding highlights to a PDF without raising exceptions.
    """
    pdf_path = setup_test_environment
    output_path = pdf_path.replace(".pdf", "_highlighted.pdf")
    highlights = ["test", "PDF"]
    try:
        highlight_pdf(pdf_path, output_path, highlights)
        assert os.path.exists(output_path)
    except Exception as e:
        pytest.fail(f"Exception occurred during highlight_pdf: {e}")

# Run tests
if __name__ == "__main__":
    pytest.main(["-v", __file__])
