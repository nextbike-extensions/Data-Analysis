from stringprep import b1_set

import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import os

files = [file for file in os.listdir('data')]

other = []
friday = []
saturday = []
sunday = []
all_data = []

names = ["Monday - Thursday", "Friday", "Saturday", "Sunday", "All days"]
all_data = [other, friday, saturday, sunday, all_data]
all_kmeans = []

for i in range(len(files)):
    print(names[i])
    with open(f'data/{files[i]}') as file:
        for line in file:
            str1, str2, _ = line.rstrip().split(',')
            all_data[i].append(np.array([float(str1), float(str2)]))
    all_data[i] = np.array(all_data[i])

    kmeans = KMeans(n_clusters=80, random_state=42)
    kmeans.fit(all_data[i])

    centroids = kmeans.cluster_centers_
    labels = kmeans.labels_
    all_kmeans.append(kmeans)

    fig = plt.figure(figsize=(10, 8))
    # ax = fig.add_subplot(111, projection='3d')
    plt.scatter(all_data[i][:, 0], all_data[i][:, 1], c=labels, s=30, cmap='viridis')

    plt.scatter(centroids[:, 0], centroids[:, 1], s=200, c='red', marker='X', label='Centroids')

    ax = plt.gca()
    ax.set_xlim([20.88, 21.22])
    ax.set_ylim([52.04, 52.36])
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    title = f"Freestanding bikes on {names[i]}"
    plt.title(title)
    plt.savefig(title + '.png')
    plt.legend()

    # ax.view_init(elev=0, azim=4)

    plt.show()
    # for i, center in enumerate(centroids):
        # print(center)

    labels = kmeans.labels_
    unique_labels, counts = np.unique(labels, return_counts=True)

    allcentrs = []


    best = None
    maxx = 0
    cent = None
    # print("Number of points belonging to each centroid:")
    for label, count, center in zip(unique_labels, counts, centroids):
        neww = {
            'label': label,
            'count': count,
            'center': center
        }
        allcentrs.append(neww)
        if count > maxx:
            best = label
            maxx = count
            cent = center
    print(f"Centroid {best}: {maxx} points, center={cent}")
    allcentrs.sort(key=lambda x: x['count'], reverse=True)
    print(allcentrs[:10])

