import streamlit as st

st.set_page_config(page_title="Chocolate Dashboard", page_icon="🍫")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Alfa+Slab+One&display=swap');

    html, body, .stApp {
        font-family: 'Alfa Slab One', sans-serif !important;
    }

    .plotly-graph-div * {
        font-family: 'Alfa Slab One', sans-serif !important;
    }

    h1, h2, h3, h4, h5, h6 {
        font-family: 'Alfa Slab One', sans-serif !important;
        font-weight: normal !important;
    }
    </style>
""", unsafe_allow_html=True)


st.title("🍫 Welcome to the Chocolate Sales Dashboard - 2023")

st.markdown("""
This dashboard was created for portfolio purposes only.

> ⚠️ **Disclaimer:** All sales data presented here is **entirely fictional**.  
> Categories, promotions, and sales channels were inspired by the brand **Tony’s Chocolonely**,  
> but none of the data reflects actual figures or is affiliated with the company.

Designed and developed by **Liliam Martínez** as part of her personal data analysis and interactive dashboard portfolio using Streamlit.
""")
