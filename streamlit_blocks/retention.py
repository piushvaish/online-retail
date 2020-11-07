import pandas as pd
import streamlit as st
from pathlib import Path
from online_metrics.monthly_retention_rate import retention_table, plot_retention, cohort_based_retention_rate
from events.plots import retention_heatmap


def display_retention():
    st.header("Customer Retention with Cohort Analysis")
    st.write("Retention analysis is key to understanding if customers come back to your buy your product"
             " and at what frequency. Inevitably, the percentage of customers coming back will decrease"
             " with time after their acquisition as some users fail to see the value"
             "or maybe they just don’t need it or did not like it.")

    st.subheader("Monthly Retention Rate")
    st.text("Monthly Retention Rate = Retained Customers From Prev. Month/Active Customers Total")

    # data
    data_folder = Path("data/")
    tx_data = pd.read_csv(data_folder / 'data2.csv',
                          encoding="utf-8", engine='python')

    tx_retention = retention_table(tx_data)
    # st.dataframe(tx_user_type_revenue)
    fig = plot_retention(tx_retention)
    st.plotly_chart(fig)

    with st.beta_expander("See explanation"):
        st.write("""
        Monthly Retention Rate significantly jumped from June to August 
        and went back to previous levels afterwards.
        """)

    st.subheader("Cohort Based Retention Rate")
    st.write("Cohorts are determined as first purchase year-month of the customers."
             "You will be measuring what percentage of the customers retained after their"
             "first purchase in each month. This view will helps to see how recent and old cohorts"
             "differ regarding retention rate and if recent changes in customer experience affected"
             "new customer’s retention or not.")

    tx_retention_cohort = cohort_based_retention_rate(tx_data)
    if st.checkbox('Show Retention Table'):
        st.dataframe(tx_retention_cohort.style.highlight_max(axis=0))
    fig = retention_heatmap(tx_retention_cohort)
    st.plotly_chart(fig)

    with st.beta_expander("See explanation"):
        st.write("""
        First month retention rate became better recently 
        (don’t take Dec ’11 into account) and in almost 1 year, 15% of customers retain.
        """)

    # From events folder
    # st.subheader("You can see: ")
    # st.text("1. Size of each user cohort (new users per period)")
    # st.text("2. Number of returning users per subsequent period for each cohort")
    # st.text("3. Percentage of returning users per subsequent period for each cohort")

    # # from retention_data import retention_table
    # r_val, r_perc = retention_table(events, acquisition_event_name = 'Cart Created', period='m')

    # if st.checkbox('Show Retention Table'):
    #     st.write(r_val)

    # if st.checkbox('Show Retention Table ( Percentage )'):
    #     st.write(r_perc)
    # # # st.plotly_chart(retention_heatmap(r_perc))
