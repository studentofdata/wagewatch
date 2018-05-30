import os
import dash
import dash_core_components as dcc
import plotly.graph_objs as go
import dash_html_components as html
import dash_table_experiments as dt
import pandas as pd

#Constants we will need to access data or external sources 
file_name_hotels = 'ww_hotels_30.csv'
file_name_jobs = 'ww_jobs_30.csv'

file_location_hotels = os.path.join(os.getcwd(), 'data','processed', file_name_hotels)
file_location_jobs = os.path.join(os.getcwd(), 'data','processed', file_name_jobs)

#Loading in raw data
j_data = pd.read_csv(file_location_jobs)
h_data = pd.read_csv(file_location_hotels)



#Backend helper functions for organizing data for output
def generate_mselect_data(mselect_data, column):
    og_dict = pd.Series(mselect_data[column].unique()).to_dict()
    payload = []
    for key in og_dict.keys():
        newdict = {}
        newdict['label'] = og_dict[key]
        newdict['value'] = og_dict[key]
        payload.append(newdict)
    return payload

#Html and front-end helper functions
def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )

app = dash.Dash()

app.layout = html.Div(children=[


html.Div([
    # Control Section
    html.Div([
    # Position Selector
        html.Div([
            html.Div('Select Position', className='three columns'),
            html.Div(dcc.Dropdown(id='position', 
                options=[{'label': i, 'value': i} for i in j_data['POSITION'].unique()]))
            ]),

        html.Div([
            html.Div('Select City Market', className='three columns'),
            html.Div(dcc.Dropdown(id='citymarket',
                options=[{'label':i, 'value':i} for i in j_data['CITYMARKET'].unique()]))
            ]),
    ]),
]),


html.Div([
    html.Div(id='position-selected'),
    html.Div(id='citymarket-selected'),
    ]),

    html.Div([
        html.Div(id='pay-line-graph'),

        html.Div(id='Diagnostic_table'),
        html.H4(children='Child Table'),
        dt.DataTable(
            rows=[{}], #Initialize rows
            row_selectable=True,
            filterable=True,
            sortable=True,
            selected_row_indices=[],
            id='diag-table')
            ]),

    html.Div(id='Table'),
    html.H4(children='Table of Data'),
    dt.DataTable(
        rows=[{}], #Initialize rows
        row_selectable=True,
        filterable=True,
        sortable=True,
        selected_row_indices=[],
        id='datatable')
])



@app.callback(
    dash.dependencies.Output('datatable','rows'),
    [dash.dependencies.Input('citymarket','value')])
def update_position(citymarket):
    h_data_v2 = h_data[h_data['CITYMARKET'] == citymarket].sort_values(['POSITION','clusters'])
    return h_data_v2.to_dict('records')


@app.callback(
    dash.dependencies.Output('diag-table','rows'),
        [dash.dependencies.Input('position','value'),
         dash.dependencies.Input('citymarket','value')])
def update_graph(position, citymarket):
    #def dynamic data points for 
    j_data_v2 = j_data[j_data['POSITION'] == position]
    j_data_v2 = j_data_v2[j_data_v2['CITYMARKET'] == citymarket]
    
    data = []
    for cluster in j_data_v2['clusters']:
        temp_dict = {}
        j_data_v3 = j_data_v2[j_data_v2['clusters'] == cluster]
        values = ['min','25','50','75','max']
        temp_dict['x'] = values
        temp_dict['y'] =list(j_data_v3[values].values[0])
        temp_dict['name'] = "Tier: {}".format(cluster)
        temp_dict['type'] = ['Scatter']
        data.append(temp_dict)
    return data




@app.callback(
    dash.dependencies.Output('pay-line-graph','children'),
        [dash.dependencies.Input('position','value'),
         dash.dependencies.Input('citymarket','value')])
def update_graph(position, citymarket):
    #def dynamic data points for 
    j_data_v2 = j_data[j_data['POSITION'] == position]
    j_data_v2 = j_data_v2[j_data_v2['CITYMARKET'] == citymarket]
    j_data_v2 = j_data_v2[j_data_v2['clusters'] == 0]

    
    # data = []
    # for cluster in j_data_v2['clusters']:
    #     temp_dict = {}
    #     j_data_v3 = j_data_v2[j_data_v2['clusters'] == cluster]
    #     values = [0,25,50,75,100]
    #     temp_dict['x'] = [values]
    #     temp_dict['y'] =list(j_data_v3[["min","25","50","75","max"]].values[0])
    #     temp_dict['name'] = "Tier: {}".format(cluster)
    #     temp_dict['type'] = ['scatter']
    #     data.append(temp_dict)

    # data = [
    #     {
    #         'x': ['min','25','50','75','max'],
    #         'y': [10,25,30,45],
    #         'name': 'marker1',
    #         'type': ['scatter']

    #     },
    #     {
    #         'x': ['min','25','50','75','max'],
    #         'y': [15,20,40,32],
    #         'name': 'marker2',
    #         'type': ['scatter']
    #     }]


    trace1 = go.Scatter(
        x=[0,25,50,75,],
        y=j_data_v2[["min","25","50","75","max"]].values[0]
    )

    data = [trace1]
    layout = go.Layout(
            xaxis=dict(
            title='AXIS TITLE',
            titlefont=dict(
                family='Arial, sans-serif',
                size=18,
                color='lightgrey'
            ),
            showticklabels=True,
            tickangle=45,
            tickfont=dict(
                family='Old Standard TT, serif',
                size=14,
                color='black'
            ),
            exponentformat='e',
            showexponent='All'
        ),
        yaxis=dict(
            title='AXIS TITLE',
            titlefont=dict(
                family='Arial, sans-serif',
                size=18,
                color='lightgrey'
            ),
            showticklabels=True,
            tickangle=45,
            tickfont=dict(
                family='Old Standard TT, serif',
                size=14,
                color='black'
            ),
            exponentformat='e',
            showexponent='All'
        )
    )
    fig = go.Figure(data=data, layout=layout)




    return html.Div([
            dcc.Graph(
                id='pay-line-graph',
                figure=fig
                # figure={
                #     'data': data,
                #     'layout': {
                #         'margin': {
                #             'l': 30,
                #             'r': 0,
                #             'b': 30,
                #             't': 0
                #             },
                #         'legend': {'x': 0, 'y': 1}
                #         }
                #     }
                )
            ])



# @app.callback(
#     dash.dependencies.Output('position-selected','children'),
#     [dash.dependencies.Input('citymarket','value')])
# def update_position(citymarket):
#     citymarket=citymarket
#     return h_data[h_data['CITYMARKET'] == citymarket].to_dict('records')




if __name__ == '__main__':
    app.run_server(debug=True, port=8901)