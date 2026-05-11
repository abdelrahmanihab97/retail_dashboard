import pandas as pd
from dash import Dash, html, dcc, Input, Output
import plotly.express as px


app = Dash(__name__)

file_path = r"C:\Users\aihab\Desktop\retail_dashboard\datasets\retail_analytics_20k.csv.xls"

df = pd.read_csv(file_path)

data = df.groupby('quarter')['profit_egp'].sum().reset_index()

print(data)

fig = px.bar(data, x = 'quarter', y = 'profit_egp')



app.title = "Retail Analysis Dashboard"

app.layout = html.Div([
    html.H1("Retail Analysis Dashboard"),
    html.Div([
        html.H2("Profit Per Quantity"),
        dcc.Dropdown(
            id = 'dropdown_region',
            options=[
            {"label":r,"value":r} for r in df['region'].unique()
        ]),
        dcc.Graph(id = 'profit_per_region_fig'),
        dcc.Interval(
            id = 'interval_component',
            interval=5000,
            n_intervals=0
        )
    ]),
])

@app.callback(
        Output ("profit_per_region_fig", 'figure'),
        Input ('dropdown_region', 'value'),
        Input ('interval_component', 'n_intervals')
)
def update_dashboard(selected_region, n_intervals):
    df = pd.read_csv(file_path)
    if selected_region == None:
        data = df.groupby('quarter')['profit_egp'].sum().reset_index()
        fig = px.bar(data, x = 'quarter', y = 'profit_egp')
    else:
        filtered_df = df[df['region'] == selected_region]
        profit_per_region = filtered_df.groupby('quarter')['profit_egp'].sum().reset_index()
        fig = px.bar(profit_per_region, x = 'quarter', y = 'profit_egp')
    return fig

app.run()
