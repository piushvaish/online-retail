from datetime import datetime, timedelta
import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from plotly import graph_objs as go


def min_purchase_dataframe(df):
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
        lambda date: 100 * pd.to_datetime(date).year + pd.to_datetime(date).month)

    # merge first purchase date column to our main dataframe (df_uk)
    df_uk = pd.merge(df_uk, df_min_purchase, on='CustomerID')

    return df_uk


def user_type_revenue_df(df):
    # create a column called User Type and assign Existing
    # if User's First Purchase Year Month before the selected Invoice Year Month
    df_uk = min_purchase_dataframe(df)
    df_uk['UserType'] = 'New'
    df_uk.loc[df_uk['InvoiceYearMonth'] > df_uk['MinPurchaseYearMonth'], 'UserType'] = 'Existing'

    # calculate the Revenue per month for each user type
    df_user_type_revenue = df_uk.groupby(['InvoiceYearMonth', 'UserType'])['Revenue'].sum().reset_index()

    # filtering the dates and plot the result
    df_user_type_revenue = df_user_type_revenue.query("InvoiceYearMonth != 201012 and InvoiceYearMonth != 201112")
    return df_user_type_revenue


@st.cache
def new_customer_data(df):
    df_uk = min_purchase_dataframe(df)
    # create a column called User Type and assign Existing
    # if User's First Purchase Year Month before the selected Invoice Year Month
    df_uk['UserType'] = 'New'
    df_uk.loc[df_uk['InvoiceYearMonth'] > df_uk['MinPurchaseYearMonth'], 'UserType'] = 'Existing'
    # create a dataframe that shows new user ratio - we also need to drop NA values (first month new user ratio is 0)
    df_user_ratio = df_uk.query("UserType == 'New'").groupby(['InvoiceYearMonth'])['CustomerID'].nunique(
    )/df_uk.query("UserType == 'Existing'").groupby(['InvoiceYearMonth'])['CustomerID'].nunique()
    df_user_ratio = df_user_ratio.reset_index()
    df_user_ratio = df_user_ratio.dropna()

    # print the dafaframe
    return df_user_ratio


@st.cache
def plot_new_customer_existing(df):
    plot_data = [
        go.Scatter(
            x=df.query("UserType == 'Existing'")['InvoiceYearMonth'],
            y=df.query("UserType == 'Existing'")['Revenue'],
            name='Existing'
        ),
        go.Scatter(
            x=df.query("UserType == 'New'")['InvoiceYearMonth'],
            y=df.query("UserType == 'New'")['Revenue'],
            name='New'
        )
    ]

    plot_layout = go.Layout(
        xaxis={"type": "category"},
        title='New vs Existing'
    )
    return go.Figure(data=plot_data, layout=plot_layout)


@st.cache
def plot_new_customer_ratio(df):
    # plot the result
    plot_data = [
        go.Bar(
            x=df.query("InvoiceYearMonth>201101 and InvoiceYearMonth<201112")['InvoiceYearMonth'],
            y=df.query("InvoiceYearMonth>201101 and InvoiceYearMonth<201112")['CustomerID'],
        )
    ]

    plot_layout = go.Layout(
        xaxis={"type": "category"},
        title='New Customer Ratio'
    )
    return go.Figure(data=plot_data, layout=plot_layout)
