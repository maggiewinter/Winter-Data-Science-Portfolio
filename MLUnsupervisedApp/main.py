# Import necessary libraries
import streamlit as st
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
import altair as alt
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import seaborn as sns
from sklearn.metrics import silhouette_score

# Header and introduction to app
st.header("K-Means Unsupervised App")
st.markdown("> ##### As a follow-up to the previous supervised machine learning app, please"
" use the provided dataset or one of your choosing to explore k-means clustering.")

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
# Sample dataset    
else:
    data = pd.read_csv("data/winequality-red.csv", delimiter=';')

st.markdown("If you do not upload a file, the dataset `winequality-red` will be used.")

st.divider()

###################################################

st.markdown("You do not need to specify a label as this is an unsupervised algorithm. "
"However, if you wish to, please choose the column from the list below.")

st.markdown("*If you are using the `winequality-red` dataset, 'quality' is recommended as the label.*")

# Allow for user-selected label for later visualization if desired
label = st.selectbox("Choose label", data.columns, 
                     index=None, placeholder="Choose variable to predict (if desired)")

st.divider()

###################################################

# Data processing
st.markdown("### Process Data")
st.markdown("If your data is not fully processed, please select the boxes below to remove " \
"rows with non-numeric or N/A values.")

# Remove NA values
if st.toggle('**Remove rows with N/A values**', value = True):
    data = data.dropna()

#Remove non-numeric columns
if st.toggle('**Remove non-numeric columns**', value=True):
    data_og = data
    data = data_og.select_dtypes(include='number')
    if label in data_og.columns and label not in data.columns:
        data[label] = data_og[label]

# Define X and y
features = [col for col in data.columns if col != label]
X = data[features]
if label != None:
    y = data[label]

# Print column names
st.markdown("The features used in the clustering algorithm will be:")
st.table(X.columns)

st.divider()

###################################################

# Run model with defined parameters
st.markdown("### Run Algorithm")

st.markdown("K-means requires the data to be scaled so that variables of higher magnitudes do not have undue effect."
" Press the button below to scale the data and begin clustering!")

# Scale the data
if st.button('**Scale the data**'):
    scaler = StandardScaler()
    X = scaler.fit_transform(X)

    # Cluster # selection
    sel_clusters = st.slider('Select the number of clusters', 1, 15, 10)

    # Run algorithm!
    kmeans = KMeans(n_clusters=sel_clusters, random_state=42)
    clusters = kmeans.fit_predict(X)
    centroids = kmeans.cluster_centers_

    # Reduce the data to 2 dimensions for visualization using PCA
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X)

    plt.figure(figsize=(12, 9))
    for cluster_num in range(sel_clusters):
        plt.scatter(X_pca[clusters == cluster_num, 0], X_pca[clusters == cluster_num, 1],
                    label=f'Cluster {cluster_num}', alpha=0.7, edgecolor='k', s=60)

    plt.xlabel('PC1')
    plt.ylabel('PC2')
    plt.title(f'KMeans Clustering with {sel_clusters} Clusters')
    plt.legend(loc='best')
    plt.grid(True)

    # Display plot
    st.pyplot(plt)

    # Print centroids
    st.write("Centroids:\n", centroids)

    # View data visualized by true label (if one was input)
    if label != None:
        st.write("The data shown below is visualized by your selected label.")
        # Get unique class labels
        unique_labels = sorted(y.unique())
        palette = sns.color_palette("hsv", len(unique_labels)) 

        # Create plot
        fig, ax = plt.subplots(figsize=(12, 9))
        for i, label_value in enumerate(unique_labels):
            ax.scatter(X_pca[y == label_value, 0], X_pca[y == label_value, 1],
                    color=palette[i], alpha=0.7, edgecolor='k', s=60, label=str(label_value))

        ax.set_xlabel('PC1')
        ax.set_ylabel('PC2')
        ax.set_title('True Labels: 2D PCA Projection')
        ax.legend(loc='best')
        ax.grid(True)

        # Show in Streamlit
        st.pyplot(fig)

    st.divider()

    ###################################################

    # Elbow and silhouette score plots
    st.markdown("### Algorithm Assessment")

    st.markdown("View the elbow plot and average silhouette score plot below to determine the optimal number of clusters.")

    # Define range of k values
    ks = range(2, 15)

    wcss = [] 
    silhouette_scores = [] 

    # Loop over range of k
    for k in ks:
        km = KMeans(n_clusters=k, random_state=42)
        km.fit(X)
        wcss.append(km.inertia_)
        labels = km.labels_
        silhouette_scores.append(silhouette_score(X, labels))

    # Elbow plot
    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.plot(ks, wcss, marker='o')
    plt.xlabel('Number of clusters (k)')
    plt.ylabel('Within-Cluster Sum of Squares')
    plt.title('Elbow Plot for Best Number of Clusters')
    plt.grid(True)

    # Silhouette Score plot
    plt.subplot(1, 2, 2)
    plt.plot(ks, silhouette_scores, marker='o')
    plt.xlabel('Number of clusters (k)')
    plt.ylabel('Silhouette Score')
    plt.title('Silhouette Score for Best Number of Clusters')
    plt.grid(True)

    plt.tight_layout()
    st.pyplot(plt)
