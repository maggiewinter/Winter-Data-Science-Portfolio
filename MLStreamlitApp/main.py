# Import necessary libraries
import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, roc_curve, roc_auc_score, auc
from sklearn.preprocessing import StandardScaler

## Add note on making sure data is clean and desired features are numeric

# Sample dataset
data = pd.read_csv("MLStreamlitApp/data/california_housing.csv")
label = 'ocean_proximity'

# User-uploaded dataset
uploaded_data = st.file_uploader("Upload a csv file if desired",type=['csv'])
if uploaded_data is not None:
    data = uploaded_data
    label = st.selectbox('Choose the target variable to be predicted', data.columns)

if st.checkbox('Remove rows with N/A values'):
    data = data.dropna()

features = list(data.columns)
features.remove(label)

X = data[features]
y = data[label]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

if st.checkbox('Scale the data'):
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)



# Adjust model settings

sel_neighbors = st.slider('Select the number of neighbors', 1, 25)
metrics = ['minkowski', 'manhattan', 'cosine']
sel_metric = st.selectbox('Select distance metric', metrics)


# Run model
# Initialize the KNN classifier
knn = KNeighborsClassifier(n_neighbors = sel_neighbors, metric = sel_metric)

# Train model
knn.fit(X_train, y_train)
y_pred = knn.predict(X_test)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)
st.write(accuracy)

# Calculate AUC
y_probs = knn.predict_proba(X_test)
auc_score = roc_auc_score(y_test, y_probs, multi_class='ovr')
st.write(auc_score)
