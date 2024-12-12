# Import Python libraries
import os
from langchain_neo4j import Neo4jGraph
from langchain_openai import ChatOpenAI

# Import Custom libraries
from Chains.vector_graph_chain import get_vector_graph_chain
from Chains.graph_qa_chain import get_graph_qa_chain, get_graph_qa_chain_with_context
from Chains.decompose import query_analyzer
from Prompts.prompt_template import create_few_shot_prompt, create_few_shot_prompt_with_context
from Prompts.prompt_examples import examples
from Prompts.prompt_formatter import create_formatter_prompt
from Graph.state import GraphState
from Tools.parse_vector_search import DocumentModel, Metadata

neo4j_url = os.environ.get("NEO4J_URI")
neo4j_user = os.environ.get("NEO4J_USERNAME")
neo4j_pwd = os.environ.get("NEO4J_PASSWORD")

graph = Neo4jGraph(
    url=neo4j_url,
    username=neo4j_user,
    password=neo4j_pwd
)

api_key = os.environ.get("OPENAI_API_KEY")

# Initialize the appropriate LLM based on provider
if (api_key != ""):
    llm = ChatOpenAI(
        model=os.environ.get("OPENAI_GENERATIVE_MODEL"), 
        temperature=0,
        api_key=api_key
    )
else:
    raise ValueError("Please set your OpenAI API Key in .env file")

def decomposer(state: GraphState):
    
    '''Returns a dictionary of at least one of the GraphState'''    
    '''Decompose a given question to sub-queries'''
    print("Decomposer Node:")
    question = state["question"]
    print(f"question: {question}")
    subqueries = query_analyzer.invoke(question)
    # print({"subqueries": subqueries, "question":question})
    return {"subqueries": subqueries, "question":question}
    
def vector_search(state: GraphState):
    
    ''' Returns a dictionary of at least one of the GraphState'''
    ''' Perform a vector similarity search and return article id as a parsed output'''
    print("Vector Search Node:")
    question = state["question"]
    queries = state["subqueries"]
    # print(f"question: {question}")
    # print(f"subqueries: {queries}\n")
    
    vector_graph_chain = get_vector_graph_chain()
    # print(vector_graph_chain)
    print("Begin vector graph chain")
    chain_result = vector_graph_chain.invoke({
        "query": queries[0].sub_query},
    )
    print("End vector graph chain")

    # Convert the result to a list of DocumentModel instances
    documents = []
    for doc in chain_result['source_documents']:
        temp_doc = DocumentModel(
        page_content=doc.page_content,
        metadata=Metadata()
        )
        metadata = Metadata(
            omid=doc.metadata.get("omid"),
            title=temp_doc.extract_title(),  # Extract title using the method
            year=doc.metadata.get("year"),
            month=doc.metadata.get("month"),
            day=doc.metadata.get("day"),
            venue=temp_doc.extract_venue(),  # Extract venue using the method
            publisher=doc.metadata.get("publisher"),
            embedding_vectors=doc.metadata.get("embedding_vectors")
        )
        document = DocumentModel(
            page_content=doc.page_content,
            metadata=metadata
        )
        
        documents.append(document)

    extracted_data = [{"title": doc.extract_title(), "omid": doc.metadata.omid, "year": doc.metadata.year} for doc in documents]
    article_ids = [{"omid": doc.metadata.omid, "title": doc.extract_title()} for doc in documents]
    # print({"article_ids": article_ids, "documents": extracted_data, "question":question, "subqueries": queries})
    return {"article_ids": article_ids, "documents": extracted_data, "question":question, "subqueries": queries}

def prompt_template(state: GraphState):
    
    '''Returns a dictionary of at least one of the GraphState'''
    '''Create a simple prompt tempalate for graph qa chain'''
    print("Prompt Template Node:")
    question = state["question"]

    # Create a prompt template
    prompt = create_few_shot_prompt()
    # print({"prompt": prompt, "question":question})
    return {"prompt": prompt, "question":question}

def graph_qa(state: GraphState):
    
    ''' Returns a dictionary of at least one of the GraphState '''
    ''' Invoke a Graph QA Chain '''
    print("Graph QA Node:")
    question = state["question"]
    print(f"State: {state}")
    graph_qa_chain = get_graph_qa_chain(state)
    # print(f"Graph QA Chain: {graph_qa_chain}")
    result = graph_qa_chain.invoke(
        {
            #"context": graph.schema, 
            "query": question,
        },
    )
    return {"documents": result, "question":question}
    
def prompt_template_with_context(state: GraphState):
    
    '''Returns a dictionary of at least one of the GraphState'''
    '''Create a dynamic prompt template for graph qa with context chain'''
    print("Prompt Template with Context Node:")
    question = state["question"]
    queries = state["subqueries"]
    print(f"State: {state}")

    # Create a prompt template
    prompt_with_context = create_few_shot_prompt_with_context(state)
    
    return {"prompt_with_context": prompt_with_context, "question":question, "subqueries": queries}

def graph_qa_with_context(state: GraphState):
    
    '''Returns a dictionary of at least one of the GraphState'''
    '''Invoke a Graph QA chain with dynamic prompt template'''
    
    queries = state["subqueries"]
    prompt_with_context = state["prompt_with_context"]

    # Instantiate graph_qa_chain_with_context
    # Pass the GraphState as 'state'. This chain uses state['prompt'] as input argument
    graph_qa_chain = get_graph_qa_chain_with_context(state)
    
    result = graph_qa_chain.invoke(
        {
            "query": queries[1].sub_query,
        },
    )
    return {"documents": result, "prompt_with_context":prompt_with_context, "subqueries": queries}

def format_response(state: GraphState):
    """Format the raw response into a user-friendly output using full context from GraphState"""
    print("Format Response Node:")
    
    # Extract all relevant information from state
    raw_response = state["documents"]
    question = state["question"]
    has_subqueries = "subqueries" in state and state["subqueries"] is not None
    article_context = state.get("article_ids", [])
    
    # Use existing LLM instance and get formatter prompt
    format_prompt = create_formatter_prompt()
    
    # Format the response
    if isinstance(raw_response, dict) and "result" in raw_response:
        raw_result = raw_response["result"]
    else:
        raw_result = raw_response
    
    # Build subqueries info if available
    subqueries_info = ""
    if has_subqueries:
        subqueries_info = f"Subqueries Used:\n{state['subqueries']}"
    
    # Build article context info if available
    article_context_info = ""
    if article_context:
        article_context_info = f"Articles Found in Context:\n{article_context}"
    
    formatted_response = llm.invoke(  # Using the existing llm from nodes.py
        format_prompt.format(
            question=question,
            query_type="Vector Search + Graph Query" if has_subqueries else "Direct Graph Query",
            result=str(raw_result),
            vector_search=str(has_subqueries),
            subqueries_info=subqueries_info,
            article_context_info=article_context_info
        )
    )
    
    return {"documents": formatted_response.content, "question": question, "formatted_response": formatted_response.content}