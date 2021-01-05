# -*- coding: utf-8 -*-
from dataiku.customrecipe import *
import dataiku
import pandas as pd, numpy as np

# Retrieve array of dataset names from 'input' role, then create datasets
input_names = get_input_names_for_role('input')
input_datasets = [dataiku.Dataset(name) for name in input_names]

# For outputs, the process is the same:
output_names = get_output_names_for_role('main_output')
output_datasets = [dataiku.Dataset(name) for name in output_names]

# Retrieve parameter values from the of map of parameters
threshold = get_recipe_config()['threshold']

# Read the input
input_dataset = input_datasets[0]
df = input_dataset.get_dataframe()
column_names = df.columns

# We'll only compute correlations on numerical columns
# So extract all pairs of names of numerical columns
pairs = []
for i in range(0, len(column_names)):
    for j in range(i + 1, len(column_names)):
        col1 = column_names[i]
        col2 = column_names[j]
        if df[col1].dtype == "float64" and \
           df[col2].dtype == "float64":
            pairs.append((col1, col2))

for pair in pairs:
    corr = df[[pair[0], pair[1]]].corr().iloc[0][1]
    if np.abs(corr) > threshold:
      output.append({"col0" : pair[0],
                     "col1" : pair[1],
                     "corr" :  corr})

# Write the output to the output dataset
output_dataset =  output_datasets[0]
output_dataset.write_with_schema(pd.DataFrame(output))
