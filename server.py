import dash
import json
import numpy as np
import pandas as pd

from dash import dcc, html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

from plotly import express as px
from plotly import subplots as sp
from plotly import graph_objects as go

# Importing dataset and interpretations
data = pd.read_csv("Dataset/data_18_v4.csv")
with open("./long_text.json", 'r') as file:
	long_text = json.load(file)
with open("./catppuccin_mocha.json", 'r') as file:
	colors = json.load(file)

app = dash.Dash("Dashboard")

continuous_fields = {
	"displ": "Displacement",
	"city_mpg": "City MPG",
	"hwy_mpg": "Highway MPG",
	"cmb_mpg": "Combined MPG",
	"cyl": "Number of Cylinders",
	"air_pollution_score": "Air Pollution Score",
	"greenhouse_gas_score": "Greenhouse Gas Score"
}
score_fields = {
	"air_pollution_score": "Air Pollution Score",
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
	color_seq = list(colors.values())[:len(data['veh_class'].unique())]
	figure = px.sunburst(
		data,
		path = ['veh_class', 'fuel'],
		values = 'air_pollution_score',
		color_discrete_sequence = color_seq,
		height = 720,
		width = 720
	)
	figure.update_layout(
		title = "Air Pollution Score Comparison between Vehicle Classes",
		title_font = dict(color = colors["subtext0"]),
		plot_bgcolor = colors["surface1"],
		paper_bgcolor = colors["surface2"]
	)
	return figure
def static_pie():
	color_seq = list(colors.values())[:len(data['veh_class'].unique())]

	class_count = data['veh_class'].value_counts().reset_index()
	class_count.columns = [
		'veh_class', 'count'
	]

	figure = px.pie(
		class_count,
		values = 'count',
		names = 'veh_class',
		color_discrete_sequence = color_seq,
		height = 720,
		width = 720
	)

	figure.update_layout(
		title = 'Vehicle Class Distribution',
		title_font = dict(color = colors["subtext0"]),
		legend_font = dict(color = colors["subtext0"]),
		plot_bgcolor = colors["surface1"],
		paper_bgcolor = colors["surface2"]
	)
	return figure
def static_stack_bar():
	color_seq = list(colors.values())[:len(data['fuel'].unique())]
	veh_dist = data.groupby(['veh_class', 'fuel']).size().reset_index(name = 'count')
	
	figure = px.bar(
		veh_dist,
		x = 'count',
		y = 'veh_class',
		color = 'fuel',
		color_discrete_sequence = color_seq,
		orientation = 'h',
		height = 840,
		width = 1280
	)
	
	figure.update_layout(
		title = 'Vehicle and Fuel Type Distribution',
		xaxis_title = 'Count',
		yaxis_title = 'Vehicle Class',
		legend_title = 'Fuel Type',
		title_font = dict(color = colors["subtext0"]),
		legend_font = dict(color = colors["subtext0"]),
		font = dict(color = colors["text"]),
		plot_bgcolor = colors["surface1"],
		paper_bgcolor = colors["surface2"]
	)

	return figure
def static_tree():
	color_seq = list(colors.values())[:len(data['veh_class'].unique())]

	figure = px.treemap(
		data,
		path = ['veh_class', 'trans'],
		values = 'greenhouse_gas_score',
		color_discrete_sequence = color_seq,
		height = 840,
		width = 1600
	)

	figure.update_layout(
		title = 'Greenhouse Gas Score vs Vehicle Class and Transmission Type',
		title_font = dict(color = colors["subtext0"]),
		font = dict(color = colors["text"]),
		plot_bgcolor = colors["surface1"],
		paper_bgcolor = colors["surface2"]
	)
	return figure
def static_pair():
	columns = ['city_mpg', 'hwy_mpg', 'cmb_mpg']
	figure = sp.make_subplots(
		rows = len(columns),
		cols = len(columns),
		shared_xaxes = False,
		shared_yaxes = False
	)

	for i, col1 in enumerate(columns):
		for j, col2 in enumerate(columns):
			if col1 == col2:
				trace = go.Histogram(
					x = data[col1],
					name = col1,
					showlegend = False,
					marker = dict(color = list(colors.values())[i * len(columns) + j])
				)
			else:
				trace = go.Scatter(
					x=data[col1],
					y=data[col2],
					mode='markers',
					marker = dict(color = list(colors.values())[i * len(columns) + j]),
					name = col1.split('_')[0] + ' vs ' + col2.split('_')[0]
				)
			figure.add_trace(trace, row=i + 1, col=j + 1)

	# Customize the layout
	for i, col in enumerate(columns):
		figure.update_xaxes(title_text=col, row=len(columns), col=i + 1)
		figure.update_yaxes(title_text=col, row=i + 1, col=1)

	figure.update_layout(
	    title='Miles Per Gallon Relationship',
		title_font = dict(color = colors["subtext0"]),
		plot_bgcolor = colors["surface1"],
		paper_bgcolor = colors["surface2"],
		font = dict(color = colors["text"]),
	    showlegend=False,
	    height=1000,
	    width=1000,
	)

	return figure


# Define app layout
app.title = "Fuel Economy Data Analysis"
app.layout = html.Div([
	# Heading Components
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
	
	# Scatter Plot Components
	html.Div([
		html.H2("Interactive Plot 1: Scatter plot"),
		
		html.Div([
			html.Label("X Value: ", className = 'scatter-drop-label'),
			dcc.Dropdown(
				id = 'scatter_x',
				options = continuous_fields,
				value = 'hwy_mpg',
				className = 'interactive-drop',
			),
			html.Br(),
			html.Label("Y Value: ", className = 'scatter-drop-label'),
			dcc.Dropdown(
				id = 'scatter_y',
				options = continuous_fields,
				value = 'city_mpg',
				className = 'interactive-drop'
			)
		], id = 'interactive-input'),
		dcc.Graph(id = 'scatter-plot'),
	], id = 'scatter', className = 'visual'),
	
	# Boxplot Components
	html.Div([
		html.H2("Interactive Plot 2: Box Plot"),

		html.Div([
			html.Label("Category: ", className = 'box-drop-label'),
			dcc.Dropdown(
				id = 'boxplot_x',
				options = categorical_fields,
				value = 'trans',
				className = 'interactive-drop'
			),
			html.Br(),
			html.Label("Value: ", className = 'box-drop-label'),
			dcc.Dropdown(
				id = 'boxplot_y',
				options = score_fields,
				value = 'greenhouse_gas_score',
				className = 'interactive-drop'
			)
		], id="interactive-input"),
		dcc.Graph(id = 'boxplot')
	], id = 'box', className = 'visual'),

	# Sunburst Components
	html.Div([
		html.H2("Static Plot 1: Sunburst Plot"),

		html.P(long_text["sunburst"]),
		dcc.Graph(id= ' sunburst-plot', figure = static_sunburst())
	], id = 'sunburst', className = 'visual'),

	# Pie Components
	html.Div([
		html.H2("Static Plot 2: Pie Chart"),
  
		html.P(long_text["pie"]),
		dcc.Graph(id = 'pie-chart', figure = static_pie())
	], id = 'pie', className = 'visual'),

	# Stacked Bar Plot Components
	html.Div([
		html.H2("Static Plot 3: Stacked Bar Plot"),

		html.P(long_text["stack-bar"]),
		dcc.Graph(id = 'stack-bar', figure = static_stack_bar())
	], id = 'stackbar', className = 'visual'),

	# Treemap Components
	html.Div([
		html.H2("Static Plot 4: Treemap"),

		html.P(long_text["treemap"]),
		dcc.Graph(id = 'treemap-plot', figure = static_tree())
	], id = 'treemap', className = 'visual'),

	# Pairplot Components
	html.Div([
		html.H2("Static Plot 5: Pair Plot"),

		html.P(long_text["pair"]),
		dcc.Graph(id = 'pair-plot', figure = static_pair())
	], id = 'pairplot', className = 'visual')
])

# Define callback to update scatter plot based on dropdown selections
@app.callback(
	Output('scatter-plot', 'figure'),
	[Input('scatter_x', 'value'), Input('scatter_y', 'value')]
)
def update_scatter_plot(x_axis_column, y_axis_column):
	figure = {
		'data': [
			{
				'x': data[x_axis_column],
				'y': data[y_axis_column],
				'mode': 'markers',
				'text': data['model'],  # Display model names on hover
				'marker': {'size': 10, 'color': colors["teal"]}
			}
		],
		'layout': {
			'title': f'Scatter Plot ({continuous_fields[x_axis_column]} vs {continuous_fields[y_axis_column]})',
			'xaxis': {'title': continuous_fields[x_axis_column]},
			'yaxis': {'title': continuous_fields[y_axis_column]},
			'font': {'color': colors["text"]},
			'plot_bgcolor': colors["surface1"],
			'paper_bgcolor': colors["surface2"],
			'height': 960,
			'width': 960
		}
	}
	return figure

@app.callback(
	Output('boxplot', 'figure'),
	[Input('boxplot_x', 'value'), Input('boxplot_y', 'value')]
)
def update_boxplot(x_column, y_column):
	figure = go.Figure()
	
	figure.add_trace(go.Box(
		x = data[x_column],
		y = data[y_column],
		boxpoints = 'outliers',
		hoverinfo = 'y+text',
		text = data['model'],
		marker = dict(
			size = 6,
			opacity = 0.6,
			color = colors["lavender"]
		)
	))

	# Customize the layout
	figure.update_layout(
		title = f'{categorical_fields[x_column]} vs {score_fields[y_column]}',
		xaxis_title = categorical_fields[x_column],
		yaxis_title = score_fields[y_column],
		font = dict(color = colors["text"]),
		plot_bgcolor = colors["surface1"],
		paper_bgcolor = colors["surface2"],
		height = 800,
		width = 50 + min(150 * len(data[x_column].unique()), 1400)

	)

	return figure

app.run_server(debug = True)
