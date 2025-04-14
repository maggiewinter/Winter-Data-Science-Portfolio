# Import necessary libraries
import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.preprocessing import StandardScaler


# Sample dataset
data = pd.read_csv("data/california_housing.csv")

# User-uploaded dataset
uploaded_data = st.file_uploader("Upload a csv file if desired",type=['csv']) #,key='1')
if uploaded_data is not None:
    data = uploaded_data





# Adjust model settings



# Run model



# Accuracy vs precision



# AUC score






