# Import necessary libraries
import streamlit as st
import pandas as pd
import plotly.express as px

# Read in fight song data
df = pd.read_csv("basic_streamlit_app/data/fight_songs.csv")

# =================================
# Introduction
# =================================
st.title("Onward to Victory")
st.subheader("*Explore college fight songs from across the Power Five "
"conferences (and Notre Dame)!*")
st.markdown("##### This app allows the user to filter songs by various characteristics "
"and learn more about the songs of specific schools and conferences.")
st.markdown("---")

# Introduction to dataset
st.write("*Below are the fight songs featured in this database.*")
df_display = df.filter(['song_name', 'school', 'conference'], 
                     axis=1)
st.dataframe(df_display, use_container_width=True)
st.caption("This data was compiled by FiveThirtyEight for a 2019 article and "
        "includes 65 schools.")
st.markdown("---")
st.header("Key Variables")
st.markdown(
    "* `year` : when the song was written (some are `unknown`)  "
    "\n* `student_writer` : whether the writer was a student (some are `unknown`) "
    "\n* `official_song` : whether the song is the official school song as opposed to a fan favorite  "
    "\n* `sec_duration` : how long the song is, in seconds  "
    "\n* `victory_win_won` : whether the song contains the word victory *or* win *or* won  "
    "\n* `spelling` : whether the song spells anything  "
    "\n* `trope_count` : how many (out of 9) common tropes the song contains : "
    "the words **fight**, **victory**, **win**/**won**, and '**rah**'; "
    "references to **opponents**, a **group of men** (sons, boys, etc.), "
    "or the **school colors**; '**nonsense**' **syllables**; and **spelling**"
)
st.markdown("---")

# =================================
# Overall Statistics : Histograms
# =================================
st.header("Histograms")
# Histogram of song length
fig1 = px.histogram(df, x="sec_duration", nbins=40, 
                title="Song Length",
                labels={"sec_duration": "Length (seconds)"},
                color_discrete_sequence=["darkgreen"])

# Histogram of year written
fig2 = px.histogram(df, x="year", nbins=30, 
                title="Years Written",
                labels={"year": "Year (C.E.)"},
                color_discrete_sequence=["darkgreen"])

# Histogram of how many tropes are present
fig3 = px.histogram(df, x="trope_count", nbins=24, 
                title="Tropes Present",
                labels={"trope_count": "Number of Tropes"},
                color_discrete_sequence=["darkgreen"])
# Display
col1, col2= st.columns(2)
with col1:
    st.plotly_chart(fig1, use_container_width=True)
with col2:
    st.plotly_chart(fig2, use_container_width=True)
st.plotly_chart(fig3)
st.markdown("---")

# =================================
# Overall Statistics : Pie Charts
# =================================
st.header("Pie Charts")
# Student writers
# Get counts for each category (yes/no/unknown)
student_writer_counts = df['student_writer'].value_counts().reset_index()
student_writer_counts.columns = ['student_writer', 'count']
fig4 = px.pie(student_writer_counts, values='count', names='student_writer', 
              title='Student Writer')

# Official song
# Get counts for each category (yes/no)
official_song_counts = df['official_song'].value_counts().reset_index()
official_song_counts.columns = ['official_song', 'count']
fig5 = px.pie(official_song_counts, values='count', names='official_song', 
              title='Official Song')

# Spelling
# Get counts for each category (yes/no)
spelling_counts = df['spelling'].value_counts().reset_index()
spelling_counts.columns = ['spelling', 'count']
fig6 = px.pie(spelling_counts, values='count', names='spelling', 
              title='Spelling')

# Victory/ win/ won
# Get counts for each category (yes/no)
victory_win_won_counts = df['victory_win_won'].value_counts().reset_index()
victory_win_won_counts.columns = ['victory_win_won', 'count']
fig7 = px.pie(victory_win_won_counts, values='count', names='victory_win_won', 
              title='Victory/ Win/ Won')

# Display in rows
col1, col2= st.columns(2)
with col1:
    st.plotly_chart(fig4, use_container_width=True)
with col2:
    st.plotly_chart(fig5, use_container_width=True)
with col1:
    st.plotly_chart(fig6, use_container_width=True)
with col2:
    st.plotly_chart(fig7, use_container_width=True)
st.markdown("---")

