import pandas as pd 
import streamlit as st
import plotly.graph_objects as go
from mycolorpy import colorlist as mcp

st.set_page_config(layout="wide")

st.title('VIP Funnel')


option = st.selectbox(
    'Mes',
    ('Octubre','Noviembre','Diciembre', 'Enero'))
if option == 'Octubre':
    df = pd.read_csv('Fil/logs_202310_prev.csv')
elif option == 'Noviembre':
    df = pd.read_csv('Fil/logs_202311_prev.csv')
if option == 'Diciembre':
    df = pd.read_csv('Fil/logs_202312_prev.csv')
if option == 'Enero':
    df = pd.read_csv('Fil/logs_202401_prev.csv')




nodes = list(df.prev_action)
colors =mcp.gen_color(cmap="cool",n=len(nodes))
nodes.append('Click on Button for purchase membership')
links = []
for i in list(df.index):
    links.append({'source': i, 'target': len(nodes)-1, 'value': df.num_actions[i], 'color': colors[i]})

# Create figure
fig = go.Figure(data=[go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.3),
        label=nodes
    ),
    link=dict(
        source=[link['source'] for link in links],
        target=[link['target'] for link in links],
        value=[link['value'] for link in links], color =[link['color'] for link in links]
    ),
)],)

# Update layout
fig.update_layout(title_text=option, font_size=15, autosize=False, width=1500, height=1000)
# fig.show()
# st.dataframe(df,use_container_width=True)
df.rename(columns= {'num_actions':'# Clicks','prev_action':'Acción previa'}, inplace = True)

st.markdown(df.style.hide(axis="index").to_html(), unsafe_allow_html=True)

st.plotly_chart(fig, use_container_width=True)
