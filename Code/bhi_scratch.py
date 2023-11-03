# !/usr/bin/env python3
# -*- coding:utf-8 -*-

# @Time    : 2023/11/01 14:00
# @Author  : Sammean Shaw
# @FileName: bhi_scratch.py
import numpy as np
from sklearn.mixture import GaussianMixture


def calculate_bhi(t1, t2, t2_star, flair):
    # Assuming t1, t2, t2_star, and flair are numpy arrays containing the MRI data

    # Create a 4D array by stacking the 3D MRI sequences
    mri_data = np.stack((t1, t2, t2_star, flair), axis=-1)

    # Reshape the data into a 2D array (voxels x sequences)
    mri_data = mri_data.reshape((-1, 4))

    # Apply Gaussian Mixture Model clustering
    n_clusters = 2  # Two clusters: healthy and abnormal
    gmm = GaussianMixture(n_components=n_clusters, random_state=0)
    gmm.fit(mri_data)

    # Get the posterior probabilities of belonging to the "healthy" cluster
    posterior_probabilities = gmm.predict_proba(mri_data)[:, 0]  # Index 0 corresponds to the "healthy" cluster

    # Reshape posterior probabilities back to the original 3D shape
    bhi_3d = posterior_probabilities.reshape(t1.shape)

    # Calculate the mean BHI value for each subject
    bhi_mean = np.mean(bhi_3d)

    return bhi_mean


# Example usage
t1_data = np.random.rand(64, 64, 64)  # Replace with your actual MRI data
t2_data = np.random.rand(64, 64, 64)
t2_star_data = np.random.rand(64, 64, 64)
flair_data = np.random.rand(64, 64, 64)

bhi_value = calculate_bhi(t1_data, t2_data, t2_star_data, flair_data)
print("Brain Health Index (BHI):", bhi_value)