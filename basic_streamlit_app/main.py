import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("basic_streamlit_app/data/fight_songs.csv")

st.title("Let's learn more about college fight songs!")
st.markdown("*This data was compiled by five thirty eight for an article on college fight songs.*")

df_disp1 = df.filter(['school', 'conference', 'song_name', 'writer'], axis=1)
st.dataframe(df_disp1)
st.dataframe(df)

# Histogram 
fig1, ax1 = plt.subplots()
ax1.hist(df.sec_duration, bins=30, color='green', edgecolor='black')
ax1.set_title("Histogram of Fight Song Length")
ax1.set_xlabel("Length (in seconds)")
ax1.set_ylabel("Number of Songs")

st.pyplot(fig1)