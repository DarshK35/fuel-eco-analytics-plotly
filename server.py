import dash
import json
import numpy as np
import pandas as pd

from dash import dcc, html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

from plotly import express as px
from plotly import graph_objects as go

# Importing dataset and interpretations
data = pd.read_csv("Dataset/data_18_v4.csv")
with open("./long_text.json", 'r') as file:
	long_text = json.load(file)

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

# Static visualisation functions
def static_sunburst():
    figure = px.sunburst(
        data,
        path = ['veh_class', 'fuel'],
        values = 'air_pollution_score'
    )
    figure.update_layout(
        title = "Air Pollution Score Comparison between Vehicle Classes"
    )
    return figure


# Define app layout
app.title = "Fuel Economy Data Analysis"
app.layout = html.Div([	
	html.Div([
		html.H1("Fuel Economy Data Analytics"),
		html.P(long_text["students"][0]),
		html.P([
			long_text["students"][1],
			html.Br(),
			long_text["students"][2],
			html.Br(),
			long_text["students"][3]
		])
	], className = 'header'),
	
	# Scatter Plot components
	html.Div([
		html.H2("Interactive Plot 1: Scatter plot"),
		dcc.Dropdown(
			id = 'scatter_x',
			options = continuous_fields,
			value = 'hwy_mpg',
			className = 'scatter-drop'
		),
		dcc.Dropdown(
			id = 'scatter_y',
			options = continuous_fields,
			value = 'city_mpg',
			className = 'scatter-drop'
		),
		dcc.Graph(id='scatter-plot'),
	], className = 'scatter'),
	
	# Boxplot Components
	html.Div([
		html.H2("Interactive Plot 2: Box Plot"),
		dcc.Dropdown(
			id = 'boxplot_x',
			options = categorical_fields,
			value = 'trans',
			className = 'box-drop'
		),
		dcc.Dropdown(
			id = 'boxplot_y',
			options = continuous_fields,
			value = 'greenhouse_gas_score',
			className = 'box-drop'
		),
		dcc.Graph(id='boxplot')
	], className = 'box'),

	# Sunburst Components
	html.Div([
		html.H2("Static Plot 1: Sunburst Plot"),

	    dcc.Graph(id='sunburst-plot', figure = static_sunburst())
	], className = 'sunburst')
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

app.run_server(debug = True)
