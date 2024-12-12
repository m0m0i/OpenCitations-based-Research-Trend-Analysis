import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import mplcursors

# Load the CSV file
df = pd.read_csv('../graph_database_setup/sampled_citations_metadata_clean .csv')

var1 = 'volume'
var2 = 'author'

# Convert var1 column to numeric, coercing errors to NaN
df[var1] = pd.to_numeric(df[var1], errors='coerce')

# Drop rows with NaN values in var1
df = df.dropna(subset=[var1])

# Split authors into lists and fill NaN values
df[var2] = df[var2].fillna('').apply(lambda x: x.split(', ') if isinstance(x, str) else [])

# Filter for a single author (e.g., "Zhao")
selected_author = "Zhao"
filtered_df = df[df[var2].apply(lambda authors: selected_author in authors)]

# Get all publications and their citation volumes for the selected author
publications = filtered_df.explode(var2).groupby(['title', var2])[var1].sum().reset_index()
publications = publications[publications[var2] == selected_author]

# Create graph
G = nx.Graph()

# Add author node
G.add_node(selected_author, type=var2, size=500, color='#FF6F61')  # Modern red for the author node

# Add publication nodes and edges
for _, row in publications.iterrows():
    title = row['title']
    volume = row[var1]
    G.add_node(title, type='publication', size=max(volume / 5, 50), color='#6BAED6')  # Modern blue for publication nodes
    G.add_edge(selected_author, title, color='#9E9AC8')  # Edge color in modern purple

# Prepare data for visualization
pos = nx.spring_layout(G, k=0.6, seed=42)  # Consistent layout with controlled spacing
node_sizes = [G.nodes[node]['size'] for node in G]
node_colors = [G.nodes[node]['color'] for node in G]
edge_colors = [G.edges[edge]['color'] for edge in G.edges]

# Draw the graph
plt.figure(figsize=(14, 10))
nodes = nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=node_sizes, alpha=0.9)
edges = nx.draw_networkx_edges(G, pos, edge_color=edge_colors, width=2, alpha=0.7)

# Draw labels for the author and publications
nx.draw_networkx_labels(
    G, pos,
    labels={node: node if G.nodes[node]['type'] == var2 else '' for node in G},
    font_size=14, font_weight='bold', verticalalignment='bottom'
)

# Title and layout improvements
plt.title(f"Publications of {selected_author}", fontsize=16, fontweight='bold')
plt.axis('off')
plt.tight_layout()

# Add tooltips using mplcursors for publication titles
cursor = mplcursors.cursor(nodes, hover=True)

def on_hover(sel):
    hovered_node = list(G.nodes)[sel.index]
    if G.nodes[hovered_node]['type'] == 'publication':
        sel.annotation.set_text(hovered_node)
    else:
        sel.annotation.set_text('')  # Hide tooltip for non-publication nodes

cursor.connect("add", on_hover)

# Show the graph
plt.show()
