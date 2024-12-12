import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import mplcursors

# Load the CSV file
df = pd.read_csv('../graph_database_setup/sampled_citations_metadata_clean.csv')

var1 = 'volume'
var2 = 'venue'
var3 = 'pub_year'

# Convert var1 column to numeric, handling errors
df[var1] = pd.to_numeric(df[var1], errors='coerce')

# Drop rows with NaN values in var1
df.dropna(subset=[var1], inplace=True)

# Split venues into lists and handle missing values
df[var2] = df[var2].fillna('').apply(lambda x: x.split(', ') if isinstance(x, str) else [])

# Filter publications for a specific venue (e.g., "Lipids")
selected_venue = "Lipids"
filtered_df = df[df[var2].apply(lambda venues: selected_venue in venues)]

# Aggregate citation volumes for publications by the selected venue
publications = (
    filtered_df.groupby(['title', var3])[var1]
    .sum()
    .reset_index()
)

# Ensure var3 is integer for proper positioning
publications[var3] = publications[var3].astype(int)

# Sort publications by publication year
publications.sort_values(by=var3, inplace=True)

# Create the graph
G = nx.Graph()

# Add venue node
G.add_node(
    selected_venue,
    type=var2,
    size=300,
    color='#FF6F61'  # Bold red for the venue node
)

# Add publication nodes and edges
for _, row in publications.iterrows():
    title = row['title']
    volume = row[var1]
    pub_year = row[var3]
    G.add_node(
        title,
        type='publication',
        size=max(volume / 10, 50),  # Scale node size based on volume
        color='#4CAF50',  # Modern green for publication nodes
        pub_year=pub_year
    )

# Prepare positions for nodes based on publication year (x-axis)
pos = {}
y_positions = {}  # Track y-positions for each x to avoid overlap

def get_y_offset(x):
    """Get the next available y position for a given x."""
    if x not in y_positions:
        y_positions[x] = 0
    else:
        y_positions[x] += 1
    return y_positions[x]

for node in G.nodes:
    if G.nodes[node]['type'] == 'publication':
        pub_year = G.nodes[node][var3]
        pos[node] = (pub_year, get_y_offset(pub_year))  # Scatter on y-axis with x-axis as pub_year
    else:
        pos[node] = (min(publications[var3]) - 1, 0)  # Venue node on the leftmost side

# Extract node attributes for visualization
node_sizes = [G.nodes[node]['size'] for node in G]
node_colors = [G.nodes[node]['color'] for node in G]

# Draw the graph with a modern color palette
plt.figure(figsize=(14, 8))
nodes = nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=node_sizes, alpha=0.9)
edges = nx.draw_networkx_edges(G, pos, edge_color='#9E9AC8', width=2, alpha=0.7)  # Modern purple edges

# Draw labels for nodes (only show venue name and publication titles)
nx.draw_networkx_labels(
    G,
    pos,
    labels={node: node if G.nodes[node]['type'] == var2 else '' for node in G},
    font_size=12,
    font_family='sans-serif',
    font_weight='bold'
)

# Add title and axis labels
plt.title(f'Publications in {selected_venue} by Year', fontsize=16, fontweight='bold', color='#333333')
plt.xlabel("Publication Year", fontsize=12, labelpad=10, color='#333333')
plt.ylabel("Scattered Y-Axis (Avoiding Overlap)", fontsize=12, labelpad=10, color='#333333')
plt.xticks(rotation=45)
plt.axis('off')
plt.tight_layout()

# Add interactive tooltips using mplcursors
cursor = mplcursors.cursor(nodes, hover=True)

def on_hover(sel):
    hovered_node = list(G.nodes)[sel.index]
    sel.annotation.set_text(hovered_node)

cursor.connect("add", on_hover)

# Display the graph
plt.show()