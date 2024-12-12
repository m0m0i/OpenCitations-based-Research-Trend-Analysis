import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import mplcursors

# Load the CSV file
df = pd.read_csv('../graph_database_setup/sampled_citations_metadata_clean.csv')

var1 = 'volume'
var2 = 'pub_year'
var3 = 'author'

# Convert var1 and var2 columns to numeric, handling errors
df[var1] = pd.to_numeric(df[var1], errors='coerce')
df[var2] = pd.to_numeric(df[var2], errors='coerce')

# Drop rows with NaN values in var1 or var2
df.dropna(subset=[var1, var2], inplace=True)

# Split authors into lists and handle missing values
df[var3] = df[var3].fillna('').apply(lambda x: x.split(', ') if isinstance(x, str) else [])

# Explode authors into separate rows and calculate total volume per author
author_citations = df.explode(var3).groupby(var3)[var1].sum().nlargest(10)
top_authors = author_citations.index.tolist()

# Filter for top 10 authors and get their first publication year
filtered_df = df[df[var3].apply(lambda authors: any(author in top_authors for author in authors))]
first_pub_years = (
    filtered_df.explode(var3)
    .groupby(var3)[var2]
    .min()
    .loc[top_authors]
)

# Create a graph
G = nx.Graph()

# Add nodes for each top author with size based on citation volume and x-axis based on first pub_year
for author in top_authors:
    G.add_node(
        author,
        type=var3,
        size=author_citations[author] / 10,  # Scale node size for better visualization
        color='#4CAF50',  # Modern green color for nodes
        pub_year=first_pub_years[author]
    )

# Prepare positions for nodes based on first publication year (x-axis)
pos = {}
y_offset = 0

for node in G.nodes:
    pub_year = G.nodes[node][var2]
    pos[node] = (pub_year, y_offset)  # Scatter nodes along the y-axis to avoid overlap
    y_offset += 1

# Extract node attributes for visualization
node_sizes = [G.nodes[node]['size'] for node in G]
node_colors = [G.nodes[node]['color'] for node in G]

# Draw the graph with a modern style
plt.figure(figsize=(14, 8))
nodes = nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=node_sizes, alpha=0.9)
nx.draw_networkx_labels(G, pos, labels={node: node for node in G}, font_size=10, font_family='sans-serif')

# Add title and axis labels
plt.title('Top 10 Authors by Citation Volume', fontsize=16, fontweight='bold', color='#333333')
plt.xlabel("Year", fontsize=12, labelpad=10, color='#333333')  # Explicitly label x-axis as "Year"

# Add x-axis ticks and gridlines for clarity
years = sorted(first_pub_years.unique())
plt.xticks(years, rotation=45)
plt.grid(axis='x', linestyle='--', alpha=0.5)

plt.axis('on')  # Show axes explicitly
plt.tight_layout()

# Add interactive tooltips using mplcursors
cursor = mplcursors.cursor(nodes, hover=True)

def on_hover(sel):
    hovered_node = list(G.nodes)[sel.index]
    sel.annotation.set_text(f"{hovered_node}\nVolume: {int(author_citations[hovered_node])}")

cursor.connect("add", on_hover)

# Display the graph
plt.show()
