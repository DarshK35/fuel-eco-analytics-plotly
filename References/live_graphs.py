import dash
from dash.dependencies import Output, Input, State
from dash import dcc
from dash import html
import plotly
import random
import plotly.graph_objs as go
from collections import deque

X = deque(maxlen=20)
X.append(1)
Y = deque(maxlen=20)
Y.append(1)


app = dash.Dash(__name__)
app.layout = html.Div(
    [
        dcc.Graph(id='live-graph', animate=True),
        dcc.Interval(
            id='graph-update',
            interval=500,
            n_intervals=0
        ),

        html.Button("Pause/Resume (SpaceBar)", 'pause-button', n_clicks = 0)
    ]
)

@app.callback(Output('live-graph', 'figure'),
              [Input('graph-update', 'n_intervals')],
              [State('pause-button', 'n_clicks')])
def update_graph_scatter(n, n_clicks):
    if n_clicks == None:
        clicked = 0

    if n_clicks % 2 == 1:
        return dash.no_update

    X.append(X[-1]+1)
    Y.append(Y[-1]+Y[-1]*random.uniform(-0.1,0.1))

    data = plotly.graph_objs.Scatter(
            x=list(X),
            y=list(Y),
            name='Scatter',
            mode= 'lines+markers'
            )

    return {'data': [data],'layout' : go.Layout(xaxis=dict(range=[min(X),max(X)]),
                                                yaxis=dict(range=[min(Y),max(Y)]),)}


if __name__ == '__main__':
    app.run_server(debug=True)
