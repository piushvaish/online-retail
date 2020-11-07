import pandas as pd
import streamlit as st
from pathlib import Path
from online_metrics.new_customer_ratio import user_type_revenue_df, new_customer_data, plot_new_customer_existing, plot_new_customer_ratio


def display_new_customer_ratio():
    st.header("New Customer Ratio")
    st.subheader(
        "A good indicator of if you are losing existing customers or unable to attract new ones")
    st.write("A new customer is whoever did \nhis/her first purchase.")

    # data
    data_folder = Path("data/")
    tx_data = pd.read_csv(data_folder / 'data2.csv',
                          encoding="utf-8", engine='python')

    tx_user_type_revenue = user_type_revenue_df(tx_data)
    # st.dataframe(tx_user_type_revenue)
    fig = plot_new_customer_existing(tx_user_type_revenue)
    st.plotly_chart(fig)
    with st.beta_expander("See explanation"):
        st.write("""
        Existing customers are showing a positive trend and tells 
        that customer base is growing but new customers have a slight negative trend.
        """)

    tx_user_ratio = new_customer_data(tx_data)
    # st.dataframe(tx_user_type_revenue)
    fig = plot_new_customer_ratio(tx_user_ratio)
    st.plotly_chart(fig)
    with st.beta_expander("See explanation"):
        st.write("""
        New Customer Ratio has declined as expected 
        (we assumed on Feb, all customers were New) and running around 20%.
        """)
