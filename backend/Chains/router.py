import os

from typing import Literal
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

class RouteQuery(BaseModel):
    """Route a user query to the most relevant datasource."""

    datasource: Literal["vector search", "graph query"] = Field(
        ...,
        description="Given a user question choose to route it to vectorstore or graphdb.",
    )

# Loading environment variables from .env file
load_dotenv()

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

structured_llm_router = llm.with_structured_output(RouteQuery)

system = """You are an expert at routing a user question to perform vector search or graph query. 
The vector store contains documents related to authors, author properties such as name, articles, and article properties such as year and publisher . Here are three routing situations:
If the user question is about similarity search, perform vector search. The user query may include term like similar, related, relvant, identitical, closest etc to suggest vector search. For all else, use graph query.

Example questions of Vector Search Case: 
    Find articles about photosynthesis
    Find similar articles that is about oxidative stress
    
Example questions of Graph DB Query: 
    MATCH (n:Article) RETURN COUNT(n)
    MATCH (n:Article) RETURN n.title

Example questions of Graph QA Chain: 
    Find articles published in a specific year and return it's title, authors
    Find authors from the institutions who are located in a specific country, e.g Japan
"""

route_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "{question}")
    ]
)

question_router = route_prompt | structured_llm_router