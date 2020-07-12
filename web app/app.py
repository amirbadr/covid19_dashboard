# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 17:41:41 2020

@author: omidb
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table
import plotly.graph_objects as go
import pandas as pd
import json
import pickle
import _pickle as cPickle
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

from utils import Canada_fig, confirmed_graph, Canada_provinces_map, US_map, Canada_trend_map

### Canada Trend Map
with open('data/Trend Table.pickle', 'rb') as handle:
    Canada_trend_table = cPickle.load(handle)
with open('data/CA_regions_trend_json.pickle', 'rb') as handle:
    canada_trend_json = cPickle.load(handle)
Canada_trends_map = Canada_trend_map(Canada_trend_table, canada_trend_json)

### Canada Province-level Map
with open('data/Canada_map_data.pickle', 'rb') as handle:
    Canada_map_table = cPickle.load(handle)
with open('data/Canada 4326.pickle', 'rb') as handle:
    canada_province_json = cPickle.load(handle)
fig_Canada = Canada_fig(Canada_map_table, canada_province_json)

####  Confirmed, Death, Recovered, Testing for time-series
with open('data/Canada Confirmed Cases.pickle', 'rb') as handle:
    Confirmed_Canada = cPickle.load(handle)
with open('data/Canada Confirmed Cases Daily.pickle', 'rb') as handle:
    Daily_Confirmed_Canada = cPickle.load(handle)
fig_confirmed_timeseries_canada = confirmed_graph(Daily_Confirmed_Canada)

with open('data/Canada Death Cases.pickle', 'rb') as handle:
    Death_Canada = cPickle.load(handle)
with open('data/Canada Death Cases Daily.pickle', 'rb') as handle:
    Daily_Death_Canada = cPickle.load(handle)
    
with open('data/Canada Recover Cases.pickle', 'rb') as handle:
    Recovered_Canada = cPickle.load(handle)
with open('data/Canada Recover Cases Daily.pickle', 'rb') as handle:
    Daily_Recovered_Canada = cPickle.load(handle)

with open('data/Canada Testing Cases.pickle', 'rb') as handle:
    Testing_Canada = cPickle.load(handle)
with open('data/Canada Testing Cases Daily.pickle', 'rb') as handle:
    Daily_Testing_Canada = cPickle.load(handle)       
      
## Canada Summary table
with open('data/Canada_data_table.pickle', 'rb') as handle:
    Canada_data_table = cPickle.load(handle)

## Canada Regions Map    
with open('data/Canada regions Table.pickle', 'rb') as handle:
    Canada_cities_report = cPickle.load(handle)    
with open('data/Canada regions location.pickle', 'rb') as handle:
    canada_regions_json = cPickle.load(handle)
Canada_regions_map = Canada_provinces_map(Canada_cities_report, canada_regions_json, 'Ontario')

## US County Map
with open('data/US_Confirmed_Death.pickle', 'rb') as handle:
    US_Confirmed_Death = cPickle.load(handle)
US_Confirmed_Death.loc[:,'countyFIPS'] = US_Confirmed_Death.loc[:,'countyFIPS'].apply(lambda x : str("{:05d}".format(int(x))))
with open('data/US_County.pickle', 'rb') as handle:
    us_county_json = cPickle.load(handle)
fig_us = US_map(US_Confirmed_Death, us_county_json)


app = dash.Dash(__name__, 
                external_stylesheets = external_stylesheets, 
                prevent_initial_callbacks = True,
                eager_loading = True)
server = app.server

