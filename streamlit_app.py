import streamlit as st
import pandas as pd
from google.cloud import firestore
from google.oauth2 import service_account

# Autenticación con Firebase (desde st.secrets)
key_dict = st.secrets["firebase"]
creds = service_account.Credentials.from_service_account_info(dict(key_dict))
db = firestore.Client(credentials=creds, project=key_dict["project_id"])

dbMovies = db.collection("movies")

# Punto 5, inciso 1 - crear check box en el sidebar, para visualizar todos los filmes
st.sidebar.header("Opciones")
mostrar_todos = st.sidebar.checkbox("Mostrar todos los filmes", value= True)


st.sidebar.subheader("Buscar filmes por título")
titulo_buscar = st.sidebar.text_input("Título del filme :")
btn_buscar = st.sidebar.button("Buscar filmes")


st.header("Catalogo NETFLIX")

# Cargo los datos
@st.cache_data
def cargar_peliculas():
    movies_ref = list(db.collection(u'movies').stream())
    movies_dict = [x.to_dict() for x in movies_ref]

    df = pd.DataFrame(movies_dict)
    df.columns = df.columns.str.strip().str.lower()
    return df

# Se carga desde cache o si no firebase bloquea por cuotas excedidas 
movies_dataframe = cargar_peliculas()


st.sidebar.header("Opciones")

# Bandera para ver o quiar todos los filmes
mostrar_todos = st.sidebar.checkbox("Mostrar todos los filmes", value=True)

# Parte de la busqueda
st.sidebar.subheader("Buscar filmes por título")
titulo_buscar = st.sidebar.text_input("Título del filme :")
btn_buscar = st.sidebar.button("Buscar filmes")


st.header("Catalogo NETFLIX")
# Buequeda
if btn_buscar and titulo_buscar.strip() != "":
    filtro = movies_dataframe[
        movies_dataframe["name"].str.contains(
            titulo_buscar.strip(),
            case=False,
            na=False
        )
    ]

    st.header(f"Resultados de búsqueda: '{titulo_buscar}'")
    st.dataframe(filtro)







elif mostrar_todos:
    st.header("Todos los filmes")
    st.dataframe(movies_dataframe)
