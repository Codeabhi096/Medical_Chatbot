from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document
from typing import List
import os


# Extract Data From the PDF Files
def load_pdf_file(data_path: str) -> List[Document]:
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Path not found: {data_path}")

    loader = DirectoryLoader(
        data_path,
        glob="*.pdf",
        loader_cls=PyPDFLoader
    )

    documents = loader.load()

    if not documents:
        raise ValueError("No PDF documents found in the directory!")

    return documents


# Keep only minimal metadata
def filter_to_minimal_docs(docs: List[Document]) -> List[Document]:
    minimal_docs: List[Document] = []

    for doc in docs:
        src = doc.metadata.get("source", "unknown")

        minimal_docs.append(
            Document(
                page_content=doc.page_content.strip(),
                metadata={"source": src}
            )
        )

    return minimal_docs


# Split the Data into Text Chunks
def text_split(extracted_data: List[Document]) -> List[Document]:
    if not extracted_data:
        raise ValueError("No documents provided for splitting!")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50  # increased for better context retention
    )

    text_chunks = text_splitter.split_documents(extracted_data)

    return text_chunks


# Download the Embeddings from HuggingFace
def download_hugging_face_embeddings():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},  # change to 'cuda' if GPU available
        encode_kwargs={"normalize_embeddings": True}
    )

    return embeddings