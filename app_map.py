import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

from plotly import graph_objs as go

external_stylesheets = ['style.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'Claims'

df = pd.read_csv("data.csv")
df = df.set_index("country")
df["sum"] = df.groupby("country").sum()["amount"]


app.layout = html.Div([
    html.H1(
        "Claim Visualization Tool"
    ),
    html.Div([
        dcc.Graph(
            id='map-graph',
            animate=True,
            style={'margin-top': '20'},
            figure={
                'data': [go.Choropleth(
                    locationmode="country names",
                    locations=df.index,
                    z=df["sum"],
                )],
                'layout': {
                    "geo_scope": "africa"
                }
            },
            hoverData={'points': [{'location': 'france'}]}
        ),
        dcc.Graph(
                id='scatter-graph'
            )
    ], style={"columnCount": 2})
])

@app.callback(
    dash.dependencies.Output('scatter-graph', 'figure'),
    [dash.dependencies.Input('map-graph', 'hoverData')]
    )
def update_graph(hoverData):
    country = hoverData["points"][0]["location"]
    return {
        'data': [go.Scatter(
            x=df.loc[country, "claim_local_id"],
            y=df.loc[country, "amount"],
            text=country,
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        "layout": go.Layout(
            xaxis={
                'title': "Claim day",
                'type': 'linear'
            },
            yaxis={
                'title': "Amount",
                'type': 'linear'    
            },
            hovermode='closest'
        )
    }

if __name__ == '__main__':
    app.run_server(debug=True)