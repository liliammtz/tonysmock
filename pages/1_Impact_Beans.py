import streamlit as st
import pandas as pd
import plotly.express as px

# -------- CONFIGURACIÓN DE PÁGINA --------
st.set_page_config(page_title="Impact Beans", page_icon="🌱", layout="wide")

# -------- FUENTE Y ESTILOS --------
st.markdown("""
    <style>
    @font-face {
        font-family: 'ChunkFive';
        src: url('/static/ChunkFive.woff') format('woff');
    }

    body, html, .stApp {
        font-family: 'ChunkFive', sans-serif !important;
        background-color: #fff9f5;
    }

    .block-container {
        padding-top: 2rem;
    }

    h1, h2, h3, h4, h5, h6, .css-18ni7ap, .css-1d391kg, .plotly-graph-div * {
        font-family: 'ChunkFive', sans-serif !important;
    }
    </style>
""", unsafe_allow_html=True)

# -------- CARGAR DATOS --------
@st.cache_data
def load_data():
    return pd.read_csv("Database.csv", parse_dates=["Date"])

df = load_data()

# Verificar que las columnas existan
required_cols = {"Category", "ImpactBeans", "ProductName", "CostPerUnit"}
if not required_cols.issubset(df.columns):
    st.error(f"🚫 El archivo no contiene las columnas necesarias: {required_cols}")
    st.stop()

# -------- TÍTULO --------
st.title("🌱 Impact Beans vs Chocolate Type")

st.markdown("""
This visualization shows how the *Impact Beans* score varies by chocolate type.

Each dot represents a specific chocolate product and its ethical/sustainability score.
""")

# -------- GRAFICA STRIP PLOT --------
fig = px.strip(
    df,
    x="Category",
    y="ImpactBeans",
    color="Category",
    hover_name="ProductName",
    title="Impact Beans Distribution by Chocolate Type",
    stripmode="overlay",
    #!jitter=0.4,
    labels={"ImpactBeans": "Impact Beans", "Category": "Chocolate Type"},
    color_discrete_sequence=px.colors.qualitative.Bold
)

fig.update_traces(
    marker=dict(size=16, line=dict(width=1, color='black'), symbol='circle'),
    selector=dict(mode='markers')
)

fig.update_layout(
    plot_bgcolor="#fff9f5",
    paper_bgcolor="#fff9f5",
    font=dict(family="ChunkFive", size=18),
    title_x=0.3,
    margin=dict(t=60, b=40)
)

st.plotly_chart(fig, use_container_width=True)
