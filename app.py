import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import calendar
import plotly.graph_objects as go
# from jupyter_dash import JupyterDash
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np                
import dash_table
degree_sign = u"\N{DEGREE SIGN}"


mapbox_access_token = 'pk.eyJ1IjoidXJ2aTk3IiwiYSI6ImNrbmUzMG1hcDBhNjIydnFxdXZjbzNhZGoifQ.zKEd5FBU5ajxGXdLYe0erw'
#Reading the csv file
data = pd.read_csv("withmonth.csv")
data['Date'] =  pd.to_datetime(data['Date'])

df = data.copy()
actvy_options = data["Activity"].unique()
day_options = data["Day"].unique()
df['text'] = "Location: " + df['Location'] + ", " + df['Province'] + " \nActivity: " + df["Activity"] + "," +" \n Weather: " + df["Temp"].astype(str) + " "+ degree_sign + "C"

day_df = data.groupby(["Day"],as_index=False).sum().sort_values(by="Day")
year_df = data.groupby(["Year"],as_index=False).sum()
month_df = data.groupby(["Month"],as_index=False).sum()

bar_df = data.groupby(["Activity"],as_index=False).sum()

day_act_df = data.groupby(["Activity","Day"],as_index=False).sum()
yr_act_df = data.groupby(["Activity","Year"],as_index=False).sum()
month_act_df = data.groupby(["Activity","Month"],as_index=False).sum()


# the style arguments for the sidebar.
SIDEBAR_STYLE = {
    'position': 'fixed',
    'top': 0,
    'left': 0,
    'bottom': 0,
    'width': '20%',
    'padding': '20px 10px',
    'background-color': '#f8f9fa'
}

# the style arguments for the main content page.
CONTENT_STYLE = {
    'margin-left': '20%',
    'margin-right': '5%',
    'padding': '20px 10p'
}

TEXT_STYLE = {
    'textAlign': 'center',
    'color': '#191970'
}


controls = dbc.FormGroup(
    [
        html.P('Activities', style={
            'textAlign': 'center'
        }),
        
        dcc.Checklist(id='the_activity',
                    options=[{'label':str(b),'value':b} for b in sorted(df['Activity'].unique())],
                    value=[b for b in sorted(df['Activity'].unique())], labelStyle = {'display': 'block', 'cursor': 'pointer', 'margin-left':'20px'}),
        
        html.Br(),
        html.P('Year Slider', style={
            'textAlign': 'center'
        }),
        dcc.Slider(
        id="the_year",
        min = 2009,
        max =2020,
        value = 2014,
        marks = {
            2009: '2009',
            2010: '2010',
            2011: '2011',
            2012: '2012',
            2013: '2013',
            2014: '2014',
            2015: '2015',
            2016: '2016',
            2017: '2017',
            2018: '2018',
            2019: '2019',
            2020: '2020',}  
        )
    ]
)

sidebar = html.Div(
    [
        html.H2('Parameters', style=TEXT_STYLE),
        html.Hr(),
        controls
    ],
    style=SIDEBAR_STYLE,
)



content_second_row = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(id='the_map', config = {"displayModeBar": False}), md=11
        )
    ]
)

content_third_row = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(id='incidents-bargraph', config = {"displayModeBar": False}), width=5,
        ),
        dbc.Col([
            dcc.Dropdown(
                id="DayorYear",
                options=[{'label': 'Day', 'value': 'Day'}, {'label': 'Year','value': 'Year'}],
                value='Year'),
            dcc.Graph(id='incidents-bargraph-days', config = {"displayModeBar": False})
        ], width = 5)
    ]
)


fig_wea = go.Figure(data=go.Scatter(x=data["Activity"], y=data["Temp"], mode='markers',marker_color = "#118ab2"))

fig_wea.update_layout(title= {"text": 'Weather during  incidents for each activity',"xanchor":"center", "x": 0.5, "y": 0.9},
                   xaxis_title='Activity',
                   yaxis_title='Temperature in Celius')

fig_date = go.Figure()

fig_date.add_trace(go.Scatter(x=data["Date"], y=data["Fatality"], name="Fatality",
                            line=dict(color='#ef476f', width=4)))
fig_date.add_trace(go.Scatter(x=data["Date"], y=data["Injury"], name ="Injury",
                    line=dict(color='#073b4c', width=4)))
