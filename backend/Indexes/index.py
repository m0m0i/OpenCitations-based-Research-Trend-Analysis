import os
import openai
from langchain_community.vectorstores import Neo4jVector
from langchain_openai import OpenAIEmbeddings

openai.api_key  = os.environ.get("OPENAI_API_KEY")

if (openai.api_key != ""):
    EMBEDDING_MODEL = OpenAIEmbeddings(model=os.environ.get("OPENAI_EMBEDDING_MODEL"))
    EMBEDDING_NODE_PROPERTY = 'openai_embedding_vectors'
else:
    print("Please set your preferrable Generative AI provider in .env file")

NEO4J_CONNECTION_URI = os.environ.get('NEO4J_URI')
NEO4J_USERNAME = os.environ.get('NEO4J_USERNAME')
NEO4J_PASSWORD = os.environ.get('NEO4J_PASSWORD')

# BROKEN - LC doesn't support index across multiple node labels
def get_combined_vector_index():
    '''Create a combined vector index for Publication and Author nodes.'''
    
    # Create separate indices for Publication and Author nodes
    neo4j_publication_vector_index = Neo4jVector.from_existing_graph(
        embedding=EMBEDDING_MODEL,
        url=NEO4J_CONNECTION_URI,
        username=NEO4J_USERNAME,
        password=NEO4J_PASSWORD,
        index_name='publication_vector',
        node_label='Publication',
        text_node_properties=['title', 'venue'],  # Properties for Publication
        embedding_node_property=EMBEDDING_NODE_PROPERTY,
    )
    
    neo4j_author_vector_index = Neo4jVector.from_existing_graph(
        embedding=EMBEDDING_MODEL,
        url=NEO4J_CONNECTION_URI,
        username=NEO4J_USERNAME,
        password=NEO4J_PASSWORD,
        index_name='author_vector',
        node_label='Author',
        text_node_properties=['name'],  # Properties for Author
        embedding_node_property=EMBEDDING_NODE_PROPERTY,
    )
    
    # Combine the two indices
    combined_index = neo4j_publication_vector_index.combine(neo4j_author_vector_index)
    
    return combined_index

# BROKEN - LC doesn't support index across multiple node labels
def get_publication_author_vector_index():
    '''Create a vector index for Publication and Author nodes.'''
    print("Get Publication Author Vector Index")

    neo4j_publication_author_vector_index = Neo4jVector.from_existing_graph(
        embedding=EMBEDDING_MODEL,  # Replace with your embedding model
        url=NEO4J_CONNECTION_URI,  # Replace with your Neo4j connection URI
        username=NEO4J_USERNAME,   # Replace with your username
        password=NEO4J_PASSWORD,   # Replace with your password
        index_name='publication_author_vector',  # Name your index
        node_label=['Publication', 'Author'],  # Include both node types
        text_node_properties={
            'Publication': ['title', 'venue'],  # Properties to embed for Publication
            'Author': ['name']                  # Properties to embed for Author
        },
        embedding_node_property=EMBEDDING_NODE_PROPERTY,  # Property to store embeddings
    )
    return neo4j_publication_author_vector_index

def get_publication_vector_index():
    '''Create vector for publication title and instantiate Neo4j vector from graph.'''
    print("Get Publication Vector Index")
    
    neo4j_publication_vector_index = Neo4jVector.from_existing_graph(
        embedding=EMBEDDING_MODEL,  # Replace with your embedding model
        url=NEO4J_CONNECTION_URI,  # Replace with your connection URI
        username=NEO4J_USERNAME,   # Replace with your username
        password=NEO4J_PASSWORD,   # Replace with your password
        index_name='publication_title_vector_openai',  # Name your index
        node_label='Publication',  # Node type
        text_node_properties=['title', 'venue'],  # Properties to embed
        embedding_node_property=EMBEDDING_NODE_PROPERTY,  # Where embeddings are stored
    )
    return neo4j_publication_vector_index

def get_author_vector_index():
    '''Create vector for author names and instantiate Neo4j vector from graph.'''
    print("Get Author Vector Index")
    
    neo4j_author_vector_index = Neo4jVector.from_existing_graph(
        embedding = EMBEDDING_MODEL,
        url = NEO4J_CONNECTION_URI,
        username = NEO4J_USERNAME,
        password = NEO4J_PASSWORD,
        index_name = 'author_name_vector',
        node_label = 'Author',
        text_node_properties = ['name'],  # Embedding 'name' property
        embedding_node_property = EMBEDDING_NODE_PROPERTY,
    )
    return neo4j_author_vector_index
