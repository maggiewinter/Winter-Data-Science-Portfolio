# Import necessary libraries
import streamlit as st
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.preprocessing import StandardScaler
import altair as alt

# Header and introduction to app
st.header("K-Nearest Neighbors Machine Learning App")
st.markdown("> ##### Welcome! On this page, you can explore the k-nearest neighbors classifier " \
"with a sample dataset or an uploaded one.")

st.divider()

###################################################

## Option for user-uploaded data
st.markdown("### Upload Data (Optional)")

# Explanation of requirements
st.markdown("Please ensure that the data you upload is")
st.markdown("1. A csv\n"
"2. Under 200MB\n"
"3. Composed of only numeric features.")

# User-uploaded dataset
uploaded_data = st.file_uploader("Upload a csv file if desired",type=['csv'])
if uploaded_data is not None:
    uploaded_data = pd.read_csv(uploaded_data)
    data = uploaded_data
    # User-selected label/ target variable
    label = st.selectbox('Choose the target variable to be predicted', data.columns)
# Sample dataset    
else:
    data = pd.read_csv("MLStreamlitApp/data/california_housing.csv")
    label = 'ocean_proximity'

st.markdown("If you do not upload a file, the dataset `california_housing` will be used, " \
"with `ocean_proximity` as the label.")

st.divider()

###################################################

# Data processing
st.markdown("### Process Data")
st.markdown("If your data is not fully processed, please select the boxes below to remove " \
"rows with N/A values and/or scale the data.")
st.markdown("*Note: If using the default `california_housing.csv` dataset, rows with N/A " \
"values must be removed to avoid error.*")

# Remove NA values
if st.toggle('**Remove rows with N/A values**', value = True):
    data = data.dropna()

# Define X and y
features = [col for col in data.columns if col != label]
X = data[features]
y = data[label]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale the data
if st.toggle('**Scale the data**', value = True):
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

st.divider()

###################################################

# Run model with defined parameters
st.markdown("### Run Algorithm")

# Briefly explain knn
st.markdown("In the k-nearest neighbors model, observations are labeled based on which labeled points " \
"they are closest to. The 'k' value is the number of neighboring points taken into consideration. " \
"For this reason, odd k values generally perform better because they remove the possibility of a point " \
"having a 50% chance of being one of two labels.")

# Hyperparameter tuning
sel_neighbors = st.slider('Select the number of neighbors', 1, 25)
metrics = ['minkowski', 'manhattan', 'cosine']
sel_metric = st.selectbox('Select distance metric', metrics)

# Initialize KNN classifier
knn = KNeighborsClassifier(n_neighbors = sel_neighbors, metric = sel_metric)

# Train model
knn.fit(X_train, y_train)
y_pred = knn.predict(X_test)

st.divider()

###################################################

# Evaluate model performance
st.markdown("### Evaluate")

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)
accuracy = round(accuracy, 3)

# Calculate AUC
y_probs = knn.predict_proba(X_test)
auc_score = roc_auc_score(y_test, y_probs, multi_class='ovr')
auc_score = round(auc_score, 3)

# Display accuracy and AUC; explain measurements
col1, col2 = st.columns(2)
with col1:
    st.metric("###### Accuracy Score", accuracy)
    st.caption("Accuracy: the percentage of labels the model correctly assigns.")
with col2:
    st.metric("###### AUC Score", auc_score)
    st.caption("AUC: the area under the ROC curve, a comparison between the true positive "
    "and false positive rate.")

st.divider()

###################################################

# Determine best k value for accuracy
st.markdown("### Optimize")
st.markdown("Each value of k (up to a selected number) is plotted based on accuracy. " \
"Choose the maximum value you want to test and then click the button to view the graph.")

# User-selected max k value
max = st.slider('Maximum number of neighbors', 1, 15, value = 7)
k_values = range(1, max + 1) 

# Button to kickstart
if st.button("Evaluate Accuracy for 3 Distance Metrics", type="primary"):

    # Loading message with progress bar
    loading_message = st.empty()
    loading_message.markdown("*Loading.... thank you for your patience!*")
    progress = 0

    # Initalize results
    results = []

    # For loop where each k value is evaluated in each of the three distance metrics
    for m in metrics:

        # Advance progress bar
        loading_message.progress(progress, "*Loading.... thank you for your patience!*")
        progress = progress + 35

        for k in k_values:
            # Run knn and evaluate accuracy
            knn_temp = KNeighborsClassifier(n_neighbors=k, metric=m)
            knn_temp.fit(X_train, y_train)
            accuracy = accuracy_score(y_test, knn_temp.predict(X_test))
            results.append({'k_values': k, 'accuracy': accuracy, 'metric': m})

    # Advance progress bar
    progress = 85
    loading_message.progress(progress, "*Loading.... thank you for your patience!*")

    # Display line graph with metrics compared
    st.divider()
    st.altair_chart(alt.Chart(pd.DataFrame(results)).mark_line(point=True).encode(
        x='k_values:O',
        y='accuracy:Q',
        color='metric:N').configure_axisX(labelAngle = 0), use_container_width = True)

    # Finish progress bar and remove loading message
    progress = 100
    loading_message.progress(progress, "*Loading.... thank you for your patience!*")
    loading_message.empty()
