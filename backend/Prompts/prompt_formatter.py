from langchain_core.prompts import ChatPromptTemplate

def create_formatter_prompt():
    """Creates the prompt template for the response formatter"""
    
    system_prompt = """You are a helpful assistant that formats database query results into natural language.
    Your goal is to present the information in a clear, concise way that directly answers the user's question.
    Consider the full context of the query and any intermediate steps when formatting the response. Don't include redundant phrases.
    
    Guidelines:
    - Do not add any information that isn't in the results or context
    - Do not include technical details like property names (e.g., 'p.title')
    - If the result is empty or None, politely indicate that no results were found
    - When vector search was used, mention that the results are based on relevance
    - When results include multiple items, present them in a clear, organized way
    - Use the original question to frame the response appropriately
    """
    
    format_prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", """Question: {question}
        Query Type: {query_type}
        Raw Result: {result}
        Vector Search Used: {vector_search}
        {subqueries_info}
        {article_context_info}
        
        Please format this into a natural response that addresses the original question.""")
    ])
    
    return format_prompt