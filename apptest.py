import streamlit as st

st.set_page_config(page_title="Test ChunkFive", page_icon="🍫")
# Inyectar la fuente .ttf personalizada
st.markdown("""
    <style>
    @font-face {
        font-family: 'ChunkFive';
        src: url('/static/chunk.ttf') format('truetype');
        font-weight: normal;
        font-style: normal;
    }

    html, body, .stApp {
        font-family: 'ChunkFive', sans-serif !important;
    }

    .plotly-graph-div * {
        font-family: 'ChunkFive', sans-serif !important;
    }

    h1, h2, h3, h4, h5, h6 {
        font-family: 'ChunkFive', sans-serif !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🍫 Welcome with ChunkFive")
st.markdown("### 🔠 If you see this text in ChunkFive... it worked! 🎉")
