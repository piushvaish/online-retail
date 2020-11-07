#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import random
import streamlit as st
from pathlib import Path

from events.create_data import create_dummy_data
from events.retention_data import retention_table
from events.plots import plot_users_per_period, plot_stacked_funnel, retention_heatmap, plot_user_flow


from streamlit_blocks.home import display_home
from streamlit_blocks.new_customer_ratio import display_new_customer_ratio
from streamlit_blocks.retention import display_retention


# data
data_folder = Path("data/")
tx_data = pd.read_csv(data_folder / 'data2.csv',
                      encoding="utf-8", engine='python')

# dummy data
events = create_dummy_data()


# Navigation
navigation = st.sidebar.radio(
    "Navigation",
    ("Home", "New Customer Ratio", "Customer Retention with Cohort Analysis",
     "Customer Segmentation",
     "Customer Acquisition Detail", "Customer Funnel Analysis",
     "Visualizing Customer Journey")
)

if navigation == "Home":
    display_home()

if navigation == "New Customer Ratio":
    display_new_customer_ratio()


if navigation == "Customer Retention with Cohort Analysis":
    display_retention()


if navigation == "Customer Segmentation":
    st.header("Customer Segmentation")
    st.subheader("Using RFM (Recency - Frequency - Monetary Value) Clustering")
    st.write("Low Value: Customers who are less active than others, \n not very frequent buyer/visitor and generates very low - zero - maybe negative revenue.")
    st.write(
        "Mid Value: Using platform fairly frequent and generates moderate revenue.")
    st.write("High Value: High Revenue, Frequency and low Inactivity.")


if navigation == "Customer Acquisition Detail":
    st.header("Customer Acquisition Details")
    st.write("Customer acquisition is the process of bringing new customers or clients to your business."
             "The goal of this process is to create a systematic, sustainable acquisition strategy that"
             "can evolve with new trends and changes.")

    st.subheader("You can see: ")
    st.text("1. New acquired users per period")
    st.text("2. Number of acquired users who are active per period")
    st.text("3. Number of returning users per period \n(i.e. active users who were acquired during a previous period)")
    st.text("4. W/W Growth: week-on-week percentage growth. \nIdeally, you want this to be always in the positives and increasing with time.")
    st.text("5. N/R Ratio: new-to-returning users ratio. \n Indicative of how the period activity is shared between new and returning customers.")

    fig = plot_users_per_period(events=events, acquisition_event_name='Cart Created',
                                user_source_col='user_source', period='m')
    st.plotly_chart(fig)


if navigation == "Customer Funnel Analysis":
    st.header("Customer Funnel Analysis")
    st.write("Funnel analysis is critical in identifying bottlenecks at any point in the user journey."
             " Usually, there is a key event which generates revenue for the business."
             "Maximising the number of people performing this action is thus to our best interest.")

    st.subheader("You can see: ")
    st.text("1. Number of customers that perform each step")
    st.text("2. Percentage of customers that perform each step")

    steps = ['Cart Created', 'Add Payment',
             'Order Created', 'Order Processed', 'Shipment Released', 'Order Completed']
    fig = plot_stacked_funnel(events, steps, col='user_source')
    st.plotly_chart(fig)


# Sankey
if navigation == "Visualizing Customer Journey":
    st.header("Visualizing Customer Journey using Sankey Diagram")
    st.write("Sankey diagram is a type of chart that displays flows and their quantities."
             " Arrows of various thickness are used to visualize the quantity in each flow as well"
             " as the direction or path in which they flow."
             " Mapping out journey flow diagrams helps in identifying and visualising the most dominant ones."
             " This helps in raising insights around customer's touchpoints, but also identifying which steps your customers use the most.")

    st.subheader("You can see: ")
    st.text(
        "1. Most dominant customer journey flows by first defining the starting point")
    fig = plot_user_flow(events, starting_step='Cart Created')
    st.plotly_chart(fig)
