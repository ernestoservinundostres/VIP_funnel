import pandas as pd
import plotly.graph_objects as go
import numpy as np
import matplotlib.cm as cm
import matplotlib.colors as mcolors

# Load the example files
prev_df = pd.read_csv('/Users/claudiaeenriquezgracia/Downloads/logs_202310_prev.csv')
post_df = pd.read_csv('/Users/claudiaeenriquezgracia/Downloads/202310_post.txt', sep='\t')
post1_df = pd.read_csv('/Users/claudiaeenriquezgracia/Downloads/202310_post1.txt', sep='\t')
print(post1_df['Target'].dtype)
post1_df['Target'] = post1_df['Target'].astype(str) + '_post'

# Define the pivotal node
pivotal_action = "Click on Button for purchase membership"

# Extract nodes from prev actions and append the pivotal node
nodes_prev = list(prev_df['prev_action']) + [pivotal_action]

# Extract unique nodes from post and post1 (combining Source and Target)
nodes_post = np.unique(post_df[['Source', 'Target']].values)
nodes_post1 = np.unique(post1_df[['Source', 'Target']].values)

# Combine and ensure unique nodes across all datasets
all_nodes = np.unique(np.concatenate((nodes_prev, nodes_post, nodes_post1)))

# Generate colors for nodes using matplotlib
def gen_colors(n, cmap_name='nipy_spectral'):
    cmap = cm.get_cmap(cmap_name, n)
    colors = [mcolors.rgb2hex(cmap(i)) for i in range(n)]
    return colors

colors = gen_colors(len(all_nodes))

# Map nodes to their indices for easy lookup
node_indices = {node: idx for idx, node in enumerate(all_nodes)}

# Initialize list of links
links = []

# Links from prev actions to pivotal node
for _, row in prev_df.iterrows():
    links.append({
        'source': node_indices[row['prev_action']],
        'target': node_indices[pivotal_action],
        'value': row['num_actions']
    })

# Links from pivotal node to post actions
for _, row in post_df.iterrows():
    links.append({
        'source': node_indices[pivotal_action],
        'target': node_indices[row['Target']],
        'value': row['Clicks']
    })

# Links from post actions to post1 actions
for _, row in post1_df.iterrows():
    if row['Source'] in node_indices and row['Target'] in node_indices:
        links.append({
            'source': node_indices[row['Source']],
            'target': node_indices[row['Target']],
            'value': row['Clicks']
        })

# Create the Sankey diagram
fig = go.Figure(data=[go.Sankey(
    arrangement='snap',
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.3),
        label=list(all_nodes),
        color=colors
    ),
    link=dict(
        source=[link['source'] for link in links],
        target=[link['target'] for link in links],
        value=[link['value'] for link in links],
        color=[colors[link['source']] for link in links]  # Use source node color for links
    )
)])

fig.update_layout(title_text="VIP Funnel - October 2023", font_size=10, height=800, width=1000)
fig.show()
print(post1_df['Target'].head())
