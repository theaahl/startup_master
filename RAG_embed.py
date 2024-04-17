#from langchain.document_loaders import DirectoryLoader
from langchain_community.document_loaders import DirectoryLoader
#from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
#from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores.chroma import Chroma
import os
import shutil
import streamlit as st
from pymongo import MongoClient
#from langchain.vectorstores import MongoDBAtlasVectorSearch
from pymongo.server_api import ServerApi 
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import MongoDBAtlasVectorSearch
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader

def load_documents():
    print("loading begins")
    # folder_path = "./files/"
    # all_documents = []
    # for filename in os.listdir(folder_path):
    #     if filename.endswith(".pdf"):
    #         # Construct the full path to the PDF file
    #         file_path = os.path.join(folder_path, filename)
            
    #         # Load the PDF document
    #         loaded_document = PyPDFLoader(file_path)
            
    #         # Append the loaded document to the list
    #         all_documents.append(loaded_document) 
    loader = PyPDFLoader("./files/The Real Product Market Fit.pdf")
    print("loader ferdig")
    documents = loader.load()

    print("loading complete")
    return documents


def split_text(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=200,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} documents into {len(chunks)} chunks.")

    # document = chunks[10]
    # print(document.page_content)
    # print(document.metadata)

    return chunks

def save_embeddings(chunks):
    collection = client.RAG_data.frameworks
    
    embeddings = OpenAIEmbeddings(openai_api_key=st.secrets.api.key)

    # Reset w/out deleting the Search Index 
    # collection.delete_many({})
    # print("Slettet gammel data")
    # Insert the documents in MongoDB Atlas with their embedding
    docsearch = MongoDBAtlasVectorSearch.from_documents(
        chunks, embeddings, collection=collection, index_name="vsearch_index"
    )

    return docsearch

@st.cache_resource
def init_connection():
    return MongoClient(st.secrets.mongo.uri, server_api=ServerApi('1'))

client = init_connection()
collection = client.RAG_data.frameworks

# documents = load_documents()
# chunks = split_text(documents)

# docsearch = save_embeddings(chunks, collection)