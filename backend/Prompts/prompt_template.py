import os
import openai

from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate
from langchain_core.example_selectors import MaxMarginalRelevanceExampleSelector
from Prompts.prompt_examples import examples

# Import Custom Libraries
from Graph.state import GraphState

openai.api_key  = os.environ.get("OPENAI_API_KEY")

if (openai.api_key != ""):
    EMBEDDING_MODEL = OpenAIEmbeddings(model=os.environ.get("OPENAI_EMBEDDING_MODEL"))
    EMBEDDING_NODE_PROPERTY = 'openai_embedding_vectors'
else:
    print("Please set your preferrable Generative AI provider in .env file")

# Instantiate a example selector
example_selector = MaxMarginalRelevanceExampleSelector.from_examples(
    examples = examples,
    embeddings = EMBEDDING_MODEL,
    vectorstore_cls = Chroma,
    k=5,   
)

# Configure a formatter
example_prompt = PromptTemplate(
    input_variables=["question", "query"],
    template="Question: {question}\nCypher query: {query}"
)

def create_few_shot_prompt():
    '''Create a prompt template without context variable. The suffix provides dynamically selected prompt examples using similarity search'''
    
    prefix = """
    Task:Generate Cypher statement to query a graph database.
    Instructions:
    Use only the provided relationship types and properties in the schema.
    Do not use any other relationship types or properties that are not provided.

    Note: Do not include any explanations or apologies in your responses.
    Do not respond to any questions that might ask anything else than for you to construct a Cypher statement.
    Do not include any text except the generated Cypher statement.

    Examples: Here are a few examples of generated Cypher statements for particular questions:
    """

    FEW_SHOT_PROMPT = FewShotPromptTemplate(
        example_selector = example_selector,
        example_prompt = example_prompt,
        prefix=prefix,
        suffix="Question: {question}, \nCypher Query: ",
        input_variables =["question","query"],
    ) 
    return FEW_SHOT_PROMPT

def create_few_shot_prompt_with_context(state: GraphState):
    '''Create a prompt template with context variable. The context variable will be based on the output from vector qa chain'''
    '''The output of vector qa is list of node ids against which to perform graph query'''
    print("Create Few Shot Prompt With Context Function:")
    context = state["article_ids"]

    # print(f"Context: {context}")
    
    prefix = f"""
    Task:Generate Cypher statement to query a graph database.
    Instructions:
    Use only the provided relationship types and properties in the schema.
    Do not use any other relationship types or properties that are not provided.

    Note: Do not include any explanations or apologies in your responses.
    Do not respond to any questions that might ask anything else than for you to construct a Cypher statement.
    Do not include any text except the generated Cypher statement.
    
    A context is provided from a vector search with the following publication IDs (omid), ordered by relevance:
    {[f"omid: {article['omid']}, title: {article['title']}" for article in context]}

    Using these publication IDs, create Cypher statements to query the graph. Note that Articles are referred to as Publications in the database.
    Examples: Here are a few examples of generated Cypher statements for some question examples:
    """

    # print(f"Example Selector: {example_selector}")
    # print(f"Example Prompt: {example_prompt}")
    # print(f"Prefix: {prefix}")

    FEW_SHOT_PROMPT = FewShotPromptTemplate(
        example_selector = example_selector,
        example_prompt = example_prompt,
        prefix=prefix,
        suffix="Question: {question}, \nCypher Query: ",
        input_variables =["question", "query"]
    )

    # Debugging: Check what the template contains
    # print(f"DEBUG: Generated FewShotPromptTemplate input_variables: {FEW_SHOT_PROMPT.input_variables}")
    # print(f"DEBUG: Generated FewShotPromptTemplate prefix: {FEW_SHOT_PROMPT.prefix}")
    # print(f"DEBUG: Generated FewShotPromptTemplate suffix: {FEW_SHOT_PROMPT.suffix}")

    return FEW_SHOT_PROMPT