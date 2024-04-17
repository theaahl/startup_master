from pymongo import MongoClient
from langchain_community.vectorstores import MongoDBAtlasVectorSearch
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor
import streamlit as st
from pymongo.server_api import ServerApi 
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

# https://www.youtube.com/watch?v=tcqEUSNCn8I


#query = "I want to build an app for grocery shopping. How can i know if this is a viable product?"
#https://www.mongodb.com/developer/languages/python/semantic-search-made-easy-langchain-mongodb/?utm_campaign=devrel&utm_source=youtube&utm_medium=organic_social&utm_content=ZvwUzcMvKiI&utm_term=jay.javed
#https://github.com/mongodb-developer/atlas-langchain/blob/main/vectorize.py
#https://blog.langchain.dev/tutorial-chatgpt-over-your-data/

PROMPT_TEMPLATE = """
\nWhen the user asks a question, use the following context to answer, if relevant:
\n
{context}
"""

@st.cache_resource
def init_connection():
    return MongoClient(st.secrets.mongo.uri, server_api=ServerApi('1'))

client = init_connection()
collection = client.RAG_data.frameworks

def retrieve_information(query):

    vectorStore = MongoDBAtlasVectorSearch(
        collection, OpenAIEmbeddings(openai_api_key=st.secrets.api.key), index_name="vsearch_index")

    docs = vectorStore.max_marginal_relevance_search(query, K=3)

    return docs

def generate_query(docs, query):
    context_text = "\n\n---\n\n".join([doc.page_content for doc in docs]) #combine_context(docs)
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text) #, question=query)
    print(prompt)
    return prompt

def retrieve_response(prompt):
    model = ChatOpenAI(openai_api_key=st.secrets.api.key, model_name = 'gpt-4', temperature=0)
    response_text = model.predict(prompt)

    formatted_response = f"Response: {response_text}"
    print(formatted_response)
    return formatted_response

