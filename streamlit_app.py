import streamlit as st
import pandas as pd
from google.cloud import firestore
from google.oauth2 import service_account

key_dict = st.secrets["firebase"]
creds = service_account.Credentials.from_service_account_info(dict(key_dict))
db = firestore.Client(credentials=creds, project=key_dict["project_id"])

@st.cache_data
def cargar_peliculas():
    movies_ref = list(db.collection("movies").stream())
    movies_dict = [x.to_dict() for x in movies_ref]
    df = pd.DataFrame(movies_dict)
    df.columns = df.columns.str.strip().str.lower()
    return df

movies_dataframe = cargar_peliculas()

st.sidebar.header("Opciones")

mostrar_todos = st.sidebar.checkbox(
    "Mostrar todos los filmes",
    value=True,
    key="chk_mostrar"
)

st.sidebar.subheader("Buscar filmes por título")
titulo_buscar = st.sidebar.text_input(
    "Título del filme :",
    key="txt_buscar"
)
btn_buscar = st.sidebar.button(
    "Buscar filmes",
    key="btn_buscar"
)

st.sidebar.subheader("Seleccionar Director")
lista_directores = sorted(movies_dataframe["director"].dropna().unique())

director_select = st.sidebar.selectbox(
    "Director",
    lista_directores,
    key="sel_dir"
)

btn_filtrar_director = st.sidebar.button(
    "Filtrar director",
    key="btn_filtrar_director"
)

st.header("Catalogo NETFLIX")

if btn_buscar and titulo_buscar.strip() != "":
    filtro = movies_dataframe[
        movies_dataframe["name"].str.contains(
            titulo_buscar.strip(), case=False, na=False
        )
    ]
    st.header(f"Resultados de búsqueda: '{titulo_buscar}'")
    st.dataframe(filtro)

elif btn_filtrar_director:
    filtro_director = movies_dataframe[
        movies_dataframe["director"] == director_select
    ]
    st.header(f"Filmes del director: {director_select}")
    st.write(f"Total filmes: {len(filtro_director)}")
    st.dataframe(filtro_director)

elif mostrar_todos:
    st.header("Todos los filmes")
    st.dataframe(movies_dataframe)
