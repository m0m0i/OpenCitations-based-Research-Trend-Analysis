from dotenv import load_dotenv
import os
from Graph.graph import app

load_dotenv()

def graphRAG(role, message):
    result = app.invoke({"question": message})

    return result['documents']