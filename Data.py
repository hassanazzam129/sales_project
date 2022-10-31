import pandas as pd
import plotly.express as px
import streamlit as st

# reading data 
df = pd.read_excel('.\sources\sales.xlsx')
df.columns = df.columns.str.replace(' ', '_').str.upper()
df = df.drop(['COMPANY','STORE_CODE','COMMENT','SERIAL_#','UPC','VENDOR','ALU'],axis=1)  # drop columns 
      
st.write(df)