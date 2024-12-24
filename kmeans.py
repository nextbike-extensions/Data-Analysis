import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans


more = []
with open('file2.txt') as file:
    for line in file:
        str1, str2, str3, _ = line.rstrip().split(',')
        more.append(np.array([float(str1), float(str2), float(str3)]))
more = np.array(more)

kmeans = KMeans(n_clusters=1000, random_state=42)
kmeans.fit(more)

centroids = kmeans.cluster_centers_
labels = kmeans.labels_

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(more[:, 0], more[:, 1], more[:, 2], c=labels, s=30, cmap='viridis', label='data sample')

ax.scatter(centroids[:, 0], centroids[:, 1], centroids[:, 2], s=200, c='red', marker='X', label='Centroids')

ax.set_title("bikez")
ax.set_xlabel("longitude")
ax.set_ylabel("latitude")
ax.set_zlabel("weekday")
ax.legend()
# ax.view_init(elev=90, azim=90)

plt.show()

