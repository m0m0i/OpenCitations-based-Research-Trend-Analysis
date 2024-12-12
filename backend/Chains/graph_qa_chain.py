# Import Python Libraries
import os

from langchain_openai import ChatOpenAI
from langchain_neo4j.chains.graph_qa.cypher import GraphCypherQAChain
from langchain_neo4j import Neo4jGraph
from langchain_neo4j.graphs.graph_store import GraphStore

# Import Custom Libraries
from Prompts.prompt_template import create_few_shot_prompt, create_few_shot_prompt_with_context
from Graph.state import GraphState

# Instantiate a Neo4j graph
graph = Neo4jGraph(
    url=os.environ.get('NEO4J_URI'),
    username=os.environ.get('NEO4J_USERNAME'),
    password=os.environ.get('NEO4J_PASSWORD')
)
graph.refresh_schema()

api_key=os.environ.get("OPENAI_API_KEY")

# Initialize the appropriate LLM based on provider
if (api_key != ""):
    llm = ChatOpenAI(
        model=os.environ.get("OPENAI_GENERATIVE_MODEL"),
        temperature=0,
        api_key=os.environ.get("OPENAI_API_KEY")
    )
else:
    raise ValueError("Please set your preferred Generative AI provider (GOOGLE or OPENAI) in .env file")

def get_graph_qa_chain(state: GraphState):
    
    """Create a Neo4j Graph Cypher QA Chain"""
    print("Get Graph QA Chain Function:")
    prompt = state["prompt"]
    print(f"Prompt: {prompt}")
    print(f"Graph type: {type(graph)}")
    print(f"LLM Type: {type(llm)}")
    print(f"Prompt Type: {type(prompt)}")
    
    graph_qa_chain = GraphCypherQAChain.from_llm(
            cypher_llm = llm, #should use gpt-4 for production
            qa_llm = llm,
            validate_cypher= True,
            graph=graph,
            verbose=True,
            cypher_prompt = prompt,
            # return_intermediate_steps = True,
            return_direct = True,
            allow_dangerous_requests=True
        )
    return graph_qa_chain

def get_graph_qa_chain_with_context(state: GraphState):
    
    """Create a Neo4j Graph Cypher QA Chain. Using this as GraphState so it can access state['prompt']"""
    
    prompt_with_context = state["prompt_with_context"] 
    
    graph_qa_chain = GraphCypherQAChain.from_llm(
            cypher_llm = llm, #should use gpt-4 for production
            qa_llm = llm,
            validate_cypher= True,
            graph=graph,
            verbose=False,
            cypher_prompt = prompt_with_context,
            # return_intermediate_steps = True,
            return_direct = True,
            allow_dangerous_requests = True
        )
    return graph_qa_chain