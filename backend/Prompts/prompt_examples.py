examples = [
    {
        "question": "What are the titles of publications authored by a specific author?",
        "query": "MATCH (a:Author)-[:AUTHORED]->(p:Publication) WHERE a.name = 'Author Name' RETURN p.title"
    },
    {
        "question": "Who authored a specific publication?",
        "query": "MATCH (a:Author)-[:AUTHORED]->(p:Publication) WHERE p.title = 'Publication Title' RETURN a.name"
    },
    {
        "question": "How many publications were authored by a specific author?",
        "query": "MATCH (a:Author)-[:AUTHORED]->(p:Publication) WHERE a.name = 'Author Name' RETURN count(p)"
    },
    {
        "question": "List all authors of publications published in a specific venue.",
        "query": "MATCH (a:Author)-[:AUTHORED]->(p:Publication) WHERE p.venue = 'Venue Name' RETURN DISTINCT a.name"
    },
    {
	#no "citing" column. Does this equal to the "volume" column?
        "question": "What are the top 10 cited publications?",
        "query": "MATCH (p:Publication)<-[:CITED]-(citing:Publication) RETURN p.title, count(citing) AS citation_count ORDER BY citation_count DESC LIMIT 10"
    },
    {
        "question": "Which authors have authored publications in a specific year?",
        "query": "MATCH (a:Author)-[:AUTHORED]->(p:Publication) WHERE p.year = 2020 RETURN DISTINCT a.name"
    },
    {
        "question": "How many publications were authored by authors who published in a specific venue?",
        "query": "MATCH (a:Author)-[:AUTHORED]->(p:Publication) WHERE p.venue = 'Venue Name' RETURN count(p)"
    },
    {
        "question": "Find publications authored in a specific year and published by a specific publisher.",
        "query": "MATCH (p:Publication) WHERE p.year = 2020 AND p.publisher = 'Publisher Name' RETURN p.title"
    },
    {
        "question": "What are the titles of publications published after a specific year?",
        "query": "MATCH (p:Publication) WHERE p.year > 2010 RETURN p.title"
    },
    {
        "question": "List all publications authored by a specific author in a specific venue.",
        "query": "MATCH (a:Author)-[:AUTHORED]->(p:Publication) WHERE a.name = 'Author Name' AND p.venue = 'Venue Name' RETURN p.title"
    },
    {
	#no "citing" column. Does this equal to the "volume" column?
        "question": "Who are the authors of the most cited publication?",
        "query": "MATCH (p:Publication)<-[:CITED]-(citing:Publication), (a:Author)-[:AUTHORED]->(p) WITH p, count(citing) AS citation_count ORDER BY citation_count DESC LIMIT 1 RETURN p.title, a.name"
    },
    {
        "question": "What are the top venues by the number of publications?",
        "query": "MATCH (p:Publication) RETURN p.venue, count(p) AS num_publications ORDER BY num_publications DESC LIMIT 10"
    },
    {
        "question": "How many publications did a specific author publish in a specific year?",
        "query": "MATCH (a:Author)-[:AUTHORED]->(p:Publication) WHERE a.name = 'Author Name' AND p.year = 2020 RETURN count(p)"
    }
]
