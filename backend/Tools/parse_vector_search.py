# Import Python Libraries
from pydantic import BaseModel
from typing import List, Optional
import re

# Import Custom Libraries
from Graph.state import GraphState

class Metadata(BaseModel):    
    omid: Optional[str] = "Unknown"
    title: Optional[str] = "Unknown"
    year: Optional[int] = None
    month: Optional[int] = None
    day: Optional[int] = None
    venue: Optional[str] = "Unknown"
    publisher: Optional[str] = "Unknown"
    embedding_vectors: Optional[list[float]] = None

class DocumentModel(BaseModel):
    page_content: str
    metadata: Metadata

    # def extract_title(self) -> str:
    #     # Extract the title from page_content
    #     if self.metadata.title:
    #         return self.metadata.title
    #     return ""

    def extract_title(self) -> str:
    # Trim leading/trailing whitespaces and extract the title
        cleaned_content = self.page_content.strip()
        match = re.search(r'^title:\s*(.+)$', cleaned_content, re.MULTILINE)
        if match:
            return match.group(1).strip()  # Ensure no extra spaces
        print("Warning: Title not found in page_content.")
        return None  # Return None if the title is not found
    
    def extract_venue(self) -> str:
        cleaned_content = self.page_content.strip()
        match = re.search(r'venue:\s*(.+)', cleaned_content, re.MULTILINE)
        if match:
            return match.group(1).strip()
        print("Warning: Venue not found in page_content.")
        return None

class ResultModel(BaseModel):
    documents: List[DocumentModel]
    

def create_context(state: GraphState):
    """Originally designed to be a node, but not used as node anymore, merged to vector search step"""
    chain_result = state["documents"]
    question = state["question"]
    queries = state["subqueries"]

    # Convert the result to a list of DocumentModel instances
    documents = []
    for doc in chain_result['source_documents']:
        metadata = Metadata(
            omid=doc.metadata.get("omid"),
            title=doc.metadata.get("title"),
            year=doc.metadata.get("year"),
            month=doc.metadata.get("month"),
            day=doc.metadata.get("day"),
            venue=doc.metadata.get("venue"),
            publisher=doc.metadata.get("publisher"),
            embedding_vectors=doc.metadata.get("embedding_vectors")
        )
        document = DocumentModel(
            page_content=doc.page_content,
            metadata=metadata
        )
        documents.append(document)
    extracted_data = [{"title": doc.extract_title(), "omid": doc.metadata.omid, "year": doc.metadata.year} for doc in documents]
    article_ids = [{"omid": doc.metadata.omid, "title": doc.metadata.title} for doc in documents]
    
    return {"article_ids": article_ids, "question":question, "subqueries": queries}