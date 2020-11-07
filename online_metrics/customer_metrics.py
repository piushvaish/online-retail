from datetime import datetime, timedelta
import pandas as pd
import streamlit as st


def monthly_revenue(df):
    # converting the type of Invoice Date Field from string to datetime.
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

    # creating YearMonth field for the ease of reporting and visualization
    df['InvoiceYearMonth'] = df['InvoiceDate'].map(lambda date: 100*date.year + date.month)

    # calculate Revenue for each row and create a new dataframe with YearMonth - Revenue columns
    df['Revenue'] = df['UnitPrice'] * df['Quantity']
    df_revenue = df.groupby(['InvoiceYearMonth'])['Revenue'].sum().reset_index()
    return df_revenue


def monthly_active_customers(df):
    # creating a new dataframe with UK customers only
    df_uk = df.query("Country=='United Kingdom'").reset_index(drop=True)

    # creating monthly active customers dataframe by counting unique Customer IDs
    df_monthly_active = df_uk.groupby('InvoiceYearMonth')['CustomerID'].nunique().reset_index()

    # print the dataframe
    return df_monthly_active


def monthly_order_count(df):
    # creating a new dataframe with UK customers only
    df_uk = df.query("Country=='United Kingdom'").reset_index(drop=True)

    # creating monthly active customers dataframe by counting unique Customer IDs
    df_monthly_sales = df_uk.groupby('InvoiceYearMonth')['Quantity'].sum().reset_index()

    # print the dataframe
    return df_monthly_sales


def average_revenue_per_order(df):
    df_uk = df.query("Country=='United Kingdom'").reset_index(drop=True)
    # create a new dataframe for average revenue by taking the mean of it
    df_monthly_order_avg = df_uk.groupby('InvoiceYearMonth')['Revenue'].mean().reset_index()

    # print the dataframe
    return df_monthly_order_avg
