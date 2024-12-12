import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import mplcursors

# Load the CSV file
df = pd.read_csv('../graph_database_setup/sampled_citations_metadata_clean.csv')

var1 = 'volume'
var2 = 'author'

# Convert var1 column to numeric, coercing errors to NaN
df[var1] = pd.to_numeric(df[var1], errors='coerce')

# Drop rows with NaN values in var1
df = df.dropna(subset=[var1])

# Split authors into lists and fill NaN values
df[var2] = df[var2].fillna('').apply(lambda x: x.split(', ') if isinstance(x, str) else [])

# Calculate total citations per author
author_citations = df.explode(var2).groupby(var2)[var1].sum().nlargest(5)
top_authors = author_citations.index.tolist()

# Filter for top 5 authors
filtered_df = df[df[var2].apply(lambda authors: any(author in top_authors for author in authors))]

# Get top 10 most cited publications for each author
top_publications = filtered_df.explode(var2).groupby(['title', var2])[var1].sum().reset_index()
top_publications = top_publications[top_publications[var2].isin(top_authors)]
top_publications = top_publications.groupby(var2).apply(lambda x: x.nlargest(10, var1)).reset_index(drop=True)

# Create graph
G = nx.Graph()

# Define a modern color palette for authors
author_colors = ['#FF6F61', '#6BAED6', '#74C476', '#9E9AC8', '#FDAE6B']

# Add author nodes with colors
for i, author in enumerate(top_authors):
    G.add_node(author, type=var2, color=author_colors[i])

# Add publication nodes, edges, and their sizes
for _, row in top_publications.iterrows():
    title = row['title']
    volume = row[var1]
    author = row[var2]
    node_size = max(volume / 5, 100)  # Adjust scaling if necessary
    G.add_node(title, type='publication', volume=volume, size=node_size, color='#C0C0C0')  # Light gray for publications
    G.add_edge(author, title, color=author_colors[top_authors.index(author)])

# Prepare data for visualization
node_sizes = [G.nodes[node].get('size', 100) for node in G]
node_colors = [G.nodes[node]['color'] for node in G]
edge_colors = [G.edges[edge]['color'] for edge in G.edges]

# Draw the graph
plt.figure(figsize=(14, 10))
pos = nx.spring_layout(G, k=0.8, seed=42)  # Spring layout with fixed seed for consistency

# Draw nodes and edges
nodes = nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=node_sizes, alpha=0.9)
edges = nx.draw_networkx_edges(G, pos, edge_color=edge_colors, width=2, alpha=0.7)

# Draw labels for author nodes only
nx.draw_networkx_labels(G, pos, labels={node: node for node in G if G.nodes[node]['type'] == var2}, font_size=12, font_weight='bold')

# Add a legend for authors
plt.legend(
    handles=[plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color, markersize=10) for color in author_colors],
    labels=top_authors,
    title="Authors",
    loc="upper left",
    frameon=True,
    fontsize=10,
    title_fontsize=12,
)

# Set graph title
plt.title('Top Authors and Their Most Cited Publications', fontsize=16, fontweight='bold')

# Add tooltips using mplcursors for publication titles only
cursor = mplcursors.cursor(nodes, hover=True)
cursor.connect("add", lambda sel: sel.annotation.set_text(
    list(G.nodes)[sel.index] if G.nodes[list(G.nodes)[sel.index]]['type'] == 'publication' else ''
))

# Show the graph
plt.axis('off')
plt.tight_layout()
plt.show()
