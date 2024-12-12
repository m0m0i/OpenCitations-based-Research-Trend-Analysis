import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import random

# Load the CSV files
citations_df = pd.read_csv('../graph_database_setup/sampled_citations.csv')
metadata_df = pd.read_csv('../graph_database_setup/sampled_citations_metadata_clean .csv')

# Normalize IDs to ensure consistent lookup
citations_df['cited'] = citations_df['cited'].str.strip()
citations_df['citing'] = citations_df['citing'].str.strip()
metadata_df['id'] = metadata_df['id'].str.strip()

# Extract the first part of the metadata IDs
metadata_df['id_first'] = metadata_df['id'].str.split().str[0]

# Create mappings for titles and publication years
id_to_title = metadata_df.set_index('id_first')['title'].to_dict()
id_to_year = metadata_df.set_index('id_first')['pub_year'].to_dict()

# Filter rows where 'cited' equals the specific ID
cited_id = "omid:br/06701357266"
cited_title = id_to_title.get(cited_id, cited_id)  # Get the title or fallback to ID
cited_year = id_to_year.get(cited_id, None)  # Get the pub_year or None if missing

# Filter rows for citations of the specified ID
filtered_citations = citations_df[citations_df['cited'] == cited_id].copy()

# Map citing IDs to their titles and publication years
filtered_citations['citing_title'] = filtered_citations['citing'].map(id_to_title)
filtered_citations['citing_year'] = filtered_citations['citing'].map(id_to_year)

# Fallback to ID if the title is missing
filtered_citations['citing_title'] = filtered_citations['citing_title'].fillna(filtered_citations['citing'])

# Create a directed graph
G = nx.DiGraph()

# Add the cited publication node
G.add_node(cited_id, label=cited_title, color='#FF5733', year=cited_year)  # Red-orange for the main node

# Add citing publication nodes and edges
for _, row in filtered_citations.iterrows():
    citing_id = row['citing']
    citing_title = row['citing_title']
    citing_year = row['citing_year']
    G.add_node(citing_id, label=citing_title, color='#3498DB', year=citing_year)  # Blue for citing nodes
    G.add_edge(cited_id, citing_id, color='#95A5A6')  # Gray for edges

# Extract node attributes for visualization
node_labels = {node: f"{G.nodes[node]['label']}\n({G.nodes[node]['year']})" for node in G}  # Title and Year
node_colors = [G.nodes[node]['color'] for node in G]
edge_colors = [G.edges[edge]['color'] for edge in G.edges]
node_years = {node: int(year) if pd.notnull(year) else None for node, year in nx.get_node_attributes(G, 'year').items()}

# Sort unique years in ascending order
unique_years = sorted({year for year in node_years.values() if year is not None})  # Ignore None values

# Create a mapping of year to x position
year_to_x = {year: i for i, year in enumerate(unique_years)}

# Evenly distribute y positions
y_positions = {node: i * 3.0 for i, node in enumerate(G.nodes)}

# Calculate node positions based on year and evenly scatter along y-axis
pos = {}
for node, year in node_years.items():
    x = year_to_x[year] if year is not None else 0
    y = y_positions[node]
    pos[node] = (x, y)

# Draw the graph with a modern style
plt.figure(figsize=(16, 10))
nx.draw(
    G,
    pos,
    with_labels=True,
    labels=node_labels,  # Use title and year as label
    node_color=node_colors,
    edge_color=edge_colors,
    node_size=1200,  # Slightly larger nodes for emphasis
    font_size=10,  # Larger font size for better readability
    font_weight='bold',
    arrowsize=20,
    alpha=0.9  # Slight transparency for modern aesthetic
)

# Set graph title and axis labels
plt.title(f"Citing Relationship for '{cited_title}'", fontsize=20, color='#2C3E50')  # Dark gray title
plt.xlabel("Year", fontsize=16, color='#2C3E50')
plt.ylabel("Publication (Vertical Spacing)", fontsize=16, color='#2C3E50')

# Set x-axis as years
plt.xticks(range(len(unique_years)), unique_years, rotation=45, fontsize=12, color='#34495E')  # Use unique years as ticks
plt.grid(axis='x', linestyle='--', alpha=0.5, color='#BDC3C7')

# Add a legend for colors
plt.legend(handles=[
    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#FF5733', markersize=10, label='Cited Publication'),
    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#3498DB', markersize=10, label='Citing Publications')
], loc='upper right', fontsize=12)

# Show the plot
plt.show()
