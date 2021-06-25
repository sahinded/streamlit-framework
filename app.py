import pandas as pd
import streamlit as st
import datetime as dt


import os
from bokeh.plotting import figure, ColumnDataSource
from bokeh.models.widgets import Dropdown
from bokeh.io import curdoc
from bokeh.layouts import column

from bokeh.models import BooleanFilter, CDSView, Select, Range1d, HoverTool
from bokeh.palettes import Category20
from bokeh.models.formatters import NumeralTickFormatter
from bokeh.models import BooleanFilter, CDSView, Select, Range1d, HoverTool

import numpy as np


import requests

st.write('Milestone Project by Sahinde Dogruer,')

st.title("Interactive Charts of Stock Closing Prices for 2021")


ticker = st.sidebar.text_input("Enter stock ticker symbol, e.g.IBM",'IBM')
default='IBM'

month = st.sidebar.selectbox(
        "Select Month ", range(1,7),1)
        #("1", "2", "3", "4","5","6"))
#p = st.sidebar.number_input("How many days (1-31)", min_value=1, max_value=31, step=1)        

from dotenv import load_dotenv 

load_dotenv()


@st.cache 


 

def load_data(stock,month):
    
    print(os.environ.get('API'))    
    alphav_key = os.environ.get('API') 
   
    url ='https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol='+stock+'&apikey='+alphav_key+'&datatype=csv'
     
    data = pd.read_csv(url)
    #r= requests.get(url)
    #data = r.json()
    #data = data["Time Series (5min)"]
    df=pd.DataFrame(data)
    df.reset_index(level=0, inplace=True)
    #df['timestamp']= pd.to_datetime(df['timestamp'])
    del df['index']
    del df['adjusted_close']
    df= df.rename({'timestamp': 'Date'}, axis=1)
    df["Date"] = pd.to_datetime(df["Date"])
   
    df= df[df['Date'].dt.month == month]
   
    
    
    
   
    #df= df[pd.DatetimeIndex(df['Date']).month==month]
    #df = df[df['Date'].dt.month == ]
    print(df)

   
    return df

  
df = load_data(ticker.strip(),month)


plot = figure(title='Interactive Graph of Stock Closing Prices by Month', x_axis_type='datetime', plot_height=350, plot_width=450)
plot.xgrid.grid_line_color=None
plot.ygrid.grid_line_alpha=None
plot.xaxis.axis_label = 'Month'
plot.yaxis.axis_label = 'Closing Price'

plot.line(df['Date'], df['close'])
st.bokeh_chart(plot)

st.subheader('Stock closing prices')
st.write(df)




 
