# cs410-team-project

## Project Title

**OpenCitations-based Research Trend Analysis**

## Project Description:

Our project aims to analyze citation patterns within the OpenCitations dataset to identify and visualize emerging research trends across various academic fields. By leveraging additional datasets from Wikidata and DBpedia, we will track the growth of citations in specific research areas, pinpoint influential publications and authors, and visualize the evolution of these fields over time.  
We will focus on developing innovative metrics for citation analysis, such as measuring citation velocity and impact score, which will help capture the nuances of how different research areas develop and shift. Our interactive visualizations will allow users to explore trends dynamically, enhancing their understanding of the academic landscape.  
To ensure feasibility within our time constraints, we will concentrate on a specific research domain, allowing for in-depth analysis. Our goal is to create a comprehensive tool that not only provides valuable insights into citation dynamics but also contributes to the academic community by fostering a deeper understanding of research impact and future directions. Ultimately, our project aims to empower researchers and institutions to make informed decisions based on evolving research trends.

## How to set up the application

1. Create the Neo4j database (e.g. Neo4j desktop)
2. Seed the test data with graph_database_setup/4_RUN_THIS_upload_sampled_data_to_Neo4j.ipynb
3. Create `backend/.env` by copying `backend/.env.example`
4. Set `OPENAI_API_KEY` in `backend/.env`
5. Install backend dependencies (e.g. pip install -r requirements.txt)
6. Run Python backend server (e.g. python main.py)
7. Update the server URL at frontend/research-trend-analysis/components/custom/chat.tsx > handleSubmit
8. Run Nextjs app (pnpm dev)
9. Run python programs to visualize data (e.g. python3 visualization/top_10.py)

## Applicaiton Components:

- Data visualization
  - visualize the relationship between information in the GraphDB
- Frontend UI
  - enable user to interact with application
- Build GraphDB with Dataset
  - Use OpenSource tool like LangChain or other LLM to build RAG system
- Builld RAG based LLM application
  - fetch data from GraphDB
  - augment response with data

## Team Members:

- Aryan Ravishankar: aryanr2
- Hiroyuki Momoi: hmomoi2
- Sally Yang: hsiuchu2
- Skyler Lehto: lehto2
