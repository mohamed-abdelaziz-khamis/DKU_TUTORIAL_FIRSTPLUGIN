from dataiku.customwebapp import *

# Access the parameters that end-users filled in using webapp config
# For example, for a parameter called "input_dataset"
# input_dataset = get_webapp_config()["input_dataset"]

from bokeh.io import curdoc
from bokeh.layouts import row, widgetbox
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Slider, TextInput, Select
from bokeh.plotting import figure
import dataiku
import pandas as pd

# Parameterize web app inputs
# Retrieve parameter values from the of map of parameters
input_dataset = get_webapp_config()['input_dataset']
x_column = get_webapp_config()['x_column']
y_column = get_webapp_config()['y_column']
time_column = get_webapp_config()['time_column']
cat_column = get_webapp_config()['cat_column']

# Set up data
mydataset = dataiku.Dataset(input_dataset)
df = mydataset.get_dataframe()

x = df[x_column]
y = df[y_column]
source = ColumnDataSource(data=dict(x=x, y=y))

# Set up plot
plot = figure(plot_height=400, plot_width=400, title=y_column+" by "+x_column,
              tools="crosshair,pan,reset,save,wheel_zoom",
              x_range=[min(x), max(x)], y_range=[min(y),max(y)])

plot.scatter('x', 'y', source=source)

# Set up layouts and add to document
inputs = widgetbox()

curdoc().add_root(row(inputs, plot, width=800))

# Set up widgets
text = TextInput(title="Title", value=y_column+" by "+x_column)
time = df[time_column]
min_year = Slider(title="Time start", value=min(time), start=min(time), end=max(time), step=1)
max_year = Slider(title="Time max", value=max(time), start=min(time), end=max(time), step=1)
cat_categories = df[cat_column].unique().tolist()
cat_categories.insert(0,'All')
category = Select(title="Category", value="All", options=cat_categories)

def update_title(attrname, old, new):
    plot.title.text = text.value

def update_data(attrname, old, new):
    category_value = category.value
    selected = df[(time>=min_year.value) & (time<=max_year.value)]
    if (category_value != "All"):
        selected = selected[selected[cat_column].str.contains(category_value)==True]
    # Generate the new plot
    x = selected[x_column]
    y = selected[y_column]
    source.data = dict(x=x, y=y)
    
# Set up callbacks
text.on_change('value', update_title)

for w in [min_year, max_year, category]:
    w.on_change('value', update_data)

inputs = widgetbox(text, min_year, max_year, category)
