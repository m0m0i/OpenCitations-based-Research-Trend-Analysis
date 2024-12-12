import os

from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from langchain.output_parsers import PydanticToolsParser
from langchain_core.prompts import ChatPromptTemplate

class SubQuery(BaseModel):
    """Decompose a given question/query into sub-queries"""

    sub_query: str = Field(
        ...,
        description="A unique paraphrasing of the original questions.",
    )

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

system = """You are an expert at converting user questions into Neo4j Cypher queries. \

Perform query decomposition. Given a user question, break it down into two distinct subqueries that \
you need to answer in order to answer the original question.

For the given input question, create a query for similarity search and create a query to perform neo4j graph query.
Here is example:
Question: Find the articles about the photosynthesis and return their titles.
Answers:
sub_query1 : Find articles related to photosynthesis.
sub_query2 : Return titles of the articles
"""

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "{question}"),
    ]
)

llm_with_tools = llm.bind_tools([SubQuery])
parser = PydanticToolsParser(tools=[SubQuery])
query_analyzer = prompt | llm_with_tools | parser  # Structured output with Pydantic