# pdf_reader.py
# This file is responsible for one job only: reading a PDF and extracting its text.

# We import PdfReader from the PyPDF2 library.
# PdfReader is a class that knows how to open and read PDF files page by page.
from PyPDF2 import PdfReader


def extract_text_from_pdf(uploaded_file):
    """
    This function takes an uploaded PDF file and returns all the text inside it.

    Parameters:
        uploaded_file: This is the file object we get from Streamlit's file_uploader.

    Returns:
        A single string containing all the text from every page of the PDF.
    """

    # Step 1: Create a PdfReader object using the uploaded file.
    # This "opens" the PDF so we can read its pages.
    pdf_reader = PdfReader(uploaded_file)

    # Step 2: Create an empty string to store all extracted text.
    # We will keep adding text to this variable as we go through each page.
    extracted_text = ""

    # Step 3: Loop through every page in the PDF.
    # pdf_reader.pages is a list-like object containing all pages.
    for page in pdf_reader.pages:

        # Step 4: Extract text from the current page.
        # .extract_text() reads the visible text from that specific page.
        page_text = page.extract_text()

        # Step 5: Sometimes a page might have no text (e.g., it's an image).
        # In that case, extract_text() returns None. We check for that
        # to avoid errors when we try to add None to our string.
        if page_text:
            extracted_text += page_text + "\n"  # \n adds a new line between pages

    # Step 6: Return the final combined text from all pages.
    return extracted_text
