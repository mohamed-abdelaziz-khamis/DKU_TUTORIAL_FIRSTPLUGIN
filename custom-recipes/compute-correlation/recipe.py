# Code for custom code recipe compute-correlation (imported from a Python recipe)

# To finish creating your custom recipe from your original PySpark recipe, you need to:
#  - Declare the input and output roles in recipe.json
#  - Replace the dataset names by roles access in your code
#  - Declare, if any, the params of your custom recipe in recipe.json
#  - Replace the hardcoded params values by acccess to the configuration map

# See sample code below for how to do that.
# The code of your original recipe is included afterwards for convenience.
# Please also see the "recipe.json" file for more information.

# import the classes for accessing DSS objects from the recipe
import dataiku
# Import the helpers for custom recipes
from dataiku.customrecipe import *

# Inputs and outputs are defined by roles. In the recipe's I/O tab, the user can associate one
# or more dataset to each input and output role.
# Roles need to be defined in recipe.json, in the inputRoles and outputRoles fields.

# To  retrieve the datasets of an input role named 'input_A' as an array of dataset names:
input_A_names = get_input_names_for_role('input_A_role')
# The dataset objects themselves can then be created like this:
input_A_datasets = [dataiku.Dataset(name) for name in input_A_names]

# For outputs, the process is the same:
output_A_names = get_output_names_for_role('main_output')
output_A_datasets = [dataiku.Dataset(name) for name in output_A_names]


# The configuration consists of the parameters set up by the user in the recipe Settings tab.

# Parameters must be added to the recipe.json file so that DSS can prompt the user for values in
# the Settings tab of the recipe. The field "params" holds a list of all the params for wich the
# user will be prompted for values.

# The configuration is simply a map of parameters, and retrieving the value of one of them is simply:
my_variable = get_recipe_config()['parameter_name']

# For optional parameters, you should provide a default value in case the parameter is not present:
my_variable = get_recipe_config().get('parameter_name', None)

# Note about typing:
# The configuration of the recipe is passed through a JSON object
# As such, INT parameters of the recipe are received in the get_recipe_config() dict as a Python float.
# If you absolutely require a Python int, use int(get_recipe_config()["my_int_param"])


#############################
# Your original recipe
#############################

# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np

# Read the input
input_dataset = dataiku.Dataset("wine_quality")
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

# Compute the correlation for each pair, and write a
# row in the output array
output = []
for pair in pairs:
    corr = df[[pair[0], pair[1]]].corr().iloc[0][1]
    output.append({"col0" : pair[0],
                   "col1" : pair[1],
                   "corr" :  corr})

# Write the output to the output dataset
output_dataset =  dataiku.Dataset("wine_correlation")
output_dataset.write_with_schema(pd.DataFrame(output))