app.layout = html.Div(children=[
    dcc.Tabs([        
    dcc.Tab(label='Canada Total Cases & Trend Map', children=[
    html.H5(children='Live Canada COVID-19 Dashboard'),
    dcc.Markdown('''
                 ###### This website is an interactive dashboard to report and monitor Coronavirus COVID-19 cases in Canada. 
    ''' , style={'fontSize': 14}),
    dcc.Markdown('''
                 > 
                 > **This dashboard is updated several times a day.** All the data in this dashboard is gathered from Canada provincial websites.
                 >
                 > This dashboard is built using [Dash interactive Python framework](https://plotly.com/dash/). It automatically scrapes the Canada COVID-19 websites using Python and updates the metrics.
                 > 
                 > This dashboard is well-suited for laptop and desktop views and not currently perfectly designed for mobile phones.
                 > 
                 > All the maps and charts in this dashboard are interactive and you can hover over and zoom in and zoom out to different provinces and regions.
                 >
     ''' , style={'fontSize': 14}),
    #html.Div([
    #        html.Div('This website is an interactive dashboard that tracks Coronavirus COVID-19 cases in Canada.', style={'fontSize': 14}),
    #        html.Strong('This website is updated several times a day.', style={ 'fontSize': 14}),
    #],  style={'fontSize': 14}),
    html.Hr(),
    
     html.Div([
            html.Div([
                    html.H6('COVID-19 Confirmed cases in Canada', style = { 'fontSize': 18, 'vertical-align': 'middle', 'text-align': 'center'})
                    ]),
            dcc.Graph(
                id = 'canada-graph',
                figure = fig_Canada,
            )
            
            
     ],  style={"width" : "90%", 'margin': '0 auto'}),
     html.Hr(),
     dcc.Markdown('''
                 > 
                 > The following map is the week over week percentage change in COVID-19 confirmed cases in Canada regions.
                 > 
                 > The **red** areas are the regions that the trend is **positive** meaning the number of the COVID-19 confirmed cases are increasing compared to the previous week.
                 >
                 > The **blue** areas are the regions that the trend is **negative** meaning the number of the COVID-19 confirmed cases are decreasing compared to the previous week.
                 >
                 ''' , style={'fontSize': 14}),       
     html.Div([
             html.Div([
                    html.H6('COVID-19 Trend in Canada', style = { 'fontSize': 18, 'vertical-align': 'middle', 'text-align': 'center'})
                    ]),
            dcc.Graph(
                id = 'canada-trend-graph',
                figure = Canada_trends_map,
            )
     ],  style={"width" : "90%", 'margin': '0 auto'}),
     dcc.Markdown('''
                 > 
                 > All the content of this dashboard is gathered from the following official provincial or territorial COVID-19 webpages and flatten.ca website:
                 > 
                 ''' , style={'fontSize': 14}),
    html.Div(children=[html.A('Canada', href='https://www.canada.ca/en/public-health/services/diseases/2019-novel-coronavirus-infection.html#a1', 
                              style={'color':'black', 'fontSize': 15})] ),
    html.Div(children=[html.A('Ontario', href='https://www.ontario.ca/page/2019-novel-coronavirus#section-0', 
                              style={'color':'black', 'fontSize': 15})] ),
    html.Div(children=[html.A('FLATTEN', href='https://flatten.ca/', 
                              style={'color':'black', 'fontSize': 15})] ),
    html.Div(children=[html.A('British Columbia', href='http://www.bccdc.ca/about/news-stories/stories/2020/information-on-novel-coronavirus', 
                              style={'color':'black', 'fontSize': 15})] ),
    html.Div(children=[html.A('Alberta', href='https://www.alberta.ca/covid-19-alberta-data.aspx', 
                              style={'color':'black', 'fontSize': 15})] ),
    html.Div(children=[html.A('Quebec', href='https://www.quebec.ca/en/health/health-issues/a-z/2019-coronavirus/situation-coronavirus-in-quebec', 
                              style={'color':'black', 'fontSize': 15})] ),
    dcc.Markdown('''
                 >
                 >This dashboard is designed and maintained by Amir Badr [LinkedIn](https://www.linkedin.com/in/amirbadr9/) and Omid Badr [LinkedIn](https://www.linkedin.com/in/omidbadr/) as a personal project for educational and informative purposes.
                 >
                '''),
     ]),
    #html.Hr(),
    
    dcc.Tab(label='Canada Cities Cases', children=[
    dcc.Markdown('''
                 > 
                 > The following interactive map is COVID-19 cases in Canada by city and region. Please select the province and the map will zoom in to that region.
                 > 
                 > Please note that only reported cases with a known location by local geographic area are included in the map.
                 ''' , style={'fontSize': 14}),
    
     html.Div([
            html.Div([
                    html.H6('Select the Province', style = {'margin-right':'0em', 'margin-left':'1em', 'margin-top':'-0.1em', 'fontSize': 14})
                    ]),
            ]),
    html.Div([
            dcc.Dropdown(
                options = [{'label': col, 'value': col} for col in ['Ontario', 'Montreal', 'Quebec', 'British Columbia', 'Alberta', 'Manitoba', 'Saskatchewan', 'New Brunswick', 'Newfoundland and Labrador', 'Nova Scotia', 'Canada']],
                value = 'Ontario', 
                style = {'width':'250px', 'margin-right':'6em', 'margin-left':'0.5em', 'margin-top':'-0.3em'},
                id = 'province_selection2'
            )]),

    html.Div([
            html.Div([
                    html.H6('Cumulative COVID-19 Confirmed cases in Canada regions', style = { 'fontSize': 18, 'vertical-align': 'middle', 'text-align': 'center'})
                    ]),
            dcc.Graph(
                id = 'canada-cities-graph',
                figure = Canada_regions_map,
            )
     ],  style={"width" : "90%" , 'margin': '0 auto'}),

     ]),
    #html.Hr(),
    
    dcc.Tab(label='Canada Provinces Time Series', children=[
    dcc.Markdown('''
                 > 
                 > The following figure is a time series bar chart for Cumulative COVID-19 cases by day. Please select the province and the metric.
                 > 
                 ''' , style={'fontSize': 14}),
    html.Div([
            html.Div([
                    html.H6('Select the Province', style = {'margin-right':'0em', 'margin-left':'1em', 'margin-top':'-0.1em', 'fontSize': 14})
                    ]),
            dcc.Dropdown(
                options = [{'label': col, 'value': col} for col in ['Ontario', 'Toronto','Canada', 'Quebec', 'British Columbia', 'Alberta', 'Manitoba', 'Saskatchewan', 'New Brunswick', 'Newfoundland and Labrador', 'Nova Scotia', 'Prince Edward Island', 'Yukon', 'Northwest Territories']],
                value = 'Ontario', 
                clearable = False,
                style = {'width':'250px', 'margin-right':'4em', 'margin-left':'0.5em', 'margin-top':'-0.3em', 'display': 'inline-block', 'font-size': "100%"},
                id = 'province_selection'
            ),
            html.Div([
                    html.H6('Daily / Total ', style = {'margin-right':'0em', 'margin-left':'1em', 'margin-top':'-0.1em', 'fontSize': 14})
                    ]),
            dcc.Dropdown(
                options = [{'label': col, 'value': col} for col in ['Daily', 'Total']],
                value = 'Daily', 
                style = {'width':'100px', 'margin-right':'4em', 'margin-left':'0.5em', 'margin-top':'-0.3em'},
                clearable = False,
                id = 'daily_selection'
            ),
            html.Div([
                    html.H6('Confirmed / Deaths / Recovered / Testing Cases', style = {'margin-right':'0em', 'margin-left':'0em', 'margin-top':'-0.1em','fontSize': 14})
                    ]),
            dcc.Dropdown(
                options = [{'label': col, 'value': col} for col in ['Number of Confirmed Cases','Number of Deaths', 'Number of Recovered Cases', 'Number of Testing']],
                value = 'Number of Confirmed Cases',
                style = {'width':'250px', 'margin-right':'1em', 'margin-left':'0.5em', 'margin-top':'-0.3em'},
                clearable = False,
                id = 'metrics_selection'
            ),
    ], style = {'display':'flex', 'text-align': 'left'}),
    
    html.Div([
        dcc.Graph(
           id = 'timeseries-canada-graph',
           figure = fig_confirmed_timeseries_canada,
           #config = {'autosizable' : True}
        ),
    ], style = {"width" : "70%" , 'margin': '0 auto'}),
    #html.Hr(),
     ]),
    dcc.Tab(label='Canada Provinces Summary Table', children=[
    dcc.Markdown('''
                 > 
                 > The following table highlights the toal and today confirmed and death cases in Canada provinces.
                 > 
                 ''' , style={'fontSize': 14}),
    html.Div([
        dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in Canada_data_table.columns],
            data=Canada_data_table.to_dict('records'),
            fill_width = True,
            style_cell={'textAlign': 'center', 'font_size':'16px', 'font_family':"'Oswald',sans-serif"},
            style_data_conditional=[
                      {'if': {'row_index': 'odd'},
                        'backgroundColor': 'rgb(248, 248, 248)'},
                         {'fontWeight': 'bold'}
                     ],
            style_header={
                'backgroundColor': 'rgb(2, 21, 70)',
                'color': 'white', 'textAlign': 'center'
                    }
            ),
        ],  style={'display':'felx', 'justify-content':'center', 'align-items':'center'}),
    ]),
    dcc.Tab(label='US COVID-19 Trend Map', children=[
    dcc.Markdown('''
                 > 
                 > The following map is the week over week percentage change in COVID-19 confirmed cases in US counties.
                 > 
                 > The **red** areas are the counties that the trend is **positive** meaning the number of the COVID-19 confirmed cases are increasing compared to the previous week.
                 >
                 > The **blue** areas are the counties that the trend is **negative** meaning the number of the COVID-19 confirmed cases are decreasing compared to the previous week.
                 >
                 ''' , style={'fontSize': 14}),    
    html.Div([
            html.Div([
                    html.H6('COVID-19 Confirmed and Death cases in US Counties', 
                            style = { 'fontSize': 18, 'vertical-align': 'middle', 'text-align': 'center', 'margin-top':'1em'})
                    ]),
            dcc.Graph(
                id = 'us-graph',
                figure = fig_us,
            )
     ],  style={"width" : "95%", 'margin': '0 auto'}),
    #html.Hr(),
    
    #html.Div(children=['This website is designed and maintained by Omid Badr ',html.A('LinkedIn', href='https://www.linkedin.com/in/omidbadr/', style={'color':'red', 'fontSize': 14})\
    #,' and Amir Badr ',html.A('LinkedIn', href='https://www.linkedin.com/in/amirbadr9/', style={'color':'red', 'fontSize': 14}),' for educational and informative purposes.' ]
    #,style={'color':'black', 'fontSize': 16}),
    ]),        
   ]) 
])