fig_date.update_layout(title= {"text": 'ALL counts of Fatalities and Injury over the years (Hover for Individual Date)',"xanchor":"center", "x": 0.5, "y": 0.9},
                   xaxis_title='Dates',
                   yaxis_title='Count',)
fig_date.update_xaxes(dtick = "M5", tickformat="%d %b %Y")






content_fourth_row = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(id='incidents-line-graph', config = {"displayModeBar": False}), md=6
        ),
        dbc.Col(
            dcc.Graph(id="scatter-plot",figure = fig_wea, config = {"displayModeBar": False}), md=6
        ),
    ]
)


content_fifth_row = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(id='incidents-dateline-graph', figure = fig_date, config = {"displayModeBar": False}), md=12
        )
    ]
)

content = html.Div(
    [
        html.H2('Incidents Due To Avalanche', style=TEXT_STYLE),
        html.Hr(),

        content_second_row,
        html.Hr(),


        # dcc.Dropdown(
        #         id="Activity",
        #         options=[{'label': 'All Activities', 'value': 'All Activities'}, 
        #         {'label': 'Backcountry Skiing','value': 'Backcountry Skiing'},
        #         {'label': 'Heliskiing','value': 'Heliskiing'},
        #         {'label': 'Snowboarding','value': 'Snowboarding'},
        #         {'label': 'Snowmobiling','value': 'Snowmobiling'},
        #         {'label': 'Snow Biking','value': 'Snow Biking'},
        #         {'label': 'Ski touring	','value': 'Ski touring	'},
        #         {'label': 'Mechanized Skiing','value': 'Mechanized Skiing'},
        #         {'label': 'Skiing','value': 'Skiing'},
        #         {'label': 'Lift Skiing Closed','value': 'Lift Skiing Closed'},
        #         {'label': 'Snowshoeing & Hiking','value': 'Snowshoeing & Hiking'},
        #         {'label': 'Snowshoeing','value': 'Snowshoeing'},
        #         {'label': 'Out-of-bounds Skiing','value': 'Out-of-bounds Skiing'},
        #         {'label': 'Ice Climbing','value': 'Ice Climbing'}],
        #         value='All Activities', style={'width': '49%', 'display': 'inline-block'}),

        # dcc.Dropdown(
        #         id="DayorYear",
        #         options=[{'label': 'Day', 'value': 'Day'}, {'label': 'Year','value': 'Year'}],
        #         value='Day',style={'width': '49%', 'float': 'right', 'display': 'inline-block'}),
        content_third_row,

        html.Hr(),

        html.H3('Compare Between Two Actvitites'),

        html.P('Activity1', style={
            'textAlign': 'left'}),
            dcc.Dropdown(
                id="Activity1",
                options=[{"label": x, "value": x} for x in actvy_options],
                value='All Activities',style={'width': '49%', 'display': 'inline-block'}),
        
        html.P('Activity2', style={
            'textAlign': 'left'}),
            dcc.Dropdown(
                id="Activity2",
                options=[{"label": x, "value": x} for x in actvy_options],
                value='All Activities',style={'width': '49%', 'display': 'inline-block'}),
            
            dcc.RadioItems(
                id= "TimelineOptions",
                options=[
                    {'label': 'Year', 'value': 'Year'},
                    {'label': 'Month', 'value': 'Month'},
                    {'label': 'Day', 'value': 'Day'}
                ],value='Year'),
            
            dcc.RadioItems(
                id= "IncidentOptions",
                options=[
                    {'label': 'Fatality', 'value': 'Fatality'},
                    {'label': 'Injury', 'value': 'Injury'}
                ],value='Fatality'),
            
        content_fourth_row,
        html.Hr(),
        content_fifth_row
    ],
    style=CONTENT_STYLE
)

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
app.layout = html.Div([sidebar, content])




@app.callback(
    Output('the_map','figure'),
    [Input('the_year','value'),
    Input('the_activity', 'value')]
)
def update_figure(year_chosen,activity_chosen):
    # if click_data is None:
    dff=df[(df['Year']==year_chosen) & df['Activity'].isin(activity_chosen)]
    dff.head()
    fig = px.scatter_mapbox(dff, lat="Latitude", lon="Longitude",     color="Involvement", size="Fatality",
                  color_continuous_scale=px.colors.sequential.Sunset, size_max=10, zoom=5, 
                        mapbox_style="carto-positron", text= dff["text"], center = dict(lat = 50.25789, lon = -123.228))
    # print(f"clicked data: {click_data}")
    # temp_lat = click_data["points"][0]["lat"]
    # temp_lon = click_data["points"][0]["lon"]
    # temp_df  = data[bar_df['Activity'] == Activity]

    return (fig)



