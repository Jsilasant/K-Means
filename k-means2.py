import sys
import re
import math
import numpy as np
import os
import pandas as pd
from sklearn.cluster import KMeans, MiniBatchKMeans

def preprocess(s):
    preprocessed_s = re.sub(r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', ' ', s.lower())
    preprocessed_s = re.sub('[#$-_.&+!*\(\),\'\"]', '', preprocessed_s)
    preprocessed_s = re.sub(r'(?:@[\w_]+)', '', preprocessed_s)
    return preprocessed_s

def jaccard(a, b):
    inter = list(set(a) & set(b))
    I = len(inter)
    union = list(set(a) | set(b))
    U = len(union)
    return round(1 - (float(I) / U), 4)

def SSE(target, centroid):
    return np.sum((target - centroid)**2)

def assign_label_cluster(distance, data_point, total_iterations):
    index_min = min(distance, key=distance.get)
    return[index_min, data_point, centroids[index_max]]

def compute_new_centroids(cluster_label, centroids):
    return np.array(cluster_label + centroids)/2

def K_means(data_points, centroids, total_iteration):
    label = []
    cluster_label  = []
    total_points = len(data_points)
    k = len(centroids)

    for iteration in range(0, total_iteration):
        distance = {}
        for index_centroid  in range(0, k):
            distance[index_centroid] = SSE(data_points[index_point], centroids[index_centroid])
        label = assign_label_cluster(distance, data_points[index_point], centroids)
        centroids[label[0]] =  SSE(label[1], centroids[label[0]])

        if iteration == (total_iteration - 1):
            cluster_label.append(label)

    return [cluster_label, centroids]

def print_label_data(result):
    print("k-means Clustering:\n")
    for data in result[0]:
        print("data point:{}".format(data[1]))
        print("cluster number:{} \n".format(data[0]))
    print("Last centroids position: \n {}".format(result[1]))

def random_centroids()
    centroids = []

    return np.array(centroids)


if __name__ == "__main__":


    # Import data (currently local file)
    csv_file = 'C:\\Users\\JJ\Desktop\\School 2019\\CS4375\Assignment 3\\Health-Tweets\\goodhealth.txt'
    headers = ['ID','Timestamp', 'Tweets']
    df = pd.read_csv(csv_file, sep='|', dtype=str, header=None, names=headers)
    data_points = (csv_file, " ")
    centroids = random_centroids()
    total_iteration = 100


    [cluster_label, new_centroids] = iterate_k_means(data_points, centroids, total_iteration)
    print_label_data([cluster_label, new_centroids])
    print()
    # Preprocess data

    # Remove id and timestamp column
    df = df.drop(labels=['ID','Timestamp'], axis=1)

    # Remove any word that starts with the symbol @
    # Remove any hashtag symbols
    # Remove any URL
    # Convert every word to lowercase
    for i in df.index:
        temp = df.at[i, 'Tweets']
        df.at[i, 'Tweets'] = preprocess(temp)