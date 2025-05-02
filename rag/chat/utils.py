import PyPDF2


def extract_text_from_pdf(file_path):
    text = ""
    try:
        reader = PyPDF2.PdfReader(file_path)
        for page in reader.pages:
            text += page.extract_text() or ""
    except Exception as e:
        print("error in reading pdf file")
    return text
