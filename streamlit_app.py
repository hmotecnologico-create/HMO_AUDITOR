import streamlit as st
st.title("🛡️ HMO Auditor - SEÑAL DE EMERGENCIA")
st.write("Si ves esto, Streamlit Cloud está leyendo la RAIZ del repositorio.")
st.success("Sincronización Detectada")
if st.button("Explorar Estructura"):
    import os
    st.write(f"Directorio: {os.getcwd()}")
    st.write(f"Contenido: {os.listdir('.')}")
