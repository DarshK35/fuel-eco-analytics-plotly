import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash()

app.layout = html.Div(children=[
    html.H1(children='Simple plot using Dash'),
    dcc.Graph(
        id='example',
        figure={
            'data': [
                {'x': [1, 2, 3, 4, 5, 6], 'y': [9, 6, 4, 2, 1, 0], 'type': 'line', 'name': 'Bikes'},
                {'x': [1, 2, 3, 4, 5, 6], 'y': [8, 7, 2, 9, 5, 3], 'type': 'bar', 'name': 'Cars'},
            ],
            'layout': {
                'title': 'Basic Dash Example'
            }
        }
    )
])

if __name__=='__main__':
    app.run_server(debug=True)