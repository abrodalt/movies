import streamlit as st
import pandas as pd
from google.cloud import firestore
from google.oauth2 import service_account

# Autenticación con Firebase (desde st.secrets)
key_dict = st.secrets["firebase"]
creds = service_account.Credentials.from_service_account_info(dict(key_dict))
db = firestore.Client(credentials=creds, project=key_dict["project_id"])




dbNames = db.collection("movies")
st.header("Nuevo registro")
index = st.text_input("Index")
name = st.text_input("Movie")


submit = st.button("Crear nuevo registro")




"""
if csv_file is not None:
    df = pd.read_csv(csv_file)
    st.write("Vista previa del dataset:")
    st.dataframe(df)

    # ---------------------------
    # 2) Seleccionar colección destino
    # ---------------------------
    collection_name = st.text_input("Nombre de la colección en Firestore", "movies")

    upload_btn = st.button("Cargar dataset a Firestore")

    # ---------------------------
    # 3) Subir registros al iniciar upload
    # ---------------------------
    if upload_btn:
        col_ref = db.collection(collection_name)
        
        records = df.to_dict(orient='records')

        with st.spinner("Subiendo documentos a Firestore..."):
            for record in records:
                col_ref.add(record)

        st.success(f"Dataset cargado correctamente en la colección '{collection_name}'")

# ---------------------------
# 4) Visualización de colección existente
# ---------------------------
st.sidebar.header("Visualizar colección")
col_to_view = st.sidebar.text_input("Nombre de colección a leer", "movies")
btn_view = st.sidebar.button("Cargar datos")

if btn_view:
    docs = list(db.collection(col_to_view).stream())
    data = [d.to_dict() for d in docs]

    if data:
        st.sidebar.write("Documentos encontrados:")
        st.sidebar.write(len(data))
        st.write(pd.DataFrame(data))
    else:
        st.sidebar.write("Colección vacía o inexistente")
"""
