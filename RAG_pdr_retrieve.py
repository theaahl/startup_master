import os
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_community.vectorstores import MongoDBAtlasVectorSearch
import streamlit as st
from pymongo import MongoClient
from pymongo.server_api import ServerApi 
from langchain_openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI

PROMPT_TEMPLATE = """
When the user asks a question, use the following context to answer, if relevant:

{context}
---------------------------------------
User question: {question}
"""

# MONGO_URI = os.environ["MONGO_URI"]
PARENT_DOC_ID_KEY = "parent_doc_id"
# DB_NAME = "langchain-parent-document-retriever"
# COLLECTION_NAME = "mongodb-docs"
ATLAS_VECTOR_SEARCH_INDEX_NAME = "vector_index"
EMBEDDING_FIELD_NAME = "embedding"
# client = MongoClient(MONGO_URI)
# db = client[DB_NAME]
# MONGODB_COLLECTION = db[COLLECTION_NAME]


@st.cache_resource
def init_connection():
    return MongoClient(st.secrets.mongo.uri, server_api=ServerApi('1'))

client = init_connection()
collection = client.RAG_data.frameworks_docs2

embeddings = OpenAIEmbeddings(openai_api_key=st.secrets.api.key)


# vector_search = MongoDBAtlasVectorSearch.from_connection_string(
#     client,
#     "RAG_data.frameworks_docs2",
#     embeddings,
#     index_name=ATLAS_VECTOR_SEARCH_INDEX_NAME,
# )

vector_search = MongoDBAtlasVectorSearch.from_connection_string(
    client,
    "RAG_data" + "." + "frameworks_docs2",
    embeddings, #OpenAIEmbeddings(disallowed_special=()),
    index_name=ATLAS_VECTOR_SEARCH_INDEX_NAME,
)

def retrieve(query: str):
    vectorStore = MongoDBAtlasVectorSearch(
        collection, OpenAIEmbeddings(openai_api_key=st.secrets.api.key), index_name="vsearch_index")
    
    print("vector_search:", vector_search)

    results = vectorStore.similarity_search(
        query,
        k=3,
        pre_filter={"doc_level": {"$eq": "child"}},
        post_filter_pipeline=[
            {"$project": {"embedding": 0}},
            {
                "$lookup": {
                    "from": "frameworks_docs2",
                    "localField": PARENT_DOC_ID_KEY,
                    "foreignField": PARENT_DOC_ID_KEY,
                    "as": "parent_context",
                    "pipeline": [
                        {"$match": {"doc_level": "parent"}},
                        {"$limit": 1},
                        {"$project": {"embedding": 0}},
                    ],
                }
            },
        ],
    )
    parent_docs = []
    parent_doc_ids = set()
    for result in results:
        res = result.metadata["parent_context"][0]
        text = res.pop("text")
        # This causes serialization issues.
        res.pop("_id")
        parent_doc = Document(page_content=text, metadata=res)
        if parent_doc.metadata[PARENT_DOC_ID_KEY] not in parent_doc_ids:
            parent_doc_ids.add(parent_doc.metadata[PARENT_DOC_ID_KEY])
            parent_docs.append(parent_doc)
    
    print("Results:", results)
    print("Parent docs:", parent_docs)
    return parent_docs

# RAG prompt
# human_message = '''Answer the question based only on the following context:
# {context}
# Question: {question}'''

# messages = [
#     ("system", "You are a helpful assistant."),
#     ("human", human_message),
# ]

# tror ikke dette trengs...
# RAG
# prompt = ChatPromptTemplate.from_messages(messages)
# model = chat
# chain = (
#     RunnableParallel({"context": retrieve, "question": RunnablePassthrough()})
#     | prompt
#     | model
#     | StrOutputParser()
# )

def generate_query(docs, query):
    context_text = "\n\n---\n\n".join([doc.page_content for doc in docs]) #combine_context(docs)
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query)
    print(prompt)
    return prompt

def retrieve_response(prompt):
    model = ChatOpenAI(openai_api_key=st.secrets.api.key, model_name = 'gpt-3.5-turbo', temperature=0)
    response_text = model.predict(prompt)

    formatted_response = f"Response: {response_text}"
    return formatted_response

query = "what is esssdm?"
context = retrieve(query)
prompt = generate_query(context, query)
print(retrieve_response(prompt))