import streamlit as st
import pandas as pd



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

    st.title("LiberFin")

    st.subheader(
        "Gestor inteligente de gastos personales"
    )


    st.write(
        """
        LiberFin es una aplicación diseñada para ayudar
        a los usuarios a organizar sus finanzas personales,
        analizar sus hábitos de consumo y tomar mejores
        decisiones financieras.
        """
    )


    st.divider()


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


    st.subheader(
        "Resumen mensual"
    )


    mes = st.selectbox(
        "Selecciona el mes:",
        datos_actualizados["fecha"]
        .str[:7]
        .unique()
    )


    datos_mes = datos_actualizados[
        datos_actualizados["fecha"]
        .str.startswith(mes)
    ]


    ingresos_mes = datos_mes[
        datos_mes["tipo"] == "Ingreso"
    ]["monto"].sum()


    gastos_mes = datos_mes[
        datos_mes["tipo"] == "Gasto"
    ]["monto"].sum()


    balance_mes = ingresos_mes - gastos_mes


    gastos_categoria = (
        datos_mes[
            datos_mes["tipo"] == "Gasto"
        ]
        .groupby("categoria")["monto"]
        .sum()
    )


    if not gastos_categoria.empty:

        categoria_mayor = gastos_categoria.idxmax()

        monto_categoria = gastos_categoria.max()


    else:

        categoria_mayor = "ninguna"

        monto_categoria = 0


    if gastos_mes > 0:

        promedio = datos_mes[
            datos_mes["tipo"] == "Gasto"
        ]["monto"].mean()


        gastos_extra = datos_mes[
            (datos_mes["tipo"] == "Gasto") &
            (datos_mes["monto"] > promedio * 2)
        ]


    else:

        gastos_extra = pd.DataFrame()


    resumen = (
        f"Durante el mes {mes}, "
        f"tus ingresos fueron ${ingresos_mes:,.2f} "
        f"y tus gastos fueron ${gastos_mes:,.2f}. "
        f"Tu categoría con mayor gasto fue "
        f"{categoria_mayor} con ${monto_categoria:,.2f}. "
    )


    if not gastos_extra.empty:

        resumen += (
            "Se detectaron gastos fuera de lo normal "
            "que podrían requerir revisión."
        )

    else:

        resumen += (
            "No se detectaron gastos fuera de lo normal."
        )


    st.info(resumen)

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


    ingresos = datos[
        datos["tipo"] == "Ingreso"
    ]["monto"].sum()


    gastos = datos[
        datos["tipo"] == "Gasto"
    ]["monto"].sum()


    disponible = ingresos - gastos


    st.write(
        f"Dinero disponible actual: ${disponible:,.2f}"
    )


    meta = st.number_input(
        "¿Cuál es el monto de tu meta financiera?",
        min_value=0.0
    )


    ahorro_mensual = st.number_input(
        "¿Cuánto puedes ahorrar al mes?",
        min_value=0.0
    )


    if st.button("Calcular proyección"):


        if ahorro_mensual == 0:

            st.warning(
                "El ahorro mensual debe ser mayor a cero."
            )


        else:

            meses = meta / ahorro_mensual


            st.success(
                f"Alcanzarás tu meta aproximadamente "
                f"en {meses:.1f} meses."
            )


            porcentaje = (
                ahorro_mensual / ingresos
            ) * 100


            st.info(
                f"Esto representa aproximadamente "
                f"el {porcentaje:.1f}% de tus ingresos."
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


    gastos = datos[
        datos["tipo"] == "Gasto"
    ]


    if gastos.empty:

        st.write(
            "No existen gastos registrados."
        )


    else:

        promedio = gastos["monto"].mean()


        gastos_inusuales = gastos[
            gastos["monto"] > promedio * 2
        ]


        if gastos_inusuales.empty:

            st.success(
                "No se detectaron gastos fuera "
                "del comportamiento normal."
            )


        else:

            st.warning(
                "Se encontraron gastos inusuales:"
            )


            st.dataframe(
                gastos_inusuales
            )
