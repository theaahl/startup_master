import uuid
import streamlit as st
from pymongo import MongoClient
from pymongo.server_api import ServerApi 
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import MongoDBAtlasVectorSearch
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings

# Vet ikke om dette er nødvendig
# ###########################################################################
# # Amazon Bedrock - boto3
# import boto3
# from langchain_community.embeddings import BedrockEmbeddings

# # Setup bedrock
# bedrock_runtime = boto3.client(
#     service_name="bedrock-runtime",
#     region_name="us-east-1",
# )

# # Embeddings Model - Amazon Titan Embeddings Model using LangChain
# bedrock_embedding = BedrockEmbeddings(
#     client=bedrock_runtime,
#     model_id="amazon.titan-embed-text-v1",
# )
# ###########################################################################

PARENT_DOC_ID_KEY = "parent_doc_id"

# MONGO_URI = os.environ["MONGO_URI"]

@st.cache_resource
def init_connection():
    return MongoClient(st.secrets.mongo.uri, server_api=ServerApi('1'))

client = init_connection()
collection = client.RAG_data.frameworks_docs2

# ATLAS_VECTOR_SEARCH_INDEX_NAME = "vector_index"
# EMBEDDING_FIELD_NAME = "embedding"

def load_documents():
    print("loading begins")
    loader = PyPDFLoader("./files/LESS_ESSSDMpaper.pdf")
    print("loader ferdig")
    documents = loader.load()


    print("loading complete")
    return documents

def parent_child_splitter(data):
    parent_splitter = RecursiveCharacterTextSplitter(chunk_size=2000)
    # text_splitter = RecursiveCharacterTextSplitter(
    #     chunk_size=1000,
    #     chunk_overlap=200,
    #     length_function=len,
    #     add_start_index=True,
    # )

    # This text splitter is used to create the child documents
    # It should create documents smaller than the parent
    child_splitter = RecursiveCharacterTextSplitter(chunk_size=700)
    documents = parent_splitter.split_documents(data)
    doc_ids = [str(uuid.uuid4()) for _ in documents]
    id_key=PARENT_DOC_ID_KEY

    docs = []
    for i, doc in enumerate(documents):
        _id = doc_ids[i]
        sub_docs = child_splitter.split_documents([doc])
        for _doc in sub_docs:
            _doc.metadata[id_key] = _id
            _doc.metadata["doc_level"] = "child"
        docs.extend(sub_docs)
        doc.metadata[id_key] = _id
        doc.metadata["doc_level"] = "parent"
    return documents, docs

def save_embeddings(parent_docs, child_docs):
    embeddings = OpenAIEmbeddings(openai_api_key=st.secrets.api.key)
    documents=parent_docs + child_docs
    # Insert the documents in MongoDB Atlas with their embedding
    
    docsearch = MongoDBAtlasVectorSearch.from_documents(
        documents, embeddings, collection=collection, index_name="vsearch_index"
    )

    return docsearch

all_docs = load_documents()
parent_docs, child_docs = parent_child_splitter(all_docs)

docsearch = save_embeddings(parent_docs, child_docs)
# if __name__ == "__main__":
#     # Load docs
#     loader = PyPDFLoader("./mongodb-embedding-generative-ai.pdf")
#     data = loader.load()

#     # Split docs
#     parent_docs, child_docs = parent_child_splitter(data)

#     # Insert the documents in MongoDB Atlas Vector Search
#     _ = MongoDBAtlasVectorSearch.from_documents(
#         documents=parent_docs + child_docs,
#         embedding=bedrock_embedding,
#         collection=MONGODB_COLLECTION,
#         index_name=ATLAS_VECTOR_SEARCH_INDEX_NAME,
#     )