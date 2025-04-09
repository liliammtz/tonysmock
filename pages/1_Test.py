import streamlit as st
import pandas as pd
from PIL import Image
from io import BytesIO
import base64

# ====================== CONFIG ======================
st.set_page_config(page_title="Chocolate Flip Cards", page_icon="🍫", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Alfa+Slab+One&display=swap');

    body, html, .stApp {
        font-family: 'Alfa Slab One', sans-serif !important;
        background-color: #fff9f5;
    }

    .block-container {
        padding-top: 2rem;
    }

    .flip-card {
        perspective: 1000px;
        margin: 1.5rem auto;
        display: flex;
        justify-content: center;
    }

    .flip-card-inner {
        position: relative;
        width: 100%;
        max-width: 300px;
        aspect-ratio: 954 / 511;
        transition: transform 0.8s;
        transform-style: preserve-3d;
    }

    .flip-card:hover .flip-card-inner {
        transform: rotateY(180deg);
    }

    .flip-card-front, .flip-card-back {
        position: absolute;
        width: 100%;
        height: 100%;
        backface-visibility: hidden;
        border-radius: 15px;
        box-shadow: 3px 3px 12px rgba(0,0,0,0.1);
        overflow: hidden;
        font-family: 'Alfa Slab One', sans-serif !important;
    }

    .flip-card-front {
        background-color: #ffffff;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .flip-card-front img {
        width: 100%;
        height: 100%;
        object-fit: contain;
    }

    .flip-card-back {
        background-color: #eb2c2d;
        color: white;
        transform: rotateY(180deg);
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        font-size: 18px;
        padding: 1rem;
        text-align: center;
        font-family: 'Alfa Slab One', sans-serif !important;
    }

    .flip-card-back div {
        margin: 0.4rem 0;
    }

    h1, h2, h3, h4, h5, h6, .css-18ni7ap, .css-1d391kg, .plotly-graph-div * {
        font-family: 'Alfa Slab One', sans-serif !important;
        font-weight: normal !important;
    }
    </style>
""", unsafe_allow_html=True)


# ====================== DATA ======================
@st.cache_data
def load_data():
    return pd.read_csv("Database.csv", parse_dates=["Date"])

def image_to_base64(path):
    try:
        img = Image.open(path)
        buffered = BytesIO()
        img.save(buffered, format="WEBP")
        img_b64 = base64.b64encode(buffered.getvalue()).decode()
        return f"data:image/webp;base64,{img_b64}"
    except Exception as e:
        st.error(f"Error loading {path}: {e}")
        return ""

df = load_data()

photos = df.groupby(['ProductID','PhotoId','ProductName','Category'])['CostPerUnit'].mean().reset_index()

# ====================== UI ======================
st.title("🍫 Flip-Card Chocolate Catalog")

chunk_size = 3

for i in range(0, len(photos), chunk_size):
    row_chunk = photos.iloc[i:i+chunk_size]
    cols = st.columns(len(row_chunk))

    for col, (_, row) in zip(cols, row_chunk.iterrows()):
        image_path = f"static/images/{row['PhotoId']}"
        image_base64 = image_to_base64(image_path)

        if image_base64:
            with col:
                st.markdown(f"""
                    <div class="flip-card">
                        <div class="flip-card-inner">
                            <div class="flip-card-front">
                                <img src="{image_base64}">
                            </div>
                            <div class="flip-card-back">
                                <div><b>{row['ProductName']}</b></div>
                                <div>📦 {row['Category']}</div>
                                <div>💲{row['CostPerUnit']:.2f} USD</div>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
