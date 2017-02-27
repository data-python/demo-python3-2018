#!/usr/bin/python3

import numpy as np

# define
dataset_file = "affinity_dataset.txt"

# display the first 5 lines
x = np.loadtxt(dataset_file)
print(x[:5])

# 数据样式
n_samples, n_features = x.shape
print("This dataset has {0} samples and {1} features".format(n_samples, n_features))


