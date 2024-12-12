# OpenCitations Data Processing and Upload to Neo4j

This repository contains a series of Jupyter Notebooks and CSV files for processing and filtering OpenCitations citation data and metadata. The processed data is stored in two CSV files, one for citations and one for metadata, which are meant to be uploaded into a local Neo4j database. The final notebook also guides the process of creating nodes and relationships within Neo4j based on the processed data.

## Files

### Jupyter Notebooks:
-  **1_OpenCitations_data_processing_part_1.ipynb**  
   This notebook compiles an extract of raw citation and metadata files and prepares it for further filtering and processing in later steps. It includes initial data cleaning and pre-processing tasks.

-  **2_OpenCitations_data_processing_part_2.ipynb**  
   This notebook continues the processing pipeline, refining the data further by sampling certain records and iteratively selecting other records based on citation connections.

-  **3_Clean_sampled_citations_metadata.ipynb**  
   This notebook processes and cleans the metadata associated with the sampled citations. It ensures the metadata is in a format suitable for uploading to Neo4j.

-  **4_RUN_THIS_upload_sampled_data_to_Neo4j.ipynb**  
   This notebook is the final step in the pipeline. It loads the processed citation and metadata CSV files into a local Neo4j database. It also creates the necessary nodes and relationships in the database, allowing you to visualize and analyze the citation graph.

### CSV Files:
- **sampled_citations.csv**  
  This file contains the processed citation data. It is formatted for easy ingestion into a Neo4j graph database and includes the relevant citation details.

- **sampled_citations_metadata_clean.csv**  
  This file contains the cleaned metadata associated with the citations. It is also formatted for uploading into Neo4j, where it will be used to create metadata nodes.

## How to Use

### Prerequisites:
- A locally installed Neo4j Desktop application. You can follow the [official Neo4j Desktop installation guide](https://neo4j.com/docs/operations-manual/current/installation/neo4j-desktop/) to get started if you don't have Neo4j installed yet.

### Steps:
1. **Optional (not recommended): Run Notebooks 1, 2, and 3:**  
   Included for historical provenance purposes--does not need to be repeated, as they are very time consuming. Each notebook refines the data, with the final product being two CSV files (included in the repository):
   - `sampled_citations.csv`
   - `sampled_citations_metadata_clean.csv`
  
2. **Add a local DBMS on Neo4j Desktop**
   - You will need to create a password, and use this password in the next notebook.

3. **Upload Data to Neo4j:**  
   Open and run notebook **4_RUN_THIS_upload_sampled_data_to_Neo4j.ipynb**. This notebook will:
   - Upload the data from `sampled_citations.csv` and `sampled_citations_metadata_clean.csv` to your local Neo4j instance.
      - Notebook assumes these files are saved in the same folder as the notebook itself.
   - Create nodes for citations and metadata, and establish relationships between them, based on the citation references.

4. **Explore the Neo4j Database:**  
   Once the data is uploaded, you can use Neo4j's Cypher query language to explore the graph. For example, you can visualize the citation relationships and metadata associated with the nodes.

### Example Cypher Queries:
Here are a few Cypher queries you can run in the Neo4j browser to explore the uploaded data:
- Show author nodes:
  ```cypher
  MATCH (c:Author) RETURN c LIMIT 25;
  ```
- Show publication nodes:
  ```cypher
  MATCH (m:Publication) RETURN m LIMIT 25;
  ```
- Show authored relationships:
  ```cypher
  MATCH p=()-[r:AUTHORED]->() RETURN p LIMIT 25;
  ```
- Show cited relationships:
  ```cypher
  MATCH p=()-[r:CITED]->() RETURN p LIMIT 25;
  ```

## Notes:
- Ensure that Neo4j is running on the default port (`localhost:7687`) before running the upload notebook.
- Modify the Neo4j connection parameters in the `4_RUN_THIS_upload_sampled_data_to_Neo4j.ipynb` notebook if your setup uses custom connection details (e.g., password, different host).
- Feel free to form additional nodes and relationships among the data, either by modifying the Jupyter notebook, or running the Cypher queries directly on Neo4j Desktop.
