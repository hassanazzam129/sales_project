# Importing Libraries
import pandas as pd
import plotly.express as px
from datetime import datetime as dt
import plotly.graph_objects as go
import numpy as np
import streamlit as st
#st.set_page_config(layout="wide")

# reading data 
df = pd.read_excel('.\sources\sales.xlsx')

# Data Preprossing

df.columns = df.columns.str.replace(' ', '_').str.upper() # replace space with " _ "

df = df.drop(['COMPANY','STORE_CODE','COMMENT','SERIAL_#','UPC','VENDOR','ALU'],axis=1)  # drop columns 

df['DEP_NAME']=df['DCS_CODE'].str.extract((r'(^.{3})')) # extract data from 'DCS_CODE' to creat new column for department name

df['SPORT_NAME']=df['DCS_CODE'].str[3:6]  # extract data from 'DCS_CODE' column to creat new column for sport name

df['BRAND_NAME']=df['DESCRIPTION_2'].str[3::] # extract data from 'DESCRIPTION_2' column to creat new column for brand name

# convert data type from object to datetime
df['RCPT_DATE']=pd.to_datetime(df['RCPT_DATE'])
df['RCPT_TIME']=pd.to_datetime(df['RCPT_TIME'])

df['MONTH_NAME']=df['RCPT_DATE'].dt.month_name() # creat new column for month name

df['DAY_NAME']=df['RCPT_DATE'].dt.day_name() # creat new column for day name

df = df.rename(columns = {'AUX1':'GENDER'}) # rename aux1 column to gender

df['SIZE']= df['SIZE'].fillna('one size') # filling the null of size column by 'one size'
df.sort_values(by=['RCPT_DATE', 'RCPT_TIME'], ascending = True, inplace=True)


# Function to tender system name by it's real name
def tender (x):
    if x == 'Cash' :
        return 'Cash'
    elif x == 'UDF1' :
        return 'QNB'
    elif x == 'UDF13':
        return 'SOHOULA'
    elif x == 'UDF10' :
        return 'Points Ahly'
    elif x == 'UDF11':
        return 'Point Agricol'
    elif x == 'UDF12' :
        return 'Contact'
    elif x == 'UDF3':
        return 'Misr'
    elif x == 'UDF4' :
        return 'Premium'
    elif x == 'UDF5':
        return 'CIB'
    elif x == 'UDF6' :
        return 'Point Vod'
    elif x == 'UDF7':
        return 'Voucher'
    elif x == 'UDF8' :
        return 'Valu'
    elif x== 'Deposit':
        return 'Deposit'
    
df['TENDER_NAME']=df['TENDER_NAME'].apply(tender) # apply tener function on tender column

total_rcpt = df['RCPT_NO'].nunique()
sold_qty = df['SOLD_QTY'].sum()
total_sales =df['EXT_PRICE'].sum()
atv = (df['EXT_PRICE'].astype(int).sum()/df['RCPT_NO'].nunique())
atv=atv.round(2)

upt =df['SOLD_QTY'].astype(int).sum()/df['RCPT_NO'].nunique()
upt.round(2)
upt = upt.round(2)
total_sales = total_sales.round(2)


tab_overall_vision, tab_categ_Descraption_code,tab_Gendar_sizes = st.tabs(['Overall Vision','Category & Class Name','Gender & sizes'])

with tab_overall_vision:
    st.title('Sales Analysis During The First Six Months OF 2022')
    st.header('1- KPI\'s')
    # row 
    a1 , a2 = st.columns(2)
    a1.metric('UPT',upt)
    a2.metric('ATV',atv)
    
    st.metric('Total Sales',total_sales)
    st.metric('Sold Qty',sold_qty)
    
    st.header('2- Sales By Months')
    st.write('This Graph Will show The Total Sales Of Each Month')
    st.write('And Total Discount Of Each Month')
    fig1 = px.histogram( df , x="MONTH_NAME", y=["EXT_PRICE","EXT_DISC."],barmode= 'group',title = "Sales & Disc Per Month",width = 1000 , height = 500)
    fig1
    st.write('The Best Selling Month Is JUNE')
    st.header('3- Sales By Weekdays')
    st.write('This Graph Will show The Total Sales per Weekdays')
    fig1 = px.histogram(df, x="DAY_NAME", y="EXT_PRICE",title = "Sales Per Weekdays",width = 1000 , height = 500)
    fig1
    
    st.header('4- Sales By Brand')
    st.write('This Graph will Show Total Sales Per each Brand & It\'s Sold Qty')
    fig1 = px.bar(df.groupby('BRAND_NAME')   [['EXT_PRICE','SOLD_QTY']].sum().nlargest(20,'EXT_PRICE'),barmode= 'group',color='SOLD_QTY',width = 1000 , height = 500)
    fig1
    st.write('From This Graph We Can See That The Best Selling Brand Due to Value: ')
    st.write('ANTA')
    st.write('From This Graph We Can See That The Best Selling Brand Due to Sold Qty: ')
    st.write('ENERGETICS')
    
    
    st.header('5- Sales By Tender')
    fig = go.Figure(
    data=[
        go.Pie(labels=df['TENDER_NAME'], values=df['EXT_PRICE'], hole=0.5)
    ])
    fig
