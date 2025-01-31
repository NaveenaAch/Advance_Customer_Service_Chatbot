import pdfplumber

def load_pdf(file_path):
    """
    Function to load and extract text from a PDF file.
    
    Args:
    - file_path (str): Path to the PDF file.

    Returns:
    - str: Extracted text from the PDF file.
    """
    with pdfplumber.open(file_path) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text()
    return text