@app.callback(
    dash.dependencies.Output('incidents-bargraph', 'figure'),
    [dash.dependencies.Input('the_map', 'clickData')])
def update_bar_graph(clickData):
    df_plot_bar = bar_df.copy()

    trace1_bar = go.Bar(x=df_plot_bar["Activity"], y=df_plot_bar['Fatality'], name='Fatality', marker_color = "#ef476f")
    trace2_bar = go.Bar(x=df_plot_bar["Activity"], y=df_plot_bar['Injury'], name='Injury', marker_color = "#073b4c")

    if clickData is not None:
        # if Activity == "All Activities":
        #     df_plot_bar = bar_df.copy()
        #     # print("inside all act")
        # else:
        #     df_plot_bar = bar_df[bar_df['Activity'] == Activity]
        #     # print("inside specific act")
        print(f"cliced date: {clickData}")
        temp_lat = clickData["points"][0]["lat"]
        temp_lon = clickData["points"][0]["lon"]
        temp_df = data[(data['Latitude']==temp_lat) & (data['Longitude']==temp_lon)]
        trace1_bar = go.Bar(x=temp_df["Activity"], y=temp_df['Fatality'], name='Fatality', marker_color = "#ef476f")
        trace2_bar = go.Bar(x=temp_df["Activity"], y=temp_df['Injury'], name='Injury', marker_color = "#073b4c")
        for act in temp_df["Activity"]:
                Activity = act
        return {
        'data': [trace1_bar, trace2_bar],
        'layout':
        go.Layout(
            title='Fatalities and Injuries for {}'.format(Activity),
            barmode='group',clickmode="event+select", yaxis_title="Fatalities and Injuries Count")
    }

        # if Activity == "All Activities":
        #     df_plot_bar = bar_df.copy()
        # else:
        #     df_plot_bar = bar_df[bar_df['Activity'] == Activity]

        # trace1_bar = go.Bar(x=df_plot_bar["Activity"], y=df_plot_bar['Fatality'], name='Fatality')
        # trace2_bar = go.Bar(x=df_plot_bar["Activity"], y=df_plot_bar['Injury'], name='Injury')
        # if flag == 0:
        #     if Activity == "All Activities":
        #         df_plot_bar = bar_df.copy()
        #     else:
        #         df_plot_bar = bar_df[bar_df['Activity'] == Activity]

        #     trace1_bar = go.Bar(x=df_plot_bar["Activity"], y=df_plot_bar['Fatality'], name='Fatality')
        #     trace2_bar = go.Bar(x=df_plot_bar["Activity"], y=df_plot_bar['Injury'], name='Injury')


        # print("not none")
    return {
        'data': [trace1_bar, trace2_bar],
        'layout':
        go.Layout(
            title='Fatalities and Injuries for All Activities',xaxis=dict(tickangle = 30),
            barmode='group',clickmode="event+select", yaxis_title="Fatalities and Injuries Count")
    }



@app.callback(
    dash.dependencies.Output('incidents-bargraph-days', 'figure'),
    [dash.dependencies.Input('DayorYear', 'value'),
    dash.dependencies.Input('incidents-bargraph', 'hoverData'),
    dash.dependencies.Input('the_map', 'clickData')])
