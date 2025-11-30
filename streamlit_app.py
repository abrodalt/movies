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
mostrar_todos = st.sidebar.checkbox("Mostrar todos los filmes", value=True)


# Cargo los datos
st.header("Catalogo NETFLIX")
movies_ref = list(db.collection(u'movies').stream())
movies_dict = list(map(lambda x: x.to_dict(), movies_ref))
movies_dataframe = pd.DataFrame(movies_dict)



if mostrar_todos:
    st.header("Todos los filmes")
    st.dataframe(movies_dataframe)

"""
index = st.text_input("Index")
company = st.text_input("Company")
director = st.text_input("Director")
genre = st.text_input("Genre")
name = st.text_input("Name")
submit = st.button("Crear nuevo registro")

if index and company and director and genre and name and submit:
    doc_ref = db.collection("movies").document(index)
    doc_ref.set({
        "company": company,
        "director": director,
        "genre": genre,
        "name": name
    })
    st.success("Registro creado exitosamente")


"""
