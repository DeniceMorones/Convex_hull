# -*- coding: utf-8 -*-
"""convex_hull.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1dJqzyv5gIPnfZ08d3WA_sPN78afhB9Xh
"""

#Denice Estefania Rico Morones

import anndata as ad
from scipy.spatial import ConvexHull
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches


adata = ad.read_h5ad('1c2d14d8-32d4-41be-b38d-ba975ad10efa.h5ad')

print(adata)

umap_coords = adata.obsm['X_UMAP']
cluster_ids = adata.obs['cluster_id']

def convex_hulls(coords, cluster_ids):
    res = {}
    for cluster_id in np.unique(cluster_ids):
        cluster_coords = coords[cluster_ids == cluster_id]
        r = ConvexHull(cluster_coords)
        res[cluster_id] = r
    return res

res = convex_hulls(umap_coords, cluster_ids)

def grafica(coords, cluster_ids, res):
    plt.figure(figsize=(10, 8))
    uni_clusters = np.unique(cluster_ids)
    colores = plt.cm.get_cmap('tab10', len(uni_clusters))

    for i, cluster_id in enumerate(uni_clusters):
        cluster_coords = coords[cluster_ids == cluster_id]
        plt.scatter(cluster_coords[:, 0], cluster_coords[:, 1], s=5, color=colores(i), label=f'Cluster {cluster_id}')

        r = res[cluster_id]
        r_coords = cluster_coords[r.vertices]
        r_patch = patches.Polygon(r_coords, color=colores(i), alpha=0.2)
        plt.gca().add_patch(r_patch)

    plt.legend()
    plt.title('UMAP y Convex Hull')
    plt.xlabel('UMAP 1')
    plt.ylabel('UMAP 2')
    plt.show()

grafica(umap_coords, cluster_ids, res)