import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

CLUSTERS = 100

# Save plots in output directory
SAVE_PLOTS = False

# Select files for which you would like to create plots
MONDAY = True
TUESDAY = True
WEDNESDAY = True
THURSDAY = True
MONDAY_THURSDAY = False
FRIDAY = True
SATURDAY = True
SUNDAY = True
ALL_DATA = False

# Printing settings
N_BEST_CENTERS = 4

order = [MONDAY,
         TUESDAY,
         WEDNESDAY,
         THURSDAY,
         MONDAY_THURSDAY,
         FRIDAY,
         SATURDAY,
         SUNDAY,
         ALL_DATA
]

order_files = [
    "monday_data.txt",
    "tuesday_data.txt",
    "wednesday_data.txt",
    "thursday_data.txt",
    "monday_thursday_data.txt",
    "friday_data.txt",
    "saturday_data.txt",
    "sunday_data.txt",
    "all_data.txt"
]

dimensions = 0
prompt_flag = False
dimension_flag = False

for i in range(len(order)):
    current_file = open(f'txt_files/{order_files[i]}', 'r')
    dataset = []
    # Preparing np.arrays with data
    if os.stat(f'txt_files/{order_files[i]}').st_size == 0:
        if order[i]:
            raise Exception(f"{order_files[i]} is empty")
        else:
            continue
    if not order[i]:
        continue
    for line in current_file:
        data_piece = []
        if not dimension_flag:
            dimensions = len(line.rstrip().split(','))
            print(f"kmeans objects will be created for {dimensions} dimensional data\n")
            dimension_flag = True
        for value in line.rstrip().split(','):
            data_piece.append(float(value))

        dataset.append(np.array(data_piece))
        aa = line

    dataset = np.array(dataset)

    print(f"Creating plot for {order_files[i]}")

    kmeans = KMeans(n_clusters=CLUSTERS, random_state=42)
    kmeans.fit(dataset)

    centroids = kmeans.cluster_centers_
    labels = kmeans.labels_

    if dimensions == 3:
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(dataset[:, 0], dataset[:, 1], dataset[:, 2], c=labels, s=30, cmap='inferno')

        ax.scatter(centroids[:, 0], centroids[:, 1], centroids[:, 2], s=200, c='red', marker='X', label='Centroids')

        ax = plt.gca()
        ax.set_xlim([20.88, 21.22])
        ax.set_ylim([52.04, 52.36])
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        title = f"Freestanding bikes ({order_files[i]})"
        plt.title(title)
        if SAVE_PLOTS:
            plt.savefig(f'output/{title + '.png'}')
        plt.legend()


        plt.show()

    elif dimensions == 2:
        fig = plt.figure(figsize=(10, 8))
        plt.scatter(dataset[:, 0], dataset[:, 1], c=labels, s=30, cmap='inferno')

        plt.scatter(centroids[:, 0], centroids[:, 1], s=200, c='red', marker='X', label='Centroids')

        ax = plt.gca()
        ax.set_xlim([20.88, 21.22])
        ax.set_ylim([52.04, 52.36])
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        title = f"Freestanding bikes ({order_files[i]})"
        plt.title(title)
        plt.legend()
        if SAVE_PLOTS:
            plt.savefig(f'output/{title + '.png'}')
        plt.show()

    labels = kmeans.labels_
    unique_labels, counts = np.unique(labels, return_counts=True)

    allcenters = []

    most_points = -1
    coordinates = None
    for label, count, center in zip(unique_labels, counts, centroids):
        new = {
            'count': count,
            'coordinates': center
        }
        allcenters.append(new)
        if count > most_points:
            most_points = count
            coordinates = center
    print(f"Centroid: {most_points} points, center={coordinates}")
    allcenters.sort(key=lambda x: x['count'], reverse=True)
    print(f"{N_BEST_CENTERS} best points found:")
    for c in range(N_BEST_CENTERS):
        print(f"\t{allcenters[c]['coordinates']} with {allcenters[c]['count']} points")
