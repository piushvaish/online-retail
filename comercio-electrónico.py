#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import random
import streamlit as st

from create_data import create_dummy_data
from retention_data import retention_table
from plots import plot_users_per_period, plot_stacked_funnel, retention_heatmap, plot_user_flow
from customer_metrics import monthly_revenue, monthly_active_customers, monthly_order_count, average_revenue_per_order
from customer_metrics_plot import plot_monthly_revenue, plot_monthly_growth_rate, plot_monthly_active, plot_monthly_order_count, plot_average_monthly_revenue
from new_customer_ratio import user_type_revenue_df, new_customer_data, plot_new_customer_existing, plot_new_customer_ratio
from monthly_retention_rate import retention_table, plot_retention, cohort_based_retention_rate
events = create_dummy_data()

tx_data = pd.read_csv('..\data\data2.csv', encoding = "utf-8", engine='python')


st.sidebar.header("Navegación")
navigation = st.sidebar.radio(
    "Ir",
    ("Inicio", "Proporción de nuevos clientes", "Retención de clientes con análisis de cohortes",
    "Segmentación de clientes",
     "Detalle de adquisición de clientes",
     "Análisis de embudo de clientes", "Visualización del recorrido del cliente")
)

st.sidebar.subheader("Obtenga su demo")
st.sidebar.write("Vea cómo Red Clover puede ayudarlo a pasar de la"
" percepción de datos al valor comercial" 
" en días, no en meses.")
st.sidebar.title("Por favor contactar")
st.sidebar.write("Nicolas Settembrini")

if navigation == "Inicio":
    st.title("**Tablero analítico de comercio electrónico**")
    st.write("Puede ver la demostración de un panel de aplicación web simple."
    "Le mostrará las métricas clave del cliente, como su adquisición y su recorrido para un "
    "plataforma de comercio electrónico en la que vende sus productos.")
    if st.checkbox('Mostrar datos en línea'):
        st.dataframe(tx_data.head(10))

    st.subheader("Ganancia mensual")
    st.text("Ingresos = Conteo de clientes activos * Conteo de pedidos * Ingresos promedio por pedido")
    tx_revenue = monthly_revenue(tx_data)
    #st.dataframe(tx_revenue)
    fig = plot_monthly_revenue(tx_revenue)
    st.plotly_chart(fig)

    st.subheader("Tasa de crecimiento de ingresos mensuales")
    fig = plot_monthly_growth_rate(tx_revenue)
    st.plotly_chart(fig)

    st.subheader("Clientes activos mensuales (Reino Unido)")
    tx_monthly_active = monthly_active_customers(tx_data)
    #st.dataframe(tx_monthly_active)
    fig = plot_monthly_active(tx_monthly_active)
    st.plotly_chart(fig)

    st.subheader("Recuento mensual de pedidos (Reino Unido)")
    tx_monthly_sales = monthly_order_count(tx_data)
    #st.dataframe(tx_monthly_active)
    fig = plot_monthly_order_count(tx_monthly_sales)
    st.plotly_chart(fig)

    st.subheader("Ingresos medios por pedido (Reino Unido)")
    tx_monthly_order_avg = average_revenue_per_order(tx_data)
    #st.dataframe(tx_monthly_active)
    fig = plot_average_monthly_revenue(tx_monthly_order_avg)
    st.plotly_chart(fig)


if navigation == "Proporción de nuevos clientes":
    st.header("Proporción de nuevos clientes")
    st.text("Un buen indicador de si está perdiendo clientes existentes o no puede atraer nuevos.")
    st.write("Un cliente nuevo es quien \nha hecho su primera compra.") 
    tx_user_type_revenue = user_type_revenue_df(tx_data)
    #st.dataframe(tx_user_type_revenue)
    fig = plot_new_customer_existing(tx_user_type_revenue)
    st.plotly_chart(fig) 

    st.write("Los clientes existentes muestran una tendencia positiva y dicen que la base de clientes está creciendo"
     " pero los nuevos clientes tienen una ligera tendencia negativa.")
    
    tx_user_ratio = new_customer_data(tx_data)
    #st.dataframe(tx_user_type_revenue)
    fig = plot_new_customer_ratio(tx_user_ratio)
    st.plotly_chart(fig) 

