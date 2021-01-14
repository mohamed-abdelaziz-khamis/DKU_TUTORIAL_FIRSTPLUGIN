from compute_corr import *

# import the classes for accessing DSS objects from the recipe
import dataiku
# Import the helpers for custom recipes
from dataiku.customrecipe import *

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

# Write the output to the output dataset
output_dataset =  output_datasets[0]
output_dataset.write_with_schema(pd.DataFrame(output))