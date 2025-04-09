import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from PIL import Image
import base64
from io import BytesIO

# Configurar la página
st.set_page_config(page_title="Chocolate Showcase", page_icon="🍫", layout="wide")

# Fuente y estilos tipo vitrina
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

    .product-block {
        text-align: center;
        margin-bottom: 2em;
    }

    .product-block img {
        border-radius: 15px;
        box-shadow: 3px 3px 10px rgba(0,0,0,0.15);
        transition: transform 0.3s ease;
    }

    .product-block img:hover {
        transform: scale(1.05);
    }

    .product-name {
        font-size: 20px;
        margin-top: 0.4em;
        color: #eb2c2d;
    }

    .product-info {
        font-size: 16px;
        color: #333;
        margin-top: 0.2em;
    }

    .section-header {
        background: #eb2c2d;
        color: white;
        padding: 0.5em 1em;
        border-radius: 20px;
        font-size: 26px;
        display: inline-block;
        margin-bottom: 1em;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.2);
    }
    </style>
""", unsafe_allow_html=True)

# Cargar datos
@st.cache_data
def load_data():
    return pd.read_csv("Database.csv", parse_dates=["Date"])

df = load_data()

# Preprocesar
df = df.dropna(subset=["Category", "PhotoId", "ProductID", "CostPerUnit", "CocoaPercentage"])
df["CocoaPercentage"] = (
    df["CocoaPercentage"].astype(str).str.replace('%', '').astype(float)
)

df = df.value_counts(["Category", "PhotoId", "ProductID", "CostPerUnit", "CocoaPercentage"]).reset_index()

# Agrupar por categoría
categories = df["Category"].unique()

# Función para convertir imagen a base64
def image_to_base64(path):
    img = Image.open(path)
    buffered = BytesIO()
    img.save(buffered, format="WEBP")  # o "PNG" si es PNG
    img_b64 = base64.b64encode(buffered.getvalue()).decode()
    return f"data:image/webp;base64,{img_b64}"


for category in categories:
    st.markdown(f"<div class='section-header'>🍫 {category}</div>", unsafe_allow_html=True)

    # Filtrar y ordenar por CocoaPercentage (opcional)
    filtered = df[df["Category"] == category].sort_values(by="CocoaPercentage", ascending=True)

    cols = st.columns(5)

    #!for idx, row in filtered.iterrows():
    #!    image_path = f"static/images/{row['PhotoId']}"
    #!    col = cols[idx % 5]
    #!    with col:
    #!        st.markdown(f"""
    #!            <div class="product-block">
    #!                <img src="{image_to_base64(image_path)}" width="100%">
    #!                <div class="product-name">{row['ProductID']}</div>
    #!                <div class="product-info">Cocoa: {row['CocoaPercentage']}%</div>
    #!                <div class="product-info">💲{row['CostPerUnit']:.2f} USD</div>
    #!            </div>
    #!        """, unsafe_allow_html=True)
#!
#!
    #!        # Agrupar productos en filas de 5
    for i in range(0, len(filtered), 5):
        row_products = filtered.iloc[i:i+5]
        cols = st.columns(5)

        for col, (_, row) in zip(cols, row_products.iterrows()):
            image_path = f"static/images/{row['PhotoId']}"
            with col:
                st.markdown(f"""
                    <div class="product-block">
                        <img src="{image_to_base64(image_path)}" width="100%">
                        <div class="product-name">{row['ProductID']}</div>
                        <div class="product-info">Cocoa: {row['CocoaPercentage']}%</div>
                        <div class="product-info">💲{row['CostPerUnit']:.2f} USD</div>
                    </div>
                """, unsafe_allow_html=True)