if navigation == "Retención de clientes con análisis de cohortes":
    st.header("Retención de clientes con análisis de cohortes")
    st.write("El análisis de retención es clave para comprender si los clientes vuelven a comprar su producto"
    " y con qué frecuencia. Inevitablemente, el porcentaje de clientes que regresan disminuirá" 
    " con el tiempo después de su adquisición, ya que algunos usuarios no ven el valor" 
    " o tal vez simplemente no lo necesitan o no les gustó.")

    st.subheader("Tasa de retención mensual")
    st.text("Tasa de retención mensual = Clientes retenidos del mes anterior / Total de clientes activos")

    tx_retention = retention_table(tx_data)
    #st.dataframe(tx_user_type_revenue)
    fig = plot_retention(tx_retention)
    st.plotly_chart(fig) 

    st.subheader("Tasa de retención basada en cohortes")
    st.write("Las cohortes se determinan como la primera compra año-mes de los clientes."
    "Estará midiendo qué porcentaje de los clientes retenidos después de su" 
    " primera compra cada mes. Esta vista ayudará a ver qué tan recientes y antiguas cohortes" 
    " difieren con respecto a la tasa de retención y si los cambios recientes en la experiencia del cliente se vieron afectados" 
    " retención de nuevos clientes o no.")

    tx_retention_cohort = cohort_based_retention_rate(tx_data)
    if st.checkbox('Mostrar tabla de retención (porcentaje)'):
        st.dataframe(tx_retention_cohort)
    fig = retention_heatmap(tx_retention_cohort)
    st.plotly_chart(fig) 

if navigation == "Segmentación de clientes":
    st.header("Segmentación de clientes") 
    st.subheader("Uso de agrupaciones de RFM (actualidad, frecuencia, valor monetario)")
    st.write("Valor bajo: Clientes que son menos activos que otros, \n compradores / visitantes poco frecuentes y generan ingresos muy bajos (cero), tal vez negativos.")
    st.write("Valor medio: utiliza la plataforma con bastante frecuencia y genera ingresos moderados.")
    st.write("Valor alto: ingresos elevados, frecuencia y baja inactividad.")


if navigation == "Detalle de adquisición de clientes":
    st.header("Detalles de adquisición de clientes")
    st.write("La adquisición de clientes es el proceso de atraer nuevos clientes o clientes a su negocio." 
    "El objetivo de este proceso es crear una estrategia de adquisición sistemática y sostenible que" 
    "puede evolucionar con nuevas tendencias y cambios.")

    st.subheader("Puedes ver: ")
    st.text("1. Nuevos usuarios adquiridos por período")
    st.text("2. Número de usuarios adquiridos que están activos por período")
    st.text("3. Número de usuarios recurrentes por período\n(es decir, usuarios activos que se adquirieron durante un período anterior)")
    st.text("4. Crecimiento W/W: porcentaje de crecimiento semanal.\nLo ideal es que esto sea siempre positivo y que aumente con el tiempo.")
    st.text("5. Relación N/R: relación entre usuarios nuevos y recurrentes.\n Indica cómo se comparte la actividad del período entre clientes nuevos y recurrentes.")


    fig = plot_users_per_period(events=events, acquisition_event_name='Cart Created', 
                                user_source_col='user_source', period='m')
    st.plotly_chart(fig)

if navigation == "Análisis de embudo de clientes":
    st.header("Análisis del embudo del cliente")
    st.write("El análisis de embudo es fundamental para identificar cuellos de botella en cualquier punto del recorrido del usuario."
    " Por lo general, hay un evento clave que genera ingresos para la empresa." 
    " Por lo tanto, maximizar el número de personas que realizan esta acción es lo mejor para nuestro interés.")

    st.subheader("Puedes ver: ")
    st.text("1. Número de clientes que realizan cada paso")
    st.text("2. Porcentaje de clientes que realizan cada paso")

    steps = ['Cart Created', 'Add Payment', 
                'Order Created', 'Order Processed', 'Shipment Released', 'Order Completed']
    fig = plot_stacked_funnel(events, steps, col ='user_source')
    st.plotly_chart(fig)



# Sankey
if navigation == "Visualización del recorrido del cliente":
    st.header("Visualización del recorrido del cliente mediante el diagrama de Sankey")
    st.write("El diagrama de Sankey es un tipo de gráfico que muestra los flujos y sus cantidades." 
    " También se utilizan flechas de varios espesores para visualizar la cantidad en cada flujo" 
    " como la dirección o el camino en el que fluyen." 
    " Trazar diagramas de flujo de viaje ayuda a identificar y visualizar los más dominantes." 
    " Esto ayuda a generar conocimientos sobre los puntos de contacto del cliente, pero también a identificar qué pasos utilizan más sus clientes.")


    st.subheader("Puedes ver: ")
    st.text("1. El recorrido del cliente más dominante fluye definiendo primero el punto de partida")
    fig = plot_user_flow(events, starting_step='Cart Created')
    st.plotly_chart(fig)

