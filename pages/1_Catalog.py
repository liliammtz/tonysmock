import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import base64
from io import BytesIO

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

# Simulando el DataFrame
photos = df.groupby(['ProductID','PhotoId','ProductName','Category'])['CostPerUnit'].mean().reset_index()

st.title("🍫 Product Catalog")

# Mostrar 3 productos por fila
#?cols = st.columns(5)
#?
#?for idx, row in photos.iterrows():
#?    col = cols[idx % 5]  # para ir rotando entre 3 columnas
#?    with col:
#?        st.markdown(f"<div style='text-align: center; font-family: ChunkFive; font-size: 18px;'>{row['ProductName']}</div>", unsafe_allow_html=True)
#?        #!st.markdown(f"<div style='text-align: center; font-family: ChunkFive; font-size: 18px;'>💲 {row['CostPerUnit']:.2f} USD</div>", unsafe_allow_html=True)
#?        st.image(f"static/images/{row['PhotoId']}", caption=f"ID: {row['ProductID']}", use_container_width=True)
# Mostrar productos en una tabla visual, sin tarjetas ni bordes
chunk_size = 5  # Número de productos por fila

for i in range(0, len(photos), chunk_size):
    row_chunk = photos.iloc[i:i+chunk_size]
    cols = st.columns(chunk_size)

    for col, (_, row) in zip(cols, row_chunk.iterrows()):
        with col:
            # Imagen
            st.image(f"static/images/{row['PhotoId']}", use_container_width=True)

            # Nombre centrado
            st.markdown(f"""
                <div style='
                    font-family: ChunkFive;
                    font-size: 18px;
                    text-align: center;
                    margin-top: 0.5em;
                '>
                    {row['ProductName']}
                </div>
            """, unsafe_allow_html=True)

            # Precio centrado
            #**st.markdown(f"""
            #**    <div style='
            #**        font-size: 16px;
            #**        text-align: center;
            #**        color: #eb2c2d;
            #**        margin-top: 0.2em;
            #**    '>
            #**        💲{row['CostPerUnit']:.2f} USD
            #**    </div>
            #**""", unsafe_allow_html=True)


df_plot = df.value_counts(['ProductID', 'PhotoId', 'Category', 'Flavor', 'CocoaPercentage']).reset_index()

# Función para convertir imagen a base64
def image_to_base64(path):
    img = Image.open(path)
    buffered = BytesIO()
    img.save(buffered, format="WEBP")  # o "PNG" si es PNG
    img_b64 = base64.b64encode(buffered.getvalue()).decode()
    return f"data:image/webp;base64,{img_b64}"


##################33
# Crear categorías numéricas para X (Category) e Y (Flavor)
x_categories = df_plot['Category'].dropna().unique().tolist()
y_categories = df_plot['Flavor'].dropna().unique().tolist()

df_plot['x_num'] = df_plot['Category'].apply(lambda x: x_categories.index(x))
df_plot['y_num'] = df_plot['Flavor'].apply(lambda y: y_categories.index(y))

# Crear figura
fig = go.Figure()

# Control de offset si hay imágenes en la misma posición
offsets = {}

for _, row in df_plot.iterrows():
    key = (row['x_num'], row['y_num'])
    count = offsets.get(key, 0)
    x_offset = row['x_num'] + (count * 0.1)

    try:
        img_b64 = image_to_base64(f"static/images/{row['PhotoId']}")
        fig.add_layout_image(
            dict(
                source=img_b64,
                x=x_offset,
                y=row['y_num'],
                xref="x",
                yref="y",
                sizex=0.5,
                sizey=0.5,
                xanchor="center",
                yanchor="middle",
                layer="above"
            )
        )
        offsets[key] = count + 1
    except Exception as e:
        st.warning(f"Error with {row['PhotoId']}: {e}")

# Puntos invisibles para hover
fig.add_trace(go.Scatter(
    x=df_plot['x_num'],
    y=df_plot['y_num'],
    mode='markers',
    marker=dict(size=0.1, opacity=0),
    text=df_plot['ProductID'],
    hovertemplate='<b>%{text}</b><br>Flavor: %{y}',
    showlegend=False
))

# Ejes categóricos
fig.update_xaxes(
    tickvals=list(range(len(x_categories))),
    ticktext=x_categories,
    title="Category"
)
fig.update_yaxes(
    tickvals=list(range(len(y_categories))),
    ticktext=y_categories,
    title="Flavor"
)

# Layout final
fig.update_layout(
    title="🍫 Chocolate Flavor Map by Category",
    plot_bgcolor="#fff9f5",
    paper_bgcolor="#fff9f5",
    font=dict(family="ChunkFive", size=18),
    height=700,
    margin=dict(l=60, r=60, t=80, b=60)
)

# Mostrar
st.plotly_chart(fig, use_container_width=True)

#!st.title("🍫 Product Catalog by Category")
#!
#!for category in df['Category'].dropna().unique():
#!    st.markdown(f"### 🍬 {category}")
#!
#!    filtered_df = df[df['Category'] == category]
#!    photos = filtered_df.groupby(['ProductID','PhotoId'])['CostPerUnit'].mean().reset_index()
#!    
#!    cols = st.columns(5)
#!    for idx, row in photos.iterrows():
#!        col = cols[idx % 5]
#!        with col:
#!            st.image(f"static/images/{row['PhotoId']}", caption=f"ID: {row['ProductID']}", use_container_width=True)
#!            st.markdown(f"<div style='text-align: center; font-family: ChunkFive; font-size: 18px;'>💲 {row['CostPerUnit']:.2f} USD</div>", unsafe_allow_html=True)


#!import pandas as pd
#!import plotly.graph_objects as go
#!import streamlit as st
#!
#!# Preparar datos base
#!df_plot = df.value_counts(['ProductID', 'PhotoId', 'Category', 'CocoaPercentage']).reset_index()
#!
#!# Convertir porcentaje si es texto (ej. "70%")
#!if df_plot['CocoaPercentage'].dtype == 'object':
#!    df_plot['CocoaPercentage'] = df_plot['CocoaPercentage'].str.replace('%', '').astype(float)
#!
#!# Posiciones en x e y (podemos usar Category en eje X, y Cocoa en Y)
#!df_plot['x'] = df_plot['Category']
#!df_plot['y'] = df_plot['CocoaPercentage']
#!
#!# Gráfica tipo scatter
#!fig = px.scatter(
#!    df_plot,
#!    x='Category',
#!    y='CocoaPercentage',
#!    color='Category',
#!    hover_data=['ProductID', 'CocoaPercentage'],
#!    size_max=10,
#!    title="🍫 Cocoa Percentage by Chocolate Category",
#!)
#!
#!fig.update_layout(
#!    plot_bgcolor="#fff9f5",
#!    paper_bgcolor="#fff9f5",
#!    font=dict(family="ChunkFive", size=16, color="#000000"),
#!    title_font_size=24
#!)
#!
#!st.plotly_chart(fig, use_container_width=True)
