import streamlit as st
import pandas as pd


st.title("LiberFin")

st.write(
    "Gestor inteligente de gastos personales"
)


# Cargar datos

datos = pd.read_csv("movimientos.csv")


# Calcular información financiera

ingresos = datos[datos["tipo"] == "Ingreso"]["monto"].sum()

gastos = datos[datos["tipo"] == "Gasto"]["monto"].sum()

balance = ingresos - gastos


# Menú lateral

st.sidebar.title("Menú")


opcion = st.sidebar.selectbox(
    "Selecciona una sección:",
    [
        "Inicio",
        "Historial",
        "Análisis"
    ]
)


# Página de inicio

if opcion == "Inicio":

    st.header("Resumen financiero")

    col1, col2, col3 = st.columns(3)


    col1.metric(
        "Ingresos",
        f"${ingresos:,.2f}"
    )


    col2.metric(
        "Gastos",
        f"${gastos:,.2f}"
    )


    col3.metric(
        "Balance",
        f"${balance:,.2f}"
    )


# Historial

elif opcion == "Historial":

    st.header("Historial de movimientos")

    st.dataframe(datos)


# Análisis

elif opcion == "Análisis":

    st.header("Análisis de gastos")

    gastos_categoria = (
        datos[datos["tipo"] == "Gasto"]
        .groupby("categoria")["monto"]
        .sum()
    )


    st.bar_chart(gastos_categoria)
