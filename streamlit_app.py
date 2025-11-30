import streamlit as st
import pandas as pd
from google.cloud import firestore
from google.oauth2 import service_account

# Autenticación con Firebase (desde st.secrets)
key_dict = st.secrets["firebase"]
creds = service_account.Credentials.from_service_account_info(dict(key_dict))
db = firestore.Client(credentials=creds, project=key_dict["project_id"])

dbNames = db.collection("movies")


st.header("Catalogo NETFLIX")
names_ref = list(db.collection(u'names').stream())
names_dict = list(map(lambda x: x.to_dict(), names_ref))
names_dataframe = pd.DataFrame(names_dict)
st.dataframe(names_dataframe)

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
