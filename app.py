import dash
import fastf1
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
from dash import Dash, html, dash_table


session = fastf1.get_session(2023, 1, 'R')
session.load(telemetry=False, weather=False)
results = session.results
results_df = pd.DataFrame(results)

app = dash.Dash()
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}
app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Fast F1 Dashboard',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    dash_table.DataTable(data=results_df.to_dict('records'))
])

if __name__ == '__main__':
    app.run_server(debug=True)
