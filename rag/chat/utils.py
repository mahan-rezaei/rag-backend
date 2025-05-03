import PyPDF2, pdfplumber
from hazm import SentenceTokenizer, Normalizer
from sentence_transformers import SentenceTransformer
import chromadb
from .models import Document

import os


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
        print(f"error in reading pdf file{str(e)}")
    return full_text

def proccess_text_to_sentences(text):
    norm_text = normalizer.normalize(text)
    sentenses = [sen for sen in norm_text.split(".")]
    print("*"*90)
    print("sentences")
    print(sentenses)
    return sentenses

def embed_sentences(sentences):
    return embbeding_model.encode(sentences).tolist()

def store_sentences_in_chromaDB(sentences):
    embeddings = embed_sentences(sentences)
    ids = [f"chunc{i}" for i in range(len(sentences))]
    collection.add(documents=sentences, embeddings=embeddings, ids=ids)

def store_pdf_to_chromaDB(file_path):
    file_name = os.path.basename(file_path)
    doc, created = Document.objects.get_or_create(file_name=file_name)

    text = extract_text_from_pdf(file_path)
    sentences = proccess_text_to_sentences(text)
    print("*"*90)
    print(sentences)
    store_sentences_in_chromaDB(sentences)

    print(f"{len(sentences)} sentences added to chromaDB")
    return len(sentences)

def search_in_chroma(question, top_k=7):
    query_embedding = embed_sentences(question)   
    result = collection.query(
        query_embeddings=[query_embedding],  
        n_results=top_k
    )
    return result

def initialize_chroma_from_pdf():
    file_path = "files/medical.pdf"
    result = store_pdf_to_chromaDB(file_path)
    print(result)


# for debug
def show_chroma_data():
    result = collection.get()
    print(result)