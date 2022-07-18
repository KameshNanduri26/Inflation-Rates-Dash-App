import dash
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# reading the data            
df = pd.read_csv('modified_data.csv', index_col=0)
cols = df.columns.tolist()


external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
                "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]


# creating dash app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# layout of the app
app.layout = html.Div(
				children=[
					html.Div(
						children=[
							html.H1(
								children="Time Series of Inflation Rates",
								className='header-title'
							),
				        	html.P(
					            children="Analyze the behavior of inflation rates of countries"
					            " and the economic trade unions"
					            " between 1980 and 2022",
					            className='header-description'
				        	),
				        	html.P(
								children="📈📉", className="header-emoji"
							),
						],
						className='header'
					),					
			        html.Div(
			        	children=[
			        		html.H3(
			        			children="Select the Country or Economic Trade Unions"
			        		),
			        		dcc.Dropdown(id='country-filter', options=cols, value='India', clearable=False)
			        	],
			        	className='menu'
			        ),
			        html.Div(
			        	children=[
			        		dcc.Graph(
				        		id="inflation-chart", config={"displayModeBar": False},
					    	),
			        	],
			        	className='card wrapper'
			        ),
				],
			)


@app.callback(
    [Output("inflation-chart", "figure")],
    [Input("country-filter", "value"),],
)
def update_chart(country):
	fig = px.area(df, x=df.index, y=country, title=f'Inflation rate for {country}',
				  template='simple_white', markers=True, color_discrete_sequence=["#00D100"])
	fig.update_traces(hovertemplate='Inflation Rate: %{y} <br>Year: %{x}')
	fig.update_layout(xaxis_title='Year', yaxis_title='Inflation Rate', xaxis_range=[1980,2022])
	return [fig]

if __name__ == "__main__":
    app.run_server(debug=True)