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

    st.header("Historial financiero")


    datos_actualizados = pd.read_csv(
        "movimientos.csv"
    )


    st.dataframe(
        datos_actualizados
    )

# Análisis

elif opcion == "Análisis":

    st.header("Análisis de gastos")


    gastos = datos[
        datos["tipo"] == "Gasto"
    ]


    gastos_categoria = (
        gastos
        .groupby("categoria")["monto"]
        .sum()
    )


    st.subheader(
        "Distribución de gastos por categoría"
    )


    import plotly.express as px


    grafica = px.pie(
        values=gastos_categoria.values,
        names=gastos_categoria.index,
        title="Porcentaje de gastos"
    )


    st.plotly_chart(
        grafica
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


    ingresos = datos[
        datos["tipo"] == "Ingreso"
    ]["monto"].sum()


    gastos = datos[
        datos["tipo"] == "Gasto"
    ]["monto"].sum()


    balance = ingresos - gastos


    if balance > 0:

        ahorro = balance * 0.20


        st.success(
            f"Tienes un balance positivo. "
            f"Una recomendación es ahorrar aproximadamente "
            f"${ahorro:,.2f}."
        )


    else:

        st.warning(
            "Tus gastos son mayores o iguales a tus ingresos. "
            "Te recomendamos revisar tus categorías de consumo."
        )


    gastos_categoria = (
        datos[datos["tipo"] == "Gasto"]
        .groupby("categoria")["monto"]
        .sum()
    )


    if not gastos_categoria.empty:

        categoria_mayor = gastos_categoria.idxmax()

        gasto_mayor = gastos_categoria.max()


        porcentaje = (
            gasto_mayor / gastos
        ) * 100


        if porcentaje > 40:

            st.info(
                f"Tu categoría con mayor consumo es "
                f"{categoria_mayor}, representando "
                f"aproximadamente el {porcentaje:.1f}% "
                "de tus gastos."
            )


elif opcion == "Simulador de compra":

    st.header("Simulador de compra inteligente")


    ingresos = datos[
        datos["tipo"] == "Ingreso"
    ]["monto"].sum()


    gastos = datos[
        datos["tipo"] == "Gasto"
    ]["monto"].sum()


    disponible = ingresos - gastos


    st.write(
        f"Dinero disponible actualmente: ${disponible:,.2f}"
    )


    producto = st.text_input(
        "¿Qué producto deseas comprar?"
    )


    precio = st.number_input(
        "Precio del producto",
        min_value=0.0
    )


    if st.button("Evaluar compra"):


        diferencia = precio - disponible


        if diferencia <= 0:

            restante = disponible - precio


            st.success(
                f"Puedes comprar {producto}. "
                f"Después de la compra conservarías "
                f"${restante:,.2f}."
            )


        else:

            porcentaje = (
                diferencia / precio
            ) * 100


            st.warning(
                f"No es recomendable comprar {producto} todavía."
            )


            st.write(
                f"Necesitas ahorrar ${diferencia:,.2f} adicionales."
            )


            st.write(
                f"Esto representa aproximadamente "
                f"el {porcentaje:.1f}% del valor del producto."
            )


elif opcion == "Gastos inusuales":

    st.header("Detección de gastos inusuales")

    st.write(
        "Aquí analizaremos movimientos fuera de lo normal."
    )
    st.bar_chart(gastos_categoria)
