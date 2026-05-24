from io import BytesIO
from pypdf import PdfReader

class PDFExtractionError(Exception):
    """Raised when the PDF cannot be read or has no extractable text."""

def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    MSG = "Could not extract text from the PDF. The file may be corrupted or image-only."

    try:
        reader = PdfReader(BytesIO(pdf_bytes))
        parts = []
        for page in reader.pages:
            text = page.extract_text()
            if text:
                parts.append(text)
        full_text = "\n".join(parts).strip()
    except Exception as e:
        raise PDFExtractionError(MSG) from e
    
    if not full_text:
        raise PDFExtractionError(MSG)
    
    return full_text