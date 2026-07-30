import streamlit as st


st.title("LiberFin")

st.write(
    "Gestor inteligente de gastos personales"
)


st.sidebar.title("Menú")


opcion = st.sidebar.selectbox(
    "Selecciona una sección:",
    [
        "Inicio",
        "Registrar movimiento",
        "Historial",
        "Análisis",
        "Proyecciones",
        "Recomendaciones"
    ]
)


st.header(opcion)

st.write(
    "Esta sección estará disponible próximamente."
)