def update_date_graph(DayorYear,hoverData,clickDataMap):
    # if clickDataMap is None:
        # print("inside none")
        # if Activity == "All Activities" and DayorYear == "Day":
        #     df_plot_DY = day_df.copy()
        #     trace1_DY = go.Bar(x=df_plot_DY["Day"], y=df_plot_DY['Fatality'], name='Fatality', marker_color = "#ef476f")
        #     trace2_DY = go.Bar(x=df_plot_DY["Day"], y=df_plot_DY['Injury'], name='Injury', marker_color = "#073b4c")

        # elif Activity == "All Activities" and DayorYear == "Year":
        #     df_plot_DY = year_df.copy()
        #     trace1_DY = go.Bar(x=df_plot_DY["Year"], y=df_plot_DY['Fatality'], name='Fatality', marker_color = "#ef476f")
        #     trace2_DY = go.Bar(x=df_plot_DY["Year"], y=df_plot_DY['Injury'], name='Injury', marker_color = "#073b4c")


        # if Activity != "All Activities" and DayorYear == "Year":
        #     df_plot_DY = yr_act_df[yr_act_df['Activity'] == Activity]
        #     trace1_DY = go.Bar(x=df_plot_DY["Year"], y=df_plot_DY['Fatality'], name='Fatality', marker_color = "#ef476f")
        #     trace2_DY = go.Bar(x=df_plot_DY["Year"], y=df_plot_DY['Injury'], name='Injury', marker_color = "#073b4c")

        # elif Activity != "All Activities" and DayorYear == "Day":
        #     df_plot_DY = day_act_df[day_act_df['Activity'] == Activity]
        #     trace1_DY = go.Bar(x=df_plot_DY["Day"], y=df_plot_DY['Fatality'], name='Fatality', marker_color = "#ef476f")
        #     trace2_DY = go.Bar(x=df_plot_DY["Day"], y=df_plot_DY['Injury'], name='Injury', marker_color = "#073b4c")
    if DayorYear == "Day":
        df_plot_DY = day_df.copy()
        trace1_DY = go.Bar(x=df_plot_DY["Day"], y=df_plot_DY['Fatality'], name='Fatality', marker_color = "#ef476f")
        trace2_DY = go.Bar(x=df_plot_DY["Day"], y=df_plot_DY['Injury'], name='Injury', marker_color = "#073b4c")

    elif DayorYear == "Year":
        df_plot_DY = year_df.copy()
        trace1_DY = go.Bar(x=df_plot_DY["Year"], y=df_plot_DY['Fatality'], name='Fatality', marker_color = "#ef476f")
        trace2_DY = go.Bar(x=df_plot_DY["Year"], y=df_plot_DY['Injury'], name='Injury', marker_color = "#073b4c")
    
    if hoverData is not None:
        # print(f'Hover: {hoverData}')
        Activity = hoverData["points"][0]["x"]
        if DayorYear == "Day":
            df_plot_DY = day_act_df[day_act_df['Activity'] == Activity]
            trace1_DY = go.Bar(x=df_plot_DY["Day"], y=df_plot_DY['Fatality'], name='Fatality', marker_color = "#ef476f")
            trace2_DY = go.Bar(x=df_plot_DY["Day"], y=df_plot_DY['Injury'], name='Injury', marker_color = "#073b4c")

        elif DayorYear == "Year":
            df_plot_DY = yr_act_df[yr_act_df['Activity'] == Activity]
            trace1_DY = go.Bar(x=df_plot_DY["Year"], y=df_plot_DY['Fatality'], name='Fatality', marker_color = "#ef476f")
            trace2_DY = go.Bar(x=df_plot_DY["Year"], y=df_plot_DY['Injury'], name='Injury', marker_color = "#073b4c")
    # if clickData is None:
    #     if DayorYear == "Day":
    #         df_plot_DY = day_df.copy()
    #         trace1_DY = go.Bar(x=df_plot_DY["Day"], y=df_plot_DY['Fatality'], name='Fatality')
    #         trace2_DY = go.Bar(x=df_plot_DY["Day"], y=df_plot_DY['Injury'], name='Injury')

    #     elif DayorYear == "Year":
    #         df_plot_DY = year_df.copy()
    #         trace1_DY = go.Bar(x=df_plot_DY["Year"], y=df_plot_DY['Fatality'], name='Fatality')
    #         trace2_DY = go.Bar(x=df_plot_DY["Year"], y=df_plot_DY['Injury'], name='Injury')
    
    if clickDataMap is not None:
        # print(clickData["points"][0]["x"])
        temp_lat = clickDataMap["points"][0]["lat"]
        temp_lon = clickDataMap["points"][0]["lon"]
        temp_df = data[(data['Latitude']==temp_lat) & (data['Longitude']==temp_lon)]
        
        # if clickData is not None:
        #     Activity = clickData["points"][0]["x"]
        # else:
        for act in temp_df["Activity"]:
            Activity = act
        if DayorYear == "Day":
            df_plot_DY = day_act_df[day_act_df['Activity'] == Activity]
            trace1_DY = go.Bar(x=df_plot_DY["Day"], y=df_plot_DY['Fatality'], name='Fatality', marker_color = "#ef476f")
            trace2_DY = go.Bar(x=df_plot_DY["Day"], y=df_plot_DY['Injury'], name='Injury', marker_color = "#073b4c")

        elif DayorYear == "Year":
            df_plot_DY = yr_act_df[yr_act_df['Activity'] == Activity]
            trace1_DY = go.Bar(x=df_plot_DY["Year"], y=df_plot_DY['Fatality'], name='Fatality', marker_color = "#ef476f")
            trace2_DY = go.Bar(x=df_plot_DY["Year"], y=df_plot_DY['Injury'], name='Injury', marker_color = "#073b4c")
        
# individual activty variable for checkbox and click ... see if it works
        # if Activity == "All Activities" and DayorYear == "Day":
        #     df_plot_DY = day_df.copy()
        #     trace1_DY = go.Bar(x=df_plot_DY["Day"], y=df_plot_DY['Fatality'], name='Fatality')
        #     trace2_DY = go.Bar(x=df_plot_DY["Day"], y=df_plot_DY['Injury'], name='Injury')

        # elif Activity == "All Activities" and DayorYear == "Year":
        #     df_plot_DY = year_df.copy()
        #     trace1_DY = go.Bar(x=df_plot_DY["Year"], y=df_plot_DY['Fatality'], name='Fatality')
        #     trace2_DY = go.Bar(x=df_plot_DY["Year"], y=df_plot_DY['Injury'], name='Injury')


        # if Activity != "All Activities" and DayorYear == "Year":
        #     df_plot_DY = yr_act_df[yr_act_df['Activity'] == Activity]
        #     trace1_DY = go.Bar(x=df_plot_DY["Year"], y=df_plot_DY['Fatality'], name='Fatality')
        #     trace2_DY = go.Bar(x=df_plot_DY["Year"], y=df_plot_DY['Injury'], name='Injury')

        # elif Activity != "All Activities" and DayorYear == "Day":
        #     df_plot_DY = day_act_df[day_act_df['Activity'] == Activity]
        #     trace1_DY = go.Bar(x=df_plot_DY["Day"], y=df_plot_DY['Fatality'], name='Fatality')
        #     trace2_DY = go.Bar(x=df_plot_DY["Day"], y=df_plot_DY['Injury'], name='Injury')
        # ctx = dash.callback_context

        # if not ctx.triggered:
        #     button_id = 'No clicks yet'
        # else:
        #     button_id = ctx.triggered
        #     print("value:", button_id)
        # clickData = None
        # print(clickData)
    
    return {
        'data': [trace1_DY, trace2_DY],
        'layout':
        go.Layout(
            title='Fatalities and Injuries for each day or year',xaxis={"dtick": 1},
            barmode='group', yaxis_title="Fatalities and Injuries Count", xaxis_title = DayorYear)
    }


@app.callback(
    dash.dependencies.Output('incidents-line-graph', 'figure'),
    [dash.dependencies.Input('Activity1', 'value'),
    dash.dependencies.Input('Activity2', 'value'),
    dash.dependencies.Input('IncidentOptions', 'value'),
    dash.dependencies.Input('TimelineOptions', 'value')])
def update_comparison_graph(Activity1, Activity2, IncidentOptions, TimelineOptions):

    fig_compare = go.Figure()
        # df_plot_compare = month_act_df.copy()
    if IncidentOptions == "Fatality" and TimelineOptions == "Year":
        df_plot_compare_act1 = yr_act_df[yr_act_df['Activity'] == Activity1]
        df_plot_compare_act2 = yr_act_df[yr_act_df['Activity'] == Activity2]
        fig_compare.add_trace(go.Scatter(x=df_plot_compare_act1["Year"], y=df_plot_compare_act1["Fatality"], name=Activity1,
                            line=dict(color='#06d6a0', width=4)))
        fig_compare.add_trace(go.Scatter(x=df_plot_compare_act2["Year"], y=df_plot_compare_act2["Fatality"], name =Activity2,
                            line=dict(color='#E85D04', width=4)))
        fig_compare.update_layout(title={"text":'Fatalities for each Year',"xanchor":"center", "x": 0.5, "y": 0.9},
                   xaxis_title='Year',
                   yaxis_title='Fatalities Count')
    
    elif IncidentOptions == "Fatality" and TimelineOptions == "Month":
        df_plot_compare_act1 = month_act_df[month_act_df['Activity'] == Activity1]
        df_plot_compare_act2 = month_act_df[month_act_df['Activity'] == Activity2]
        fig_compare.add_trace(go.Scatter(x=df_plot_compare_act1["Month"], y=df_plot_compare_act1["Fatality"], name=Activity1,
                            line=dict(color='#06d6a0', width=4)))
        fig_compare.add_trace(go.Scatter(x=df_plot_compare_act2["Month"], y=df_plot_compare_act2["Fatality"], name =Activity2,
                            line=dict(color='#E85D04', width=4)))
        fig_compare.update_layout(title={"text": 'Fatalities for each Month',"xanchor":"center", "x": 0.5, "y": 0.9},
                   xaxis_title='Month',
                   xaxis_tickformat= "%B",
                   yaxis_title='Fatalities Count')
    
    elif IncidentOptions == "Fatality" and TimelineOptions == "Day":
        df_plot_compare_act1 = day_act_df[day_act_df['Activity'] == Activity1]
        df_plot_compare_act2 = day_act_df[day_act_df['Activity'] == Activity2]
        fig_compare.add_trace(go.Scatter(x=df_plot_compare_act1["Day"], y=df_plot_compare_act1["Fatality"], name=Activity1,
                            line=dict(color='#06d6a0', width=4)))
        fig_compare.add_trace(go.Scatter(x=df_plot_compare_act2["Day"], y=df_plot_compare_act2["Fatality"], name =Activity2,
                            line=dict(color='#E85D04', width=4)))
        fig_compare.update_layout(title={"text": 'Fatalities for each Day',"xanchor":"center", "x": 0.5, "y": 0.9},
                   xaxis_title='Day',
                   yaxis_title='Fatalities Count')


    
    elif IncidentOptions == "Injury" and TimelineOptions == "Year":
        df_plot_compare_act1 = yr_act_df[yr_act_df['Activity'] == Activity1]
        df_plot_compare_act2 = yr_act_df[yr_act_df['Activity'] == Activity2]
        fig_compare.add_trace(go.Scatter(x=df_plot_compare_act1["Year"], y=df_plot_compare_act1["Injury"], name=Activity1,
                            line=dict(color='#06d6a0', width=4)))
        fig_compare.add_trace(go.Scatter(x=df_plot_compare_act2["Year"], y=df_plot_compare_act2["Injury"], name =Activity2,
                            line=dict(color='#E85D04', width=4)))
        fig_compare.update_layout(title={"text":'Injuries for each Year',"xanchor":"center", "x": 0.5, "y": 0.9},
                   xaxis_title='Year',
                   yaxis_title='Injuries Count')
    
    elif IncidentOptions == "Injury" and TimelineOptions == "Month":
        df_plot_compare_act1 = month_act_df[month_act_df['Activity'] == Activity1]
        df_plot_compare_act2 = month_act_df[month_act_df['Activity'] == Activity2]
        fig_compare.add_trace(go.Scatter(x=df_plot_compare_act1["Month"], y=df_plot_compare_act1["Injury"], name=Activity1,
                            line=dict(color='#06d6a0', width=4)))
        fig_compare.add_trace(go.Scatter(x=df_plot_compare_act2["Month"], y=df_plot_compare_act2["Injury"], name =Activity2,
                            line=dict(color='#E85D04', width=4)))
        fig_compare.update_layout(title={"text":'Injuries for each Month',"xanchor":"center", "x": 0.5, "y": 0.9},
                   xaxis_title='Month',
                   yaxis_title='Injuries Count')
    
    elif IncidentOptions == "Injury" and TimelineOptions == "Day":
        df_plot_compare_act1 = day_act_df[day_act_df['Activity'] == Activity1]
        df_plot_compare_act2 = day_act_df[day_act_df['Activity'] == Activity2]
        fig_compare.add_trace(go.Scatter(x=df_plot_compare_act1["Day"], y=df_plot_compare_act1["Injury"], name=Activity1,
                            line=dict(color='#06d6a0', width=4)))
        fig_compare.add_trace(go.Scatter(x=df_plot_compare_act2["Day"], y=df_plot_compare_act2["Injury"], name =Activity2,
                            line=dict(color='#E85D04', width=4)))
        fig_compare.update_layout(title= {"text": 'Injuries for each Day',"xanchor":"center", "x": 0.5, "y": 0.9},
                   xaxis_title='Day',
                   yaxis_title='Injuries Count')
    return fig_compare
    # return {
    #     'data': [fig_compare],
        # # 'layout':
        # # go.Layout(
    #     #     title='Fatalities and Injuries for each month')
    # }






if __name__ == '__main__':
    app.run_server(debug=True)