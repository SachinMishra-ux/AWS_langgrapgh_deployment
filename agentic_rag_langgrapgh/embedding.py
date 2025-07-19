#from langchain_community.document_loaders import PyPDFLoader

# # Load PDF and extract text into documents
# loader = PyPDFLoader(r"C:\Users\smm931389\Documents\AWS_BEDROCK\simple_pdf_rag_bot\PatientReport1.2016release.pdf")
# documents = loader.load()

# ## ssl error:
# import os
# os.environ['HF_HUB_DISABLE_SSL_VERIFICATION'] = '1'

# from sentence_transformers import SentenceTransformer
# from langchain_community.vectorstores import FAISS
# from langchain_community.embeddings import HuggingFaceEmbeddings


## open source model from huggingface
# embedding_model = HuggingFaceEmbeddings(
#     model_name="BAAI/bge-base-en-v1.5",
#     model_kwargs={"device": "cpu"}
# )



import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import AzureOpenAIEmbeddings

from langchain.text_splitter import RecursiveCharacterTextSplitter

# === Load Azure credentials ===
load_dotenv(override=True)

def load_data(pdf_path):
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    return documents


# === Chunk documents ===
def chunk_documents(documents, chunk_size_words=2000, chunk_overlap_words=200):
    # Convert words to approx chars (1 word ≈ 6.5 chars conservatively)
    chunk_size_chars = chunk_size_words * 6
    chunk_overlap_chars = chunk_overlap_words * 6

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size_chars,
        chunk_overlap=chunk_overlap_chars,
        separators=["\n\n", "\n", ".", " ", ""]
    )

    return splitter.split_documents(documents)

def get_azure_embedding_model():
    return AzureOpenAIEmbeddings(
        azure_deployment=os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    )

def create_and_save_faiss(documents, embedding_model, save_path):
    db = FAISS.from_documents(documents, embedding_model)
    db.save_local(save_path)
    print(f"✅ FAISS index saved at: {save_path}")

# === Main execution ===
if __name__ == '__main__':
    pdf_path = r"C:\Users\smm931389\Documents\AWS_BEDROCK\simple_pdf_rag_bot\1519023930M32AllergyandHypersensitivity-IQuad1.pdf"
    faiss_save_path = "faiss_index_zoology_book"

    documents = load_data(pdf_path)
    print(f"Loaded {len(documents)} pages")

    chunks = chunk_documents(documents, chunk_size_words=2000)
    print(f"Created {len(chunks)} chunks")

    embedding_model = get_azure_embedding_model()
    create_and_save_faiss(chunks, embedding_model, faiss_save_path)


