import fitz
def extract_text_from_pdf(file_path:str) -> str:
    """this will open a pdf and extratct all the text page by page. Return one combined string with page markers."""
    doc = fitz.open(file_path)
    full_text = ""
    for page_num, page in enumerate(doc, start = 1):
        text = page.get_text()
        full_text += f"\n--- Page {page_num} ---\n{text}"
    doc.close()
    return full_text