with tab_categ_Descraption_code:
    st.title('In This Page we can See Analysis For Each Category & Class Name')
    st.header('1- Sales By Category')
    fig = px.bar(df.groupby('DEP_NAME')[['EXT_PRICE','SOLD_QTY','EXT_DISC.']].sum(),
       barmode= 'group',color='SOLD_QTY',template="plotly_dark",width = 1000 , height = 500)
    fig
    st.write('From This Graph We Can See That The Best Selling Category Due to Value: ')
    st.write('FOOTWEAR')
    st.write('From This Graph We Can See That The Best Selling Category Due to Sold Qty:')
    st.write('HARDWARE')
    
    st.header('2- Sales By Sport')
    fig = px.bar(df.groupby('SPORT_NAME')[['EXT_PRICE','SOLD_QTY','EXT_DISC.']].sum().nlargest(20,'EXT_PRICE'),
       barmode= 'group',color='SOLD_QTY',template="plotly_dark",width = 1000 , height = 500)
    fig
    st.write('From This Graph We Can See That The Best Selling Sport Due to Value: ')
    st.write('Running')
    st.write('From This Graph We Can See That The Best Selling Sport Due to Sold Qty:')
    st.write('Swimming')    
    
    st.header('3- Sales By Description CODE')
    fig = px.bar(df.groupby('DCS_CODE')[['EXT_PRICE','SOLD_QTY','EXT_DISC.']].sum().nlargest(20,'EXT_PRICE'),barmode= 'group',color='SOLD_QTY',width = 1000 , height = 500)
    fig
    st.write('From This Graph We Can See That The Best Selling DCS CODE Due to Value: ')
    st.write('Footwear Running Shose')
    st.write('From This Graph We Can See That The Best Selling DCS CODE Due to Sold Qty:')
    st.write('Footwear Lifestyle Shose') 
    
    st.header('4- Sales By Description Name')
    fig = px.bar(df.groupby('DESCRIPTION_2')[['EXT_PRICE','SOLD_QTY','EXT_DISC.']].sum().nlargest(30,'EXT_PRICE'),
       barmode= 'group',color='SOLD_QTY',template="plotly_dark",width = 1000 , height = 500)
    fig
    st.write('From This Graph We Can See That The Best Selling DCS CODE Due to Value: ')
    st.write(' Shose Adidas')
    st.write('From This Graph We Can See That The Best Selling DCS CODE Due to Sold Qty:')
    st.write(' T-shirt Umbro')
    
with tab_Gendar_sizes:
    st.title('In This page We Can See Analysis For Each Gender & Size')
    st.header('1- Sales By Gender')
    fig = px.bar(df.groupby('GENDER')[['EXT_PRICE','SOLD_QTY','EXT_DISC.']].sum().nlargest(20,'EXT_PRICE'),
       barmode= 'group',color='SOLD_QTY',template="plotly_dark",width = 1000 , height=500)
    fig
    st.write('From This Graph We Can See That The Best Selling Gender Due to Value')
    st.write('& SOLD QTY:(MEN)')
    
    st.header('2- Sales By Size')
    fig =px.bar(df.groupby('SIZE')[['EXT_PRICE','SOLD_QTY']].sum().nlargest(20,'EXT_PRICE'),barmode= 'group',color='SOLD_QTY',width = 1000 , height=500)
    fig
    
    st.header('The Blowe Tabel will will Display Sizes Sold Qty By Each Category& Gender')
    table = pd.pivot_table(df,values = 'SOLD_QTY',index=      ['SIZE','GENDER','DEP_NAME'],aggfunc=np.sum)
    table
    
    
        
     
      
      
  
