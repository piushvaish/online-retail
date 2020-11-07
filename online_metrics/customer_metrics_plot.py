import seaborn as sns
import matplotlib.pyplot as plt
from plotly import graph_objs as go
import streamlit as st


@st.cache
def plot_monthly_revenue(tx_revenue):
    # X and Y axis inputs for Plotly graph. We use Scatter for line graphs
    plot_data = [
        go.Scatter(
            x=tx_revenue['InvoiceYearMonth'],
            y=tx_revenue['Revenue'],
            marker_color='crimson'
        )
    ]

    plot_layout = go.Layout(
        xaxis={"type": "category"},
        #title='Monthly Revenue',
        xaxis_tickangle=90
    )
    return go.Figure(data=plot_data, layout=plot_layout)


@st.cache
def plot_monthly_growth_rate(df):
    # using pct_change() function to see monthly percentage change
    df['MonthlyGrowth'] = df['Revenue'].pct_change()

    # visualization - line graph
    plot_data = [
        go.Scatter(
            x=df.query("InvoiceYearMonth < 201112")['InvoiceYearMonth'],
            y=df.query("InvoiceYearMonth < 201112")['MonthlyGrowth'],
        )
    ]

    plot_layout = go.Layout(
        xaxis={"type": "category"},
        #title='Montly Growth Rate',
        xaxis_tickangle=90

    )

    return go.Figure(data=plot_data, layout=plot_layout)


@st.cache
def plot_monthly_active(df):
    # plotting the output
    plot_data = [
        go.Bar(
            x=df['InvoiceYearMonth'],
            y=df['CustomerID'],
            marker_color='rgb(158,202,225)',
            marker_line_color='rgb(8,48,107)',
            marker_line_width=1.5,
            opacity=0.6,
        )
    ]

    plot_layout = go.Layout(
        xaxis={"type": "category"},
        #title='Monthly Active Customers (United Kingdom)',
        xaxis_tickangle=90
    )

    return go.Figure(data=plot_data, layout=plot_layout)


@st.cache
def plot_monthly_order_count(df):
    # plot
    plot_data = [
        go.Bar(
            x=df['InvoiceYearMonth'],
            y=df['Quantity'],
            marker_color='lightsalmon'
        )
    ]

    plot_layout = go.Layout(
        xaxis={"type": "category"}  # ,
        # title='Monthly Total # of Order'
    )

    return go.Figure(data=plot_data, layout=plot_layout)


@st.cache
def plot_average_monthly_revenue(df):
    # plot the bar chart
    plot_data = [
        go.Bar(
            x=df['InvoiceYearMonth'],
            y=df['Revenue'],
            marker_color='royalblue',
            opacity=0.6,
        )
    ]

    plot_layout = go.Layout(
        xaxis={"type": "category"}  # ,
        #title='Monthly Order Average'
    )
    return go.Figure(data=plot_data, layout=plot_layout)
