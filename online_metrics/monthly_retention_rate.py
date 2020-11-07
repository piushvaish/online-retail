from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from plotly import graph_objs as go
from online_metrics.new_customer_ratio import min_purchase_dataframe, user_type_revenue_df
# https://towardsdatascience.com/data-driven-growth-with-python-part-1-know-your-metrics-812781e66a5b


def retention_table(df):
    df_uk = min_purchase_dataframe(df)
    # identify which users are active by looking at their revenue per month
    df_user_purchase = df_uk.groupby(['CustomerID', 'InvoiceYearMonth'])['Revenue'].sum().reset_index()

    # create retention matrix with crosstab
    df_retention = pd.crosstab(df_user_purchase['CustomerID'], df_user_purchase['InvoiceYearMonth']).reset_index()

    df_retention.head()

    # create an array of dictionary which keeps Retained & Total User count for each month
    months = df_retention.columns[2:]
    retention_array = []
    for i in range(len(months)-1):
        retention_data = {}
        selected_month = months[i+1]
        prev_month = months[i]
        retention_data['InvoiceYearMonth'] = int(selected_month)
        retention_data['TotalUserCount'] = df_retention[selected_month].sum()
        retention_data['RetainedUserCount'] = df_retention[(df_retention[selected_month] > 0) & (
            df_retention[prev_month] > 0)][selected_month].sum()
        retention_array.append(retention_data)

    # convert the array to dataframe and calculate Retention Rate
    df_retention = pd.DataFrame(retention_array)
    df_retention['RetentionRate'] = df_retention['RetainedUserCount']/df_retention['TotalUserCount']

    return df_retention


@st.cache
def plot_retention(df):
    # plot the retention rate graph
    plot_data = [
        go.Scatter(
            x=df.query("InvoiceYearMonth<201112")['InvoiceYearMonth'],
            y=df.query("InvoiceYearMonth<201112")['RetentionRate'],
            name="organic"
        )

    ]

    plot_layout = go.Layout(
        xaxis={"type": "category"},
        title='Monthly Retention Rate'
    )
    return go.Figure(data=plot_data, layout=plot_layout)


def cohort_based_retention_rate(df):
    # creating a new dataframe with UK customers only
    # converting the type of Invoice Date Field from string to datetime.
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    # creating YearMonth field for the ease of reporting and visualization
    df['InvoiceYearMonth'] = df['InvoiceDate'].map(lambda date: 100*date.year + date.month)
    # calculate Revenue for each row and create a new dataframe with YearMonth - Revenue columns
    df['Revenue'] = df['UnitPrice'] * df['Quantity']
    df_uk = df.query("Country=='United Kingdom'").reset_index(drop=True)
    # create a dataframe contaning CustomerID and first purchase date
    df_min_purchase = df_uk.groupby('CustomerID').InvoiceDate.min().reset_index()
    df_min_purchase.columns = ['CustomerID', 'MinPurchaseDate']
    df_min_purchase['MinPurchaseYearMonth'] = df_min_purchase['MinPurchaseDate'].map(
        lambda date: 100 * date.year + date.month)

    df_uk = min_purchase_dataframe(df)

    # identify which users are active by looking at their revenue per month
    df_user_purchase = df_uk.groupby(['CustomerID', 'InvoiceYearMonth'])['Revenue'].sum().reset_index()
    # create our retention table again with crosstab() and add firs purchase year month view
    df_retention = pd.crosstab(df_user_purchase['CustomerID'], df_user_purchase['InvoiceYearMonth']).reset_index()
    # create an array of dictionary which keeps Retained & Total User count for each month
    months = df_retention.columns[2:]
    df_retention = pd.merge(df_retention, df_min_purchase[['CustomerID', 'MinPurchaseYearMonth']], on='CustomerID')
    new_column_names = ['m_' + str(column) for column in df_retention.columns[:-1]]
    new_column_names.append('MinPurchaseYearMonth')
    df_retention.columns = new_column_names

    # create the array of Retained users for each cohort monthly
    retention_array = []
    for i in range(len(months)):
        retention_data = {}
        selected_month = months[i]
        prev_months = months[:i]
        next_months = months[i+1:]
        for prev_month in prev_months:
            retention_data[prev_month] = np.nan

        total_user_count = df_retention[df_retention.MinPurchaseYearMonth ==
                                        selected_month].MinPurchaseYearMonth.count()
        retention_data['TotalUserCount'] = total_user_count
        retention_data[selected_month] = 1

        query = "MinPurchaseYearMonth == {}".format(selected_month)

        for next_month in next_months:
            new_query = query + " and {} > 0".format(str('m_' + str(next_month)))
            retention_data[next_month] = np.round(df_retention.query(
                new_query)['m_' + str(next_month)].sum()/total_user_count, 2)
        retention_array.append(retention_data)

    df_retention = pd.DataFrame(retention_array)
    df_retention.index = months

    # showing new cohort based retention table
    return df_retention
