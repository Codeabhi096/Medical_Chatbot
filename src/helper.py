from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document         
from typing import List
import os


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


def filter_to_minimal_docs(docs: List[Document]) -> List[Document]:
    return [
        Document(
            page_content=doc.page_content.strip(),
            metadata={"source": doc.metadata.get("source", "unknown")}
        )
        for doc in docs
    ]


def text_split(extracted_data: List[Document]) -> List[Document]:
    if not extracted_data:
        raise ValueError("No documents provided for splitting!")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    return text_splitter.split_documents(extracted_data)


def download_hugging_face_embeddings():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True}
    )