# In this file I define the UI and the logic of the dashboard
import streamlit as st
import pandas as pd
from loguru import logger

from src.backend import get_features_from_the_store
from src.plot import plot_candles

st.write("""
# OHLC features dashboard
""")

# add a selectbox to the sidebar to switch between the online store
# and the offline store
online_or_offline = st.sidebar.selectbox(
    'Select the store',
    ('online', 'offline')
)

# Load the data
data = get_features_from_the_store(online_or_offline)
logger.debug(f'Received {len(data)} rows of data from the Feature Store')

# Display the chart
st.bokeh_chart(plot_candles(data.tail(1440)))


# df = pd.read_csv("my_data.csv")
# st.line_chart(df)