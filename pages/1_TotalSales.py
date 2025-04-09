import streamlit as st
import pandas as pd
import plotly.express as px

# Configurar página
st.set_page_config(page_title="Chocolate Dashboard", page_icon="🍫", layout='wide')

# Inyectar la fuente ChunkFive usando CSS
st.markdown("""
    <style>
    @font-face {
        font-family: 'ChunkFive';
        src: url('/static/ChunkFive.woff') format('woff');
        font-weight: normal;
        font-style: normal;
    }

    body, html, .stApp {
        font-family: 'ChunkFive', sans-serif !important;
        background-color: #fff9f5;
    }

    h1, h2, h3, h4, h5, h6, .css-18ni7ap, .css-1d391kg, .plotly-graph-div * {
        font-family: 'ChunkFive', sans-serif !important;
    }

    .block-container {
        padding-top: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Cargar datos
@st.cache_data
def load_data():
    return pd.read_csv("Database.csv", parse_dates=["Date"])

df = load_data()

# 🎉 Título general
st.title("🍫 Chocolate Sales Overview")

# ========================== VENTAS POR DÍA DE LA SEMANA ==========================
#!st.markdown("### 📅 Units Sold by Day of the Week")

days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
weekday_sales = (
    df.groupby('WeekdayName')['UnitsSold']
    .sum()
    .reindex(days_order)
    .reset_index()
)

fig_week = px.line(
    weekday_sales,
    x="WeekdayName",
    y="UnitsSold",
    markers=True,
    title="Weekly Sales 🍭",
    labels={"UnitsSold": "Units Sold", "WeekdayName": "Day"},
    color_discrete_sequence=["#eb2c2d"]
)

fig_week.update_traces(
    line=dict(width=6, shape='spline'),
    marker=dict(size=14, color="#d0f0f7", line=dict(width=3, color="black")),
    text=weekday_sales["UnitsSold"].apply(lambda x: f"{x:,.0f}"),
    textposition="top center",
    mode="lines+markers+text"
)

fig_week.update_layout(
    plot_bgcolor="#fff9f5",
    paper_bgcolor="#fff9f5",
    font=dict(family="ChunkFive", color="#000000", size=20),
    title_x=0.3,
    title_font=dict(size=28),
    margin=dict(t=60, b=40, l=40, r=40)
)

# 💬 Mostrar gráfico y tarjeta al lado
# 💬 Mostrar gráfico y tarjeta al lado (solo una vez, bien decorado)
col1, col2 = st.columns([3, 2])

with col1:
    st.plotly_chart(fig_week, use_container_width=True)

with col2:
    top_day = weekday_sales.sort_values('UnitsSold', ascending=False).iloc[0]
    st.markdown(f"""
    <div style="position: relative; display: inline-block;">
        <div style="
            background: linear-gradient(135deg, #eb2c2d, #e2201f);
            color: white;
            padding: 1.5em;
            border-radius: 60% 40% 30% 70% / 60% 30% 70% 40%;
            font-family: 'ChunkFive', sans-serif;
            font-size: 22px;
            text-align: center;
            box-shadow: -10px 10px 0px 0px white, 5px 5px 15px rgba(0,0,0,0.3);
            transform: rotate(-2deg);
            margin: 1em 0;
        ">
            📢 <b>Best Sales Day:</b><br>
            {top_day['WeekdayName']}<br>
            🎉 {int(top_day['UnitsSold']):,} units sold!
        </div>
        <div style="
            position: absolute;
            top: -20px;
            left: -10px;
            background: yellow;
            color: black;
            padding: 0.3em 0.7em;
            font-size: 16px;
            font-weight: bold;
            transform: rotate(-10deg);
            border-radius: 5px;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
        ">
            WOW!
        </div>
    </div>
    """, unsafe_allow_html=True)



# ========================== VENTAS POR MES ==========================
st.markdown("### 📆 Units Sold by Month")

monthly_sales = (
    df.groupby('Month')['UnitsSold']
    .sum()
    .reset_index()
    .sort_values('Month')
)

fig_month = px.line(
    monthly_sales,
    x="Month",
    y="UnitsSold",
    markers=True,
    title="Monthly Sales Trend 🍫",
    labels={"UnitsSold": "Units Sold", "Month": "Month"},
    color_discrete_sequence=["#00b5c2"]
)

fig_month.update_traces(
    line=dict(width=6, shape='spline'),
    marker=dict(size=14, color="#eb2c2d", line=dict(width=3, color="black")),
    text=monthly_sales["UnitsSold"].apply(lambda x: f"{x:,.0f}"),
    textposition="top center",
    mode="lines+markers+text"
)

fig_month.update_layout(
    plot_bgcolor="#fff9f5",
    paper_bgcolor="#fff9f5",
    font=dict(family="ChunkFive", color="#000000", size=20),
    title_x=0.3,
    title_font=dict(size=28),
    margin=dict(t=60, b=40, l=40, r=40)
)

# 💬 Mostrar gráfico y tarjeta al lado
col3, col4 = st.columns([3, 2])

with col3:
    st.plotly_chart(fig_month, use_container_width=True)

with col4:
    top_month = monthly_sales.sort_values('UnitsSold', ascending=False).iloc[0]
    st.markdown(f"""
    <div style="position: relative; display: inline-block;">
        <div style="
            background: linear-gradient(135deg, #00b5c2, #009fad);
            color: white;
            padding: 1.5em;
            border-radius: 60% 40% 30% 70% / 60% 30% 70% 40%;
            font-family: 'ChunkFive', sans-serif;
            font-size: 22px;
            text-align: center;
            box-shadow: -10px 10px 0px 0px white, 5px 5px 15px rgba(0,0,0,0.3);
            transform: rotate(1deg);
            margin: 1em 0;
        ">
            📢 <b>Top Month:</b><br>
            {top_month['Month']}<br>
            🍫 {int(top_month['UnitsSold']):,} units sold!
        </div>
        <div style="
            position: absolute;
            top: -20px;
            right: -10px;
            background: gold;
            color: black;
            padding: 0.3em 0.7em;
            font-size: 16px;
            font-weight: bold;
            transform: rotate(5deg);
            border-radius: 5px;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
        ">
            📈 HOT!
        </div>
    </div>
    """, unsafe_allow_html=True)



#!# Simulando el DataFrame
#!photos = df.groupby(['ProductID','PhotoId'])['CostPerUnit'].mean().reset_index()
#!
#!st.title("🍫 Product Catalog")
#!
#!# Mostrar 3 productos por fila
#!cols = st.columns(3)
#!
#!for idx, row in photos.iterrows():
#!    col = cols[idx % 3]  # para ir rotando entre 3 columnas
#!    with col:
#!        st.image(f"images/{row['PhotoId']}", caption=f"ID: {row['ProductID']}", use_container_width=True)
#!        st.markdown(f"<div style='text-align: center; font-family: ChunkFive; font-size: 18px;'>💲 {row['CostPerUnit']:.2f} USD</div>", unsafe_allow_html=True)
