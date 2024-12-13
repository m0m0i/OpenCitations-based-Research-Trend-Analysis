# Graph RAG with LangChain

This backend implements the Graph RAG (Retrieval Augmented Generation) system using LangChain, LangGraph, and Neo4j. The core implementation is based on [this tutorial](https://medium.com/data-science-in-your-pocket/graphrag-using-langchain-31b1ef8328b9) by Suman Gautam.

## Overview

The system uses a sophisticated query routing and processing workflow via LangGraph to handle both simple and complex queries against a Neo4j graph database. It incorporates both vector search capabilities and graph database queries to provide comprehensive and accurate responses.

### Query Processing Workflow

The system uses different processing paths depending on query complexity:

1. **Simple Queries**: 
   - Direct graph database queries using Neo4j Cypher
   - Handled through straightforward graph QA chain
   - Best for queries that can be answered directly from the graph structure

2. **Complex Queries**:
   - Query decomposition into sub-queries
   - Vector search for relevant context
   - Enhanced graph QA with additional context
   - Ideal for queries requiring multiple steps or additional context

This split approach improves response quality by:
- Improving performance on simple queries answerable by basic Cyphers
- Breaking down complex questions into manageable parts
- Using vector search to provide relevant context for graph queries
- Combining information from multiple sources when needed

## Prompt System

The project uses several types of prompts to guide the AI's responses through the workflow:

### Query Examples (prompt_examples.py)
- Comprehensive set of example queries and their corresponding Cypher translations
- Helps the model understand common query patterns
- Examples cover various relationship types and query complexities

### Prompt Templates (prompt_template.py)
- Creates dynamic few-shot prompts
- Handles both context-free and context-aware scenarios
- Uses semantic similarity to select relevant examples
- Incorporates MaxMarginalRelevanceExampleSelector for diverse example selection

### Dynamic Context Integration
- Integrates vector search results into prompts
- Provides relevant publication IDs and titles as context
- Helps narrow down the search space for complex queries

### Response Format (prompt_formatter.py)
- Integrates original question with graph query results for a more attractive respons

## Model Selection

The system supports OpenAI models. For optimal results:
- Use GPT-4 or equivalent for more complex queries
- Better models provide:
  - More accurate query decomposition
  - Better understanding of context
  - More precise Cypher query generation
- The LLM models can be specified in the *.env* file

## Setup

1. Install requirements:
```bash
pip install -r requirements.txt
```
2. Instantiate the Neo4j Graph Database (more instructions can be found in the graph_database_setup folder):
  - Ensure that the APOC plugin is installed (this provides extra functionality for Neo4j)
4. Configure environment variables by configuring your .env file:
  - Create file .env with the contents of .env.example
  - Specify the Neo4j URI, user, and password
  - Paste your OpenAI API Key
  - Specify your desired LLM for generation and embedding
**Note to Instructors: Please contact us if you need an API key to use for testing**
4. Run the Flask server:
*in the backend folder*:
```python main.py```
