import dash
import numpy as np
import pandas as pd
import seaborn as sns

from dash import dcc, html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

from plotly import express as px
from matplotlib import pyplot as plt

from plotly import graph_objects as go

data = pd.read_csv("Dataset/data_18_v4.csv")
app = dash.Dash("Dashboard")

identity_fields = {
	"model": "Car Model"
}

continuous_fields = {
	"displ": "Displacement",
	"air_pollution_score": "Air Pollution Score",
	"city_mpg": "City MPG",
	"hwy_mpg": "Highway MPG",
	"cmb_mpg": "Combined MPG",
	"greenhouse_gas_score": "Greenhouse Gas Score"
}

categorical_fields = {
	"cyl": "Number of Cylinders",
	"trans": "Transmission Type",
	"drive": "Drive Type",
	"fuel": "Fuel Type",
	"veh_class": "Vehicle Class",
	"smartway": "SmartWay"
}

# Define app layout
app.layout = html.Div([
	
	html.H1("Interactive Dash App"),
	
	# Scatter Plot components
	dcc.Dropdown(
		id='scatter_x',
		options=continuous_fields,
		value='hwy_mpg'
	),
	dcc.Dropdown(
		id='scatter_y',
		options=continuous_fields,
		value='city_mpg'
	),
	dcc.Graph(id='scatter-plot'),


	# Heatmap Components
	dcc.Dropdown(
		id = 'boxplot_x',
		options = categorical_fields,
		value = 'trans',
	),
	dcc.Dropdown(
		id = 'boxplot_y',
		options = continuous_fields,
		value = 'greenhouse_gas_score'
	),
	dcc.Graph(id='boxplot')
])

# Define callback to update scatter plot based on dropdown selections
@app.callback(
	Output('scatter-plot', 'figure'),
	[Input('scatter_x', 'value'),
	 Input('scatter_y', 'value')]
)
def update_scatter_plot(x_axis_column, y_axis_column):
	figure = {
		'data': [
			{
				'x': data[x_axis_column],
				'y': data[y_axis_column],
				'mode': 'markers',
				'text': data['model'],  # Display model names on hover
				'marker': {'size': 10}
			}
		],
		'layout': {
			'title': f'Scatter Plot ({continuous_fields[x_axis_column]} vs {continuous_fields[y_axis_column]})',
			'xaxis': {'title': continuous_fields[x_axis_column]},
			'yaxis': {'title': continuous_fields[y_axis_column]}
		}
	}
	return figure

@app.callback(
	Output('boxplot', 'figure'),
	[Input('boxplot_x', 'value'),
	 Input('boxplot_y', 'value')]
)
def update_heatmap(x_column, y_column):
	figure = go.Figure()
	
	figure.add_trace(go.Box(
		x = data[x_column],
		y = data[y_column],
		boxpoints = 'outliers',
		hoverinfo = 'y+text',
		text = data['model'],
		marker = dict(
			size = 6,
			opacity = 0.6
		)
	))

	# Customize the layout
	figure.update_layout(
		title = f'Box Plot ({categorical_fields[x_column]} vs {continuous_fields[y_column]})',
		xaxis_title = categorical_fields[x_column],
		yaxis_title = continuous_fields[y_column]
	)

	return figure


app.run_server()