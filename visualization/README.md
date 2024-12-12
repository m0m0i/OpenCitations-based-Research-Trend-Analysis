# Graph Visualization Scripts

These scripts use libraries such as pandas, networkx, and matplotlib to create graphs that visualize citation data and the relationships between authors, publications, and venues.

## Getting Started

First, install the required dependencies:

- pandas
- matplotlib
- networkx
- mplcursors

## Files in this Repository

1. top_10.py

- Description: Visualizes the top 10 authors..
- Graph Details:
- Nodes represent authors.
- Node size is proportional to the volume.
- Nodes are positioned along the x-axis based on their first publication year.

2. publication_for_single_author.py

- Description: Visualizes all publications for a single author.
- Graph Details:
- A central node represents the author.
- Connected nodes represent their publications.
- Node size is proportional to volume.

3. top_authors_and_their_top_publications.py

- Description: Displays the top 5 authors and their top 10 publications.
- Graph Details:
- Author nodes are connected to their top publications.
- Node size is proportional to volume.
- Each author is assigned a unique color for better visualization.

4. author_in_venue.py

- Description: Visualizes authors who have published in a specific venue.
- Graph Details:
- Nodes represent authors who have published in that venue.
- Nodes are scattered along the y-axis to avoid overlap
- Nodes are positioned along the x-axis based on their first publication year.

5. citing.py

- Description: Visualizes citing relationships for a specific cited publication.
- Graph Details:
- The cited publication is represented as a red-orange node.
- Citing publications are represented as blue nodes connected by edges.
- Nodes are positioned along the x-axis based on their publication year and scattered along the y-axis for clarity.
