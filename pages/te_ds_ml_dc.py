import pandas as pd
import plotly.graph_objs as go
import dash
from dash import dcc, html, callback
from dash.dependencies import Input, Output, State
df=pd.read_csv('F:\\React_projs2\\BAP_ISE_PROJECT\\te_cs_mldc.csv')
subjects_te=['ML','DC']
months = ['JAN', 'FEB', 'MAR']
colors = ['rgb(255, 0, 0)',  # Red
    'rgb(0, 255, 0)',  # Green
    'rgb(0, 0, 255)',  # Blue
    'rgb(255, 255, 0)',  # Yellow
    'rgb(255, 0, 255)',]

te_ds_page = html.Div(
    [
        html.H1('TE DS Page'),
        html.Div(
            [
                html.Div(
                    dcc.Graph(id='bar-chart3'),
                    className='figure-container',
                ),
                html.Div(
                    dcc.Graph(id='heatmap3'),
                    className='figure-container',
                ),
            ],
            className='grid-container',
        ),
        html.Div(
            [
                html.Div(
                    dcc.Graph(id='scatter-plot3'),
                    className='figure-container',
                ),
                html.Div(
                    dcc.Graph(id='pie-chart3'),
                    className='figure-container',
                ),
            ],
            className='grid-container',
        ),
    ],
    className='content',
)

layout = html.Div(
    [
        dcc.Location(id='url', refresh=False),
        te_ds_page,
        html.Div(id='page-content'),
    ]
)

@callback(
    [Output('bar-chart3', 'figure'),
     Output('heatmap3', 'figure'),
     Output('scatter-plot3', 'figure'),
     Output('pie-chart3','figure')],
    [Input('bar-chart3', 'figure'),
     Input('heatmap3', 'figure'),
     Input('scatter-plot3', 'figure'),
     Input('pie-chart3', 'figure')]
)

def update_figures3(bar_chart3, heatmap3, scatter_plot3, pie_chart3):
    # Bar chart for average attendance percentage
    bar_chart3 = go.Figure()
    bar_chart3.add_trace(go.Bar(x=subjects_te, y=[df[f'{subject}_AVG'].mean() for subject in subjects_te], marker_color=colors))
    bar_chart3.update_xaxes(title_text='Subject')
    bar_chart3.update_yaxes(title_text='Average Attendance Percentage')

    # Heatmap for attendance percentage by month and subject
    attendance_data = [[df[f'{subject}_{month}'].mean() for subject in subjects_te] for month in months]
    heatmap3 = go.Figure(data=go.Heatmap(z=attendance_data, x=subjects_te, y=months, colorscale='Viridis'))
    heatmap3.update_xaxes(title_text='Subject')
    heatmap3.update_yaxes(title_text='Month')

    # Scatter plot for attendance percentage vs. lecture count
    scatter_plot3 = go.Figure()
    for i, subject in enumerate(subjects_te):
        scatter_plot3.add_trace(go.Scatter(x=df[f'{subject}_JAN_no'] + df[f'{subject}_FEB_no'] + df[f'{subject}_MAR_no'],
                                          y=df[f'{subject}_JAN'] + df[f'{subject}_FEB'] + df[f'{subject}_MAR'],
                                          mode='markers', marker=dict(color=colors[i]), name=subject))
    scatter_plot3.update_xaxes(title_text='Total Lecture Count')
    scatter_plot3.update_yaxes(title_text='Attendance Percentage')

    # Pie chart for distribution of attendance ranges
    attendance_ranges = [0, 20, 40, 60, 80, 100]
    attendance_data = []
    for subject in subjects_te:
        attendance_count=[
        sum(
            ((df[f'{subject}_JAN'] + df[f'{subject}_FEB'] + df[f'{subject}_MAR']) / 3 >= r1) &
            ((df[f'{subject}_JAN'] + df[f'{subject}_FEB'] + df[f'{subject}_MAR']) / 3 < r2)
        )
        for r1, r2 in zip(attendance_ranges[:-1], attendance_ranges[1:])]
        attendance_data.append(attendance_count)

    
    pie_chart3 = go.Figure(
        data=[
            go.Pie(
                labels=[f'{r1}-{r2}%' for r1, r2 in zip(attendance_ranges[:-1], attendance_ranges[1:])],
                values=sum(attendance_data, []),
                name='Attendance Distribution'
            )
        ]
    )

    layout_dark = go.Layout(
        plot_bgcolor='rgb(20, 20, 20)',  # Dark background color
        paper_bgcolor='rgb(20, 20, 20)',  # Dark background color for plot area
        font=dict(color='white'),  # Font color
    )
    bar_chart3.update_layout(layout_dark)
    heatmap3.update_layout(layout_dark)
    scatter_plot3.update_layout(layout_dark)
    pie_chart3.update_layout(layout_dark)

    return bar_chart3, heatmap3, scatter_plot3, pie_chart3