@app.callback(
    Output(component_id='timeseries-canada-graph', component_property='figure'),
    [Input(component_id='province_selection', component_property='value'), 
     Input(component_id='metrics_selection', component_property='value'),
     Input(component_id='daily_selection', component_property='value')]
)
def province_metric_timeseries(province, metric, daily):
    fig = go.Figure()
    if daily == 'Total':
        if metric == 'Number of Confirmed Cases':
            fig.add_trace(go.Bar(
                            x = Confirmed_Canada['Date'],
                            y = Confirmed_Canada[province],
                            name = province,
                            ))
        elif metric == 'Number of Deaths':
            fig.add_trace(go.Bar(
                            x = Death_Canada['Date'],
                            y = Death_Canada[province],
                            name = province,
                            ))
        
        elif metric == 'Number of Recovered Cases':
            fig.add_trace(go.Bar(
                            x = Recovered_Canada['Date'],
                            y = Recovered_Canada[province],
                            name = province,
                            ))
        else:
            fig.add_trace(go.Bar(
                            x = Testing_Canada['Date'],
                            y = Testing_Canada[province],
                            name = province,
                            ))

    elif daily == 'Daily':
        if metric == 'Number of Confirmed Cases':
            fig.add_trace(go.Bar(
                            x = Daily_Confirmed_Canada['Date'],
                            y = Daily_Confirmed_Canada[province],
                            name = province,
                            ))
        elif metric == 'Number of Deaths':
            fig.add_trace(go.Bar(
                            x = Daily_Death_Canada['Date'],
                            y = Daily_Death_Canada[province],
                            name = province,
                            ))
        
        elif metric == 'Number of Recovered Cases':
            fig.add_trace(go.Bar(
                            x = Daily_Recovered_Canada['Date'],
                            y = Daily_Recovered_Canada[province],
                            name = province,
                            ))
        else:
            fig.add_trace(go.Bar(
                            x = Daily_Testing_Canada['Date'],
                            y = Daily_Testing_Canada[province],
                            name = province,
                            ))
    fig.update_layout(dict(
            title = go.layout.Title(text = 'COVID-19 '+daily+'  '+metric+' in '+province, x = 0.5, font = {'size':16, 'color':'black'}),
            xaxis = go.layout.XAxis(tickfont = dict(family = 'Rockwell', size = 16), title = go.layout.xaxis.Title(text = ''), 
                                    showgrid = False, tickmode = 'linear', tick0 = Confirmed_Canada.loc[0,'Date'], 
                                    dtick =  7*86400000.0),
            yaxis = dict(showgrid = True, showticklabels = True, tickfont = dict(family = 'Rockwell', size = 16),
                        gridcolor = 'rgb(159, 197, 232)', zerolinecolor = 'rgb(74, 134, 232)'),
            font = dict(size = 16, family = 'Arial')  ,     
            legend = dict(x = 1.1, y = 1.1),
            #height = 600,
            #width = '90%',
            xaxis_tickformat = '%d %b',
            plot_bgcolor = '#FFFFFF',
            paper_bgcolor = '#FFFFFF'
            
            
            ))
    return (fig)

@app.callback(
    Output(component_id='canada-cities-graph', component_property='figure'),
    [Input(component_id='province_selection2', component_property='value')]
)
def province_region_map(province):
    fig = Canada_provinces_map(Canada_cities_report, canada_regions_json,province)
    return (fig)

if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_hot_reload = False, dev_tools_ui = False, 
                   processes = 1, dev_tools_prune_errors = False, dev_tools_hot_reload_interval = 20)