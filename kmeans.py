import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs

# Generowanie przykładowych danych
X, _ = make_blobs(n_samples=10, n_features=2, centers=3, random_state=42)

more = []
with open('file.txt') as file:
    for line in file:
        str1, str2 = line.rstrip().split(',')
        more.append(np.array([float(str1), float(str2)]))
more = np.array(more)
print(more)
print(type(X))

# Tworzenie modelu KMeans
kmeans = KMeans(n_clusters=30, random_state=42)
kmeans.fit(more)

# Przewidywanie dla nowego punktu


# Wizualizacja
plt.scatter(more[:, 0], more[:, 1], c=kmeans.labels_, cmap='viridis', s=30, label="Punkty danych")
plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], s=200, c='red', marker='X', label='Centroidy')
plt.title("Przewidywanie klastra dla nowego punktu")
plt.legend()
plt.show()
