import streamlit as st
st.title("🛡️ HMO Auditor - MODO DIAGNÓSTICO")
st.write("Si estás viendo este mensaje, los cambios en GitHub se están sincronizando correctamente.")
st.success("Conexión con el repositorio: ACTIVA")
if st.button("Verificar Entorno"):
    st.write(f"Directorio Actual: {st.session_state.get('cwd', 'No detectado')}")
    import os
    st.write(f"Archivos en raíz: {os.listdir('.')}")
