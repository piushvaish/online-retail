import pandas as pd
import streamlit as st
from pathlib import Path

from online_metrics.customer_metrics import monthly_revenue, monthly_active_customers, monthly_order_count, average_revenue_per_order
from online_metrics.customer_metrics_plot import plot_monthly_revenue, plot_monthly_growth_rate, plot_monthly_active, plot_monthly_order_count, plot_average_monthly_revenue


def display_home():
    st.title("**E-commerce Analytical Dashboard**")
    st.write("You can see the demo of a simple web-app dashboard."
             "It will show you the key customer metrics such as your aquisition and journey for a "
             "e-commerce platform on which you sell your products.")

    # data
    data_folder = Path("data/")
    tx_data = pd.read_csv(data_folder / 'data2.csv', encoding="utf-8", engine='python')

    st.markdown("Sample data of [an online retail](https://archive.ics.uci.edu/ml/datasets/Online+Retail+II)")
    if st.checkbox('Show Online Data'):
        st.write(tx_data.head(10))

    st.subheader("Monthly Revenue")
    st.text("Revenue = Active Customer Count * Order Count * Average Revenue per Order")
    tx_revenue = monthly_revenue(tx_data)
    # st.dataframe(tx_revenue)
    fig = plot_monthly_revenue(tx_revenue)
    st.plotly_chart(fig)
    with st.beta_expander("See explanation"):
        st.write("""
        Revenue is growing especially Aug ‘11 onwards
        (and data in December is incomplete).
        """)

    st.subheader("Monthly Revenue Growth Rate")
    fig = plot_monthly_growth_rate(tx_revenue)
    st.plotly_chart(fig)
    with st.beta_expander("See explanation"):
        st.write("""
        36.5% growth the previous month.
        (December is excluded in the code since it is incomplete).
        But you need to identify what exactly happened on April.
        """)

    st.subheader("Monthly Active Customers (United Kingdom)")
    tx_monthly_active = monthly_active_customers(tx_data)
    # st.dataframe(tx_monthly_active)
    fig = plot_monthly_active(tx_monthly_active)
    st.plotly_chart(fig)
    with st.beta_expander("See explanation"):
        st.write("""
        Focus on United Kingdom as it has the most of the records in the data.
        In April, Monthly Active Customer number dropped to 817 from 923 (-11.5%)
        """)

    st.subheader("Monthly Order Count (United Kingdom)")
    tx_monthly_sales = monthly_order_count(tx_data)
    # st.dataframe(tx_monthly_active)
    fig = plot_monthly_order_count(tx_monthly_sales)
    st.plotly_chart(fig)
    with st.beta_expander("See explanation"):
        st.write("""
        Order Count also declined in April (279k to 257k, -8%).
        Active Customer Count directly affected Order Count decrease.
        """)

    st.subheader("Average Revenue per Order (United Kingdom)")
    tx_monthly_order_avg = average_revenue_per_order(tx_data)
    # st.dataframe(tx_monthly_active)
    fig = plot_average_monthly_revenue(tx_monthly_order_avg)
    st.plotly_chart(fig)
    with st.beta_expander("See explanation"):
        st.write("""
        Even the monthly order average dropped for April (16.7 to 15.8).
        """)
