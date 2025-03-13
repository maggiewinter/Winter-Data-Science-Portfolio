## Import necessary libraries
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

## Read in fight song data
df = pd.read_csv("basic_streamlit_app/data/fight_songs.csv")

## Title and subtitle; revise introduction to data
st.title("Onward to Victory!")
st.subheader("This data was compiled by five thirty eight for an article on college fight songs.")

st.write("*Below is the list of schools with their fight song in this database.*")
df_display = df.filter(['school', 'conference', 'song_name', 'writer'], 
                     axis=1)
st.dataframe(df_display)

## Song length interactive visualizations
st.markdown("---")
st.header("Overall Statistics")
st.subheader("Song Length")

# Histogram of song length
fig1 = px.histogram(df, x="sec_duration", nbins=40, 
                title="Histogram of Fight Song Length",
                labels={"sec_duration": "Length (in seconds)"},
                color_discrete_sequence=["darkgreen"])
st.plotly_chart(fig1)

# All schools song length vs year written (?)
fig2 = px.scatter(df, x='year', y='sec_duration', hover_name="school",
              title="Song Length Over the Years", color = "conference")
st.plotly_chart(fig2)

## Possible charts:
# Timeline of songs written
# Pie chart of student writer vs not
# Pie chart of official song vs not
# Histogram of bpm
# Smaller graphs of tropes?
# Pie chart of men vs not
# Pie chart of 'spelling' vs not -- pie charts can be smaller & grouped together

## This mechanism will be used later in the "Filter by Conference" section
## Code is actively a work in progress

# Filter out Independent -- only one school (Notre Dame)
filtered_conferences = df["conference"].unique()
filtered_conferences = [conf for conf in filtered_conferences if conf != "Independent"]

# User-selected conference
selected_conference = st.selectbox("Filter by conference", filtered_conferences)
filtered_conference_df = df[df["conference"] == selected_conference]

# Histogram 
fig1 = px.histogram(filtered_conference_df, x="sec_duration", nbins=20, 
                title="Histogram of Fight Song Length",
                labels={"sec_duration": "Length (in seconds)"},
                color_discrete_sequence=["green"])
st.plotly_chart(fig1)