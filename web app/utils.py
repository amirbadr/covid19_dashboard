# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 17:44:29 2020

@author: omidb
"""
def Canada_fig(Canada_map_table, canada_province_json):
    
    import plotly.graph_objects as go
    from datetime import datetime
    from pytz import timezone
    tz = timezone('EST')
    token = 'pk.eyJ1Ijoib21pZGJhZHIiLCJhIjoiY2s3eGVrM3JpMDExbDNtb3hxOWQwMWQ3bCJ9.ReYzh21GWttlycXTJ_mZJA'

    #crs = {'init': 'epsg:4326'}
    date_today = datetime.now(tz).strftime('%B %d, %Y')
    #Daily_report_Canada_shp2 = gpd.GeoDataFrame(Daily_report_Canada_shp, crs = crs, geometry='geometry')   
    fig = go.Choroplethmapbox(geojson = canada_province_json, featureidkey = "properties.NAME",
                                            locations = Canada_map_table['Province'], 
                                            z = Canada_map_table['Total Confirmed Cases'], 
                                            text = Canada_map_table['text'], # hover text
                                            hovertemplate = "<b>%{text}</b>"+"<extra></extra>",
                                            colorscale = "YlOrRd", autocolorscale=False,
                                            colorbar = dict(len = 0.75, thickness=15, ticklen=1, title = dict(font = dict(size = 1))),
                                            marker_line_width=0.1, marker_opacity=0.5,
                                            colorbar_title = 'Confirmed cases as of'+'<br>'+date_today, below=True,)
    layout =  go.Layout(mapbox_style="light",
                        #title_text='2011 US Agriculture Exports by State<br>(Hover for breakdown)',
                        mapbox_accesstoken=token,
                        mapbox_zoom=3.2, height = 600,
                        mapbox_center = {"lat": 52.493382, "lon": -92.962644},
                        margin={"r":0,"t":0,"l":0,"b":0})
    centers = go.Scattermapbox(lat= Canada_map_table['Lat'].tolist(),
                                lon= Canada_map_table['Long'].tolist(),
                                marker = {'color': 'white', 'opacity': 0, 'size': 6},
                                #textfont = {'color': 'black','size': 1},
                                mode= 'text',
                                showlegend= False,
                                hoverinfo='skip',
                                text=Canada_map_table['text'].tolist())
    
    data = [fig, centers]
    fig2 = go.Figure(layout=layout, data=data)
    return(fig2)
    
    
def confirmed_graph(cases_timeseries_table):
    import plotly.graph_objects as go
    ### Plotly 
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
                    x = cases_timeseries_table['Date'],
                    y = cases_timeseries_table['Ontario'],
                    name = 'Ontario',
                    #mode = 'lines+markers', marker = dict(size = 2), line = dict(width = 2),
                    #line_color='deepskyblue',
                    #opacity = 0.8
                    ))
    
    fig.update_layout(dict(
        title = go.layout.Title(text = 'Confirmed Cases in Canada Provinces', x = 0.5, font = {'size':16, 'color':'black'}),
        xaxis = go.layout.XAxis(tickfont = dict(family = 'Rockwell', size = 16), title = go.layout.xaxis.Title(text = ''), 
                                showgrid = False, tickmode = 'linear', tick0 = cases_timeseries_table.loc[0,'Date'], 
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
    
    return(fig)
    
def Canada_provinces_map(Canada_cities_report, canada_regions_json, Province):
    from datetime import datetime
    from pytz import timezone
    tz = timezone('EST')
    import plotly.graph_objects as go
    token = 'pk.eyJ1Ijoib21pZGJhZHIiLCJhIjoiY2s3eGVrM3JpMDExbDNtb3hxOWQwMWQ3bCJ9.ReYzh21GWttlycXTJ_mZJA'
     
    date_today = datetime.now(tz).strftime('%B %d, %Y')
    Canada_cities_report['text'] = Canada_cities_report.apply(lambda x : x['region'] + '  :  ' + str(x['num cases']), axis = 1)
    if Province != 'Canada':
        Canada_cities_report = Canada_cities_report.loc[Canada_cities_report['Province'] == Province].reset_index(drop = True)
    
    if Province == 'Canada':
        lat = 52.493382; lon = -92.962644; zoom = 3
    elif Province == 'Ontario':
        lat = 43.651070; lon = -79.347015; zoom = 7
    elif Province == 'British Columbia':
        lat = 49.246292; lon = -123.116226; zoom = 5
    elif Province == 'Alberta':
        lat = 52.268112; lon = -113.811241; zoom = 6
    elif Province == 'Quebec':
        lat = 45.508888; lon = -73.561668; zoom = 7
    elif Province == 'Manitoba':
        lat = 49.895077; lon = -97.138451; zoom = 7
    elif Province == 'Saskatchewan':
        lat = 51.262292 ; lon = -105.989011; zoom = 6
    elif Province == 'New Brunswick':
        lat = 46.054448 ; lon = -65.538143; zoom = 6
    elif Province == 'Newfoundland and Labrador':
        lat = 47.560539 ; lon = -52.712830; zoom = 4
    elif Province == 'Montreal':
        lat = 45.508888; lon = -73.561668; zoom = 10
    elif Province == 'Nova Scotia':
        lat = 44.651070; lon = -63.582687; zoom = 6
        
    
    fig = go.Choroplethmapbox(geojson = canada_regions_json, featureidkey = "properties.region",
                                    locations = Canada_cities_report['region'], 
                                    z = Canada_cities_report['num cases'], 
                                    text = Canada_cities_report['text'], # hover text
                                    hovertemplate = "<b>%{text}</b>"+"<extra></extra>",
                                    colorscale = "YlOrRd", autocolorscale=False,
                                    colorbar = dict(len = 0.75, thickness=15, ticklen=1, title = dict(font = dict(size = 1))),
                                    marker_line_width=0.01, marker_opacity=0.6,
                                    colorbar_title = 'Confirmed cases as of'+'<br>'+date_today
                                   )
    layout =  go.Layout(mapbox_style="light",
                        #title_text='2011 US Agriculture Exports by State<br>(Hover for breakdown)',
                        mapbox_accesstoken=token,
                        mapbox_zoom=zoom, 
                        mapbox_center = {"lat": lat, "lon": lon},
                        margin={"r":0,"t":0,"l":0,"b":0})
    
    fig2 = go.Figure(layout=layout, data=fig)
    return(fig2)
    
def US_map(Trend_df, us_county_json):
    #import plotly.express as px
    import plotly.graph_objects as go
    token = 'pk.eyJ1Ijoib21pZGJhZHIiLCJhIjoiY2s3eGVrM3JpMDExbDNtb3hxOWQwMWQ3bCJ9.ReYzh21GWttlycXTJ_mZJA'

    #adjusted_color_scales = px.colors.sequential.YlOrRd
    #data_scale = [int(i)/US_Confirmed_Death['Confirm'].max() for i in US_Confirmed_Death['Confirm'].quantile([0, .8, .9, .95, .99, .995, .999, .9995, 1]).tolist()]
    #colorscale = [[i,j] for i,j in zip(data_scale, adjusted_color_scales)]
    
    fig = go.Choroplethmapbox(geojson = us_county_json, featureidkey = "properties.GEOID",
                                locations = Trend_df['countyFIPS'], 
                                z = Trend_df['Weekly_dif%'],
                                zmid = 0, zmax = 100, zmin = -100,
                                text = Trend_df['Weekly_dif%'], # hover text
                                customdata = list(zip((Trend_df['County Name'] +', '+Trend_df['State']), Trend_df['Last_7_days'], Trend_df['Last_14_7_days'], Trend_df['Total Cases'], Trend_df['Death'])),
                                hovertemplate =
                                    '<b>County</b>: %{customdata[0]}'+
                                    '<br><b>Trend%</b>: %{z:,}'+
                                    '<br><b>Avg Confirmed Cases in the last 7 days</b>: %{customdata[1]:,}'+
                                    '<br><b>Avg Confirmed Cases in the last 14-7 days</b>: %{customdata[2]:,}'+
                                    '<br><b>Total Confirmed Cases</b>: %{customdata[3]:,}'+
                                    '<br><b>Total Deaths Cases</b>: %{customdata[4]:,}'+
                                    "<extra></extra>",
                                colorscale = 'RdBu', autocolorscale=False, showscale = True, reversescale = True,
                                colorbar = dict(len = 0.75, title = 'Weekly Trend', 
                                               tickvals = [-100, -75, -50, -25, 0, 25, 50, 75, 100],
                                               ticktext = ['<-100%', '-75%', '-50%', '-25%', '0%', '25%', '50%', '75%', '>100%']) ,
                                marker_line_width=0.1, marker_opacity=0.7,  
                               )
    layout =  go.Layout(mapbox_style="open-street-map",
                        #title_text='2011 US Agriculture Exports by State<br>(Hover for breakdown)',
                        mapbox_accesstoken=token,
                        mapbox_zoom=3.7, height = 600,
                        mapbox_center = {"lat": 38.000438, "lon": -98.572742},
                        hoverlabel = dict(bgcolor="white", font_size=14, font_family="Rockwell"),
                        margin={"r":0,"t":0,"l":0,"b":0})
    
    fig2 = go.Figure(layout=layout, data=fig)
    return(fig2)
    
def Canada_trend_map(Trend_df, canada_trend_json):
    import plotly.graph_objects as go
    token = 'pk.eyJ1Ijoib21pZGJhZHIiLCJhIjoiY2s3eGVrM3JpMDExbDNtb3hxOWQwMWQ3bCJ9.ReYzh21GWttlycXTJ_mZJA'
 
    fig = go.Choroplethmapbox(geojson = canada_trend_json, featureidkey = "properties.region",
                                    locations = Trend_df['Locations EN'], 
                                    z = Trend_df['Weekly_dif%'],
                                    zmid = 0, zmax = 50, zmin = -20,
                                    text = Trend_df['Weekly_dif%'], # hover text
                                    customdata = list(zip(Trend_df['Locations EN'], Trend_df['Last_7_days'], Trend_df['Last_14_7_days'], Trend_df['Total Cases'])),
                                    hovertemplate =
                                        '<b>Region</b>: %{customdata[0]}'+
                                        '<br><b>Trend%</b>: %{z:,}'+
                                        '<br><b>Avg Confirmed Cases in the last 7 days</b>: %{customdata[1]:,}'+
                                        '<br><b>Avg Confirmed Cases in the last 14-7 days</b>: %{customdata[2]:,}'+
                                        '<br><b>Total Confirmed Cases</b>: %{customdata[3]:,}'+
                                        "<extra></extra>",
                                    colorscale = 'RdYlBu', autocolorscale=False, showscale = True, reversescale = True,
                                    colorbar = dict(len = 0.75, title = 'Weekly Trend', 
                                                   tickvals = [-20, -10, 0, 10, 20, 30, 40, 50],
                                                   ticktext = ['<-20%', '-10%', '0%', '10%', '20%', '30%','40%','>50%']) ,
                                    marker_line_width=0.1, marker_opacity=0.5,  
                                   )
    layout =  go.Layout(mapbox_style="light",
                        #title_text='2011 US Agriculture Exports by State<br>(Hover for breakdown)',
                        mapbox_accesstoken=token,
                        mapbox_zoom=3.2, height = 600,
                        mapbox_center = {"lat": 52.493382, "lon": -92.962644},
                        hoverlabel = dict(bgcolor="white", font_size=14, font_family="Rockwell"),
                        margin={"r":0,"t":0,"l":0,"b":0})

    fig2 = go.Figure(layout=layout, data=fig)
    return(fig2)