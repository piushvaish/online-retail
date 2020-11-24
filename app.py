#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import random
import streamlit as st
from pathlib import Path

from streamlit_blocks.home import display_home
from streamlit_blocks.simple_metrics import display_metrics
from streamlit_blocks.retention import display_retention
from streamlit_blocks.customer_acquisition import display_customer_acquisition
from streamlit_blocks.customer_funnel import display_customer_funnel
from streamlit_blocks.customer_sankey import display_customer_sankey



# data
data_folder = Path("data/")
tx_data = pd.read_csv(data_folder / 'data2.csv',
                      encoding="utf-8", engine='python')


# Navigation
navigation = st.sidebar.radio(
    "Navigation",
    ("Home", "Key Performance Indicators", "Customer Retention / Churn Rate",
     "Customer Segmentation",
     "Customer Acquisition Detail", "Customer Funnel Analysis",
     "Visualizing Customer Journey")
)

if navigation == "Home":
    display_home()

if navigation == "Key Performance Indicators":
    display_metrics()


if navigation == "Customer Retention / Churn Rate":
    display_retention()


if navigation == "Customer Segmentation":
    st.header("Customer Segmentation")
    st.subheader("Using RFM (Recency - Frequency - Monetary Value) Clustering")
    st.write("Low Value: Customers who are less active than others, \n not very frequent buyer/visitor and generates very low - zero - maybe negative revenue.")
    st.write(
        "Mid Value: Using platform fairly frequent and generates moderate revenue.")
    st.write("High Value: High Revenue, Frequency and low Inactivity.")


if navigation == "Customer Acquisition Detail":
    display_customer_acquisition()
    


if navigation == "Customer Funnel Analysis":
    display_customer_funnel()
    


# Sankey
if navigation == "Visualizing Customer Journey":
    display_customer_sankey()