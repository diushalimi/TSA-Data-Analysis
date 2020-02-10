import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import seaborn as sns
import plotly.graph_objs as go
import dash_table
from dash.dependencies import Input, Output, State

def generate_table(df,page_size=10):
    return dash_table.DataTable(
        id='dataTable',
        columns=[{'name':i,'id':i} for i in df.columns],
        data=df.to_dict('records'),
        page_action='native',
        page_current=0,
        page_size=page_size
    )
tips=sns.load_dataset('tips')
tsa=pd.read_csv('TSA.csv')
external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css']

app=dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout=html.Div(children=[
    html.H1('Ujian Modul 2'),
    html.Div(children='Claudius Devlin Halimi'),
    
    dcc.Tabs(children=[
        dcc.Tab(value='Tab1',label='DataFrame Table',children=[
                html.Div([
                html.P('Claim Site :'),
                dcc.Dropdown(value='None',
                             id='filter-claim-site',
                             options=[{'label':'Checkpoint','value':'Checkpoint'},
                                    {'label':'Checked Baggage','value':'Checked Baggage'},
                                    {'label':'Motor Vehicle','value':'Motor Vehicle'},
                                    {'label':'Bus Station','value':'Bus Station'},
                                    {'label':'Other','value':'Other'}])
                ], className='col-3'),
                html.Br(),
                html.Div([
                    html.P('Max Rows :'),
                    dcc.Input(id='filter-row',
                            type='number',
                            value=10)
                    ], className='row col-3'),
                html.Div(children=[
                    html.Button('Search',id='filter')
                    ], className='row col-4'),
                html.Div([id='div-table', 
                    children=[generate_table(tsa, page_size=10)
                ], className='col-4')

        dcc.Tab(value='Tab2',label='haha',children=[
            dcc.Graph(
                id='graph-scatter',
                figure={'data':[
                    go.Scatter(
                        x=tips[tips['day']==i]['tip'],
                        y=tips[tips['day']==i]['total_bill'],
                        mode='markers',
                        name='Day{}'.format(i)
                        ) for i in tips['day'].unique()
                    ],
                    'layout':go.Layout(
                        xaxis={'title':'Tip'},
                        yaxis={'title':'Total Bill'},
                        title='Tips Dash Scatter Visualization',
                        hovermode='closest'
                    )
                }
            )
    ],className='col-4'),

    dcc.Tab(value='Tab3',label='Data Frame Tips',children=[
        html.Div(children=[
            html.Div([
                html.P('Smoker'),
                dcc.Dropdown(value='None',
                             id='filter-smoker',
                             options=[{'label':'No','value':'No'},
                                    {'label':'Yes','value':'Yes'},
                                    {'label':'None','value':'None'}])
                ], className='col-3'),
            html.Div([
                html.P('Sex'),
                dcc.Dropdown(value='None',
                             id='filter-sex',
                             options=[{'label':'Male','value':'Male'},
                                    {'label':'Female','value':'Female'},
                                    {'label':'None','value':'None'}])
                ], className='col-3'),
            html.Div([
                html.P('Day'),
                dcc.Dropdown(value='None',
                             id='filter-day',
                             options=[{'label':'Sunday','value':'Sun'},
                                    {'label':'Saturday','value':'Sat'},
                                    {'label':'Friday','value':'Fri'},
                                    {'label':'None','value':'None'}])
                ], className='col-3'),
            html.Div([
                html.P('Time'),
                dcc.Dropdown(value='None',
                             id='filter-time',
                             options=[{'label':'Lunch','value':'Lunch'},
                                    {'label':'Dinner','value':'Dinner'},
                                    {'label':'None','value':'None'}])
                ], className='col-3')
        ],className='row'),

        html.Br(),
        html.Div([
            html.P('Max Rows :'),
            dcc.Input(id='filter-row',
                    type='number',
                    value=10)
            ], className='row col-3'),
        html.Div(children=[
            html.Button('Search',id='filter')
            ], className='row col-4'),
        
        html.Div(id='div-table', 
                children=[generate_table(tips, page_size=10)])

    ])
], content_style={
    'font_family':'Arial',
    'borderBottom':'1px solid #d6d6d6',
    'borderLeft':'1px solid #d6d6d6',
    'borderRight':'1px solid #d6d6d6',
    'padding':'44px'})
],  style={
    'maxWidth':'1200px',
    'margin':'0 auto'})

@app.callback(
    Output(component_id='div-table', component_property='children'),
    [Input(component_id='filter', component_property='n_clicks')],
    [State(component_id='filter-row', component_property='value'),
    State(component_id='filter-smoker', component_property='value'),
    State(component_id='filter-sex', component_property='value'),
    State(component_id='filter-day', component_property='value'),
    State(component_id='filter-time', component_property='value')]
)
def update_table(n_clicks,row,smoker,sex,day,time):
    tips=sns.load_dataset('tips')
    isi=[smoker,sex,day,time]
    total=['smoker','sex','day','time']
    for i,j in zip(total,isi):
        if j=='None':
            continue
        tips=tips[tips[i]==j]
    children=[generate_table(tips, page_size=row)]
    return children

if __name__=='__main__':
    app.run_server(debug=True)