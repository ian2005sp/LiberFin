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
        "Registrar movimiento",
        "Historial",
        "Análisis",
        "Proyecciones",
        "Recomendaciones",
        "Simulador de compra",
        "Gastos inusuales"
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

elif opcion == "Registrar movimiento":

    st.header("Registrar movimiento")


    fecha = st.date_input(
        "Fecha"
    )


    tipo = st.selectbox(
        "Tipo de movimiento",
        [
            "Ingreso",
            "Gasto"
        ]
    )


    categoria = st.text_input(
        "Categoría"
    )


    etiqueta = st.text_input(
        "Etiqueta"
    )


    descripcion = st.text_input(
        "Descripción"
    )


    metodo_pago = st.selectbox(
        "Método de pago",
        [
            "Efectivo",
            "Tarjeta",
            "Transferencia"
        ]
    )


    monto = st.number_input(
        "Monto",
        min_value=0.0
    )


    if st.button("Guardar movimiento"):


        nuevo_movimiento = pd.DataFrame(
            {
                "fecha": [fecha],
                "tipo": [tipo],
                "categoria": [categoria],
                "etiqueta": [etiqueta],
                "descripcion": [descripcion],
                "metodo_pago": [metodo_pago],
                "monto": [monto]
            }
        )


        nuevo_movimiento.to_csv(
            "movimientos.csv",
            mode="a",
            header=False,
            index=False
        )


        st.success(
            "Movimiento guardado correctamente."
        )


elif opcion == "Proyecciones":

    st.header("Proyecciones financieras")

    st.write(
        "Aquí podrás calcular metas de ahorro y objetivos financieros."
    )


elif opcion == "Recomendaciones":

    st.header("Recomendaciones financieras")

    st.write(
        "Aquí LiberFin generará consejos personalizados."
    )


elif opcion == "Simulador de compra":

    st.header("Simulador de compra inteligente")

    st.write(
        "Aquí podrás evaluar si una compra afecta tu presupuesto."
    )


elif opcion == "Gastos inusuales":

    st.header("Detección de gastos inusuales")

    st.write(
        "Aquí analizaremos movimientos fuera de lo normal."
    )
    st.bar_chart(gastos_categoria)
