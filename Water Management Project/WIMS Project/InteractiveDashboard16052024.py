import streamlit as st
import pandas as pd
import plotly.express as px

# Sample DataFrame
df = px.data.gapminder()

# Title
st.title("Interactive Dashboard with Streamlit")

# Dropdown for selecting a country
selected_country = st.selectbox("Select a country", df['country'].unique())

# Filter data based on selected country
filtered_df = df[df['country'] == selected_country]

# Plotly figure
fig = px.line(filtered_df, x='year', y='gdpPercap', title=f'GDP per Capita in {selected_country}')

# Display the figure
st.plotly_chart(fig)