# =================================
# User Filtering by Variable
# =================================
st.header("Filter by Variable")
# Focus on relevant columns
mod_df = df.filter(['year', 'student_writer', 'official_song', 
                       'sec_duration', 'victory_win_won', 
                       'spelling', 'trope_count'])
# User-selected variable
variable = st.selectbox("Choose a variable!", mod_df.columns)
# Sort results by conference & alphabetically
sorted_df = df.sort_values(by=[variable, 'conference', 'school'], ascending=True)

# If the variable is numeric, the user can use a slider to filter by values
# If the variable is categorical, the user can use a selectbox to filter by values
if variable in ['year', 'sec_duration', 'trope_count']:
    value = st.select_slider(f"Filter songs by {variable}", sorted_df[variable].unique())
else :
    value = st.selectbox(f"Filter songs by {variable} value", sorted_df[variable].unique())
# Filter for the conditions given by the selectbox/ slider
filtered_df = sorted_df[sorted_df[variable] == value]
df_display2 = filtered_df.filter(['school', 'conference', 'song_name', variable], 
                     axis=1)
# Display
st.dataframe(df_display2, use_container_width=True)
st.markdown("---")

# =================================
# User Filtering by School
# =================================
st.header("Filter by School")
# Focus on relevant columns
mod_df2 = df.filter(['school', 'conference', 'song_name','year', 
                     'student_writer', 'official_song', 'sec_duration', 
                     'victory_win_won', 'spelling', 'trope_count'])
# Sort values in selectbox alphabetically to allow for easier navigation
sorted_df2 = mod_df2.sort_values(by=['school'], ascending=True)
# User-selected school
school = st.selectbox("Choose a school!", sorted_df2['school'].unique(), index = 36)
# Display all variables of selected school
df_display3 = sorted_df2[sorted_df2['school'] == school]
st.dataframe(df_display3, use_container_width=True)
st.markdown("---")

# =================================
# User Filtering by Conference
# =================================
st.header("Filter by Conference")
# Filter out Independent -- only one school (Notre Dame)
filtered_conferences = df["conference"].unique()
filtered_conferences = [conf for conf in filtered_conferences if conf != "Independent"]
# User-selected conference
selected_conference = st.selectbox("Choose a conference!", filtered_conferences)
filtered_conference_df = df[df["conference"] == selected_conference]
st.caption("*Note: Notre Dame is not included in this section because its "
"football program is independent from any conference.*")

# =================================
# Conference Statistics: Pie Charts
# =================================
# Student writers
# Get counts for each category (yes/no/unknown)
student_writer_counts = filtered_conference_df['student_writer'].value_counts().reset_index()
student_writer_counts.columns = ['student_writer', 'count']
fig8 = px.pie(student_writer_counts, values='count', names='student_writer', 
              title='Student Writer')

# Official song
# Get counts for each category (yes/no)
official_song_counts = filtered_conference_df['official_song'].value_counts().reset_index()
official_song_counts.columns = ['official_song', 'count']
fig9 = px.pie(official_song_counts, values='count', names='official_song', 
              title='Official Song')

# Spelling
# Get counts for each category (yes/no)
spelling_counts = filtered_conference_df['spelling'].value_counts().reset_index()
spelling_counts.columns = ['spelling', 'count']
fig10 = px.pie(spelling_counts, values='count', names='spelling', 
              title='Spelling')

# Victory/ win/ won
# Get counts for each category (yes/no)
victory_win_won_counts = filtered_conference_df['victory_win_won'].value_counts().reset_index()
victory_win_won_counts.columns = ['victory_win_won', 'count']
fig11 = px.pie(victory_win_won_counts, values='count', names='victory_win_won', 
              title='Victory/ Win/ Won')

# Histogram of how many tropes are present
fig12 = px.histogram(filtered_conference_df, x="trope_count", nbins=24, 
                title=f"Trope Frequency in {selected_conference} Fight Songs",
                labels={"trope_count": "Number of Tropes"},
                color_discrete_sequence=["darkgreen"])

# Display in rows (smaller than overall statistics graphs)
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.plotly_chart(fig8, use_container_width=True)
with col2:
    st.plotly_chart(fig9, use_container_width=True)
with col3:
    st.plotly_chart(fig10, use_container_width=True)
with col4:
    st.plotly_chart(fig11, use_container_width=True)
st.plotly_chart(fig12)