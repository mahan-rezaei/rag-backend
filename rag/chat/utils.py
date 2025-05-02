import PyPDF2, pdfplumber
from hazm import SentenceTokenizer, Normalizer
from sentence_transformers import SentenceTransformer
import chromadb


normalizer = Normalizer()
sent_tokenizer = SentenceTokenizer()
embbeding_model = SentenceTransformer("HooshvareLab/bert-fa-base-uncased")

chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection("pdf_chunks")


def extract_text_from_pdf(file_path):
    full_text = ""
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    full_text += text + "\n"
    except Exception as e:
        print("error in reading pdf file")
    return text
