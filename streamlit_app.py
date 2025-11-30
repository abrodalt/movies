import streamlit as st
import pandas as pd
from google.cloud import firestore
from google.oauth2 import service_account

# Autentificacion 
key_dict = st.secrets["firebase"]
creds = service_account.Credentials.from_service_account_info(dict(key_dict))
db = firestore.Client(credentials=creds, project=key_dict["project_id"])



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
mostrar_todos = st.sidebar.checkbox("Mostrar todos los filmes", value=True)

#Buscar por titulo
st.sidebar.subheader("Buscar filmes por titulo")
titulo_buscar = st.sidebar.text_input("Título del filme :")
btn_buscar = st.sidebar.button("Buscar filmes")

# Para el filto de director
st.sidebar.subheader("Seleccionar Director")

# Cargar directores únicos y ordenados
lista_directores = sorted(movies_dataframe["director"].dropna().unique())
director_select = st.sidebar.selectbox("Director", lista_directores)
btn_filtrar_director = st.sidebar.button("Filtrar director")

# Header principal
st.header("Catalogo NETFLIX")

# Filtro por titulo
if btn_buscar and titulo_buscar.strip() != "":
    filtro = movies_dataframe[
        movies_dataframe["name"].str.contains(
            titulo_buscar.strip(), case=False, na=False
        )
    ]

    st.header(f"Resultados de búsqueda: '{titulo_buscar}'")
    st.dataframe(filtro)


# Filtro por director
elif btn_filtrar_director:
    filtro_director = movies_dataframe[movies_dataframe["director"] == director_select]

    st.header(f"Filmes del director: {director_select}")
    st.write(f"Total filmes: {len(filtro_director)}")
    st.dataframe(filtro_director)

# Check para mostrar u ocultar
elif mostrar_todos:
    st.header("Todos los filmes")
    st.dataframe(movies_dataframe)








st.header("Catalogo NETFLIX")





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





