import plotly.graph_objs as go
import dash
from dash import dcc, html, callback
from dash.dependencies import Input, Output, State
import pandas as pd
df=pd.read_csv('F:\\React_projs2\\BAP_ISE_PROJECT\\marks_att_corr.csv')
months = ['JAN', 'FEB', 'MAR']
colors = ['rgb(255, 0, 0)',  # Red
    'rgb(0, 255, 0)',  # Green
    'rgb(0, 0, 255)',  # Blue
    'rgb(255, 255, 0)',  # Yellow
    'rgb(255, 0, 255)',]
subjects = df.columns[df.columns.str.contains('_Th_%Attended')].str.replace('_Th_%Attended', '')

corr_page =html.Div([
    html.H1('Attendance vs Marks Scatter Plot'),
    html.Label('Select Gender:'),
    dcc.Dropdown(
        id='gender-dropdown',
        options=[
            {'label': 'Male', 'value': 'M'},
            {'label': 'Female', 'value': 'F'},
        ],
        value='M',  # Default selected gender
        clearable=False,
    ),
    html.Label('Select Subject:'),
    dcc.Dropdown(
        id='subject-dropdown',
        options=[{'label': subj, 'value': subj} for subj in subjects],
        value=subjects[0],  # Default selected subject
        clearable=False,
    ),
    html.Div(
    dcc.Graph(id='attendance-marks-scatter'),
    className='figure-container'
    ),
],
className='content'
)

layout = html.Div(
    [
        dcc.Location(id='url', refresh=False),
        corr_page,
        html.Div(id='page-content'),
    ]
)

@callback(
    Output('attendance-marks-scatter', 'figure'),
    [Input('gender-dropdown', 'value')]
)
def update_scatter_plot(selected_gender):
    filtered_df = df[df['Gender'] == selected_gender]

    scatter_plot = go.Figure()
    scatter_plot.add_trace(go.Scatter(
        x=filtered_df['CCN_Th_%Attended'],
        y=filtered_df['CCN_Marks'],
        mode='markers',
        marker=dict(color='blue'),  # Customize marker color if needed
        text=filtered_df['Name'],  # Hover text with student names
        hoverinfo='text+x+y',
        name='CCN'  # Legend label
    ))
    scatter_plot.update_layout(
        title='Attendance vs Marks',
        xaxis_title='Attendance Percentage',
        yaxis_title='Marks',
        showlegend=True,
    )

    return scatter_plot 
