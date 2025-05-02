from chat.utils import store_pdf_to_chromaDB
import os


def initialize_chroma_from_pdf():
    file_path = "rag/files/farsi-11.pdf"
    result = store_pdf_to_chromaDB(file_path)
    print(result)
