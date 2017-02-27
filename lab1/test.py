#!/usr/bin/python3

import numpy as np

# define
dataset_file = "affinity_dataset.txt"

# display the first 5 lines
x = np.loadtxt(dataset_file)
print(x[:5])
