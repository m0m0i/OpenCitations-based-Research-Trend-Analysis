# Import Python Libraries
import os
from langchain_openai import ChatOpenAI
from langchain.chains.retrieval_qa.base import RetrievalQA

# Import Custom Libraries
from Indexes import index

api_key=os.environ.get("OPENAI_API_KEY")

# Replace the llm initialization with modular version
genai_provider = os.environ.get("GENAI")

if (api_key != ""):    
    llm = ChatOpenAI(
        model=os.environ.get("OPENAI_GENERATIVE_MODEL"), 
        temperature=0,
        api_key=os.environ.get("OPENAI_API_KEY")
    )
else:
    raise ValueError("Please set your OpenAI API Key in .env file")

vector_index = index.get_publication_vector_index()

def get_vector_graph_chain():
    '''Create a Neo4j Retrieval QA Chain. Returns top K most relevant articles'''
    vector_graph_chain = RetrievalQA.from_chain_type(
        llm, 
        chain_type="stuff", 
        retriever = vector_index.as_retriever(search_kwargs={'k':3}), 
        verbose=True,
        return_source_documents=True,
    )
    return vector_graph_chain