from neo4j import GraphDatabase
import json

# URI examples: "neo4j://localhost", "neo4j+s://xxx.databases.neo4j.io"
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "password" # your password to the local DBMS you created on Neo4j Desktop where you want to upload the data

with GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD)) as driver:
    driver.verify_connectivity()

def fetch_nodes():
    query = """
    MATCH (n)
    RETURN n
    LIMIT 5
    """
    with driver.session() as session:
        result = session.run(query)
        
        # Extract nodes and convert them to a string list
        nodes_list = [str(record["n"]) for record in result]
        nodes_string = "\n".join(nodes_list)
        
        # Wrap the string list in a JSON object with a "message" key
        output = {
            "message": nodes_string
        }
        return json.dumps(output, indent=4)