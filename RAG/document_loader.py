from pypdf import PdfReader


def load_pdf(pdf_path):
    """
    Extract text from every page of the PDF.

    Returns:
        list: A list containing the text of each page.
    """

    reader = PdfReader(str(pdf_path))

    pages = []

    for page in reader.pages:
        text = page.extract_text()

        if text:
            pages.append(text)
        else:
            pages.append("")

    return pages