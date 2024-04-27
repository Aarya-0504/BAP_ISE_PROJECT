import pandas as pd
import plotly.graph_objs as go
import dash
from dash import dcc, html, callback, dash_table
from dash.dependencies import Input, Output, State
#dash.register_page(__name__, path='/se-it',name="se_it")
df=pd.read_csv('F:\\React_projs2\\BAP_ISE_PROJECT\\se_it_data.csv')

subjects_se=['DAA','CCN','DSGT','OS','LA']
colors = ['rgb(255, 0, 0)',  # Red
    'rgb(0, 255, 0)',  # Green
    'rgb(0, 0, 255)',  # Blue
    'rgb(255, 255, 0)',  # Yellow
    'rgb(255, 0, 255)',]

se_it_page = html.Div(
    [
        html.H1('SE IT Page'),
        html.Div(
            [
                html.Div(
                    dcc.Graph(id='bar-chart2'),
                    className='figure-container',
                ),
                html.Div(
                    dcc.Graph(id='heatmap2'),
                    className='figure-container',
                ),
            ],
            className='grid-container',
        ),
        html.Div(
            [
                html.Div(
                    dcc.Graph(id='scatter-plot2'),
                    className='figure-container',
                ),
                html.Div(
                    dcc.Graph(id='pie-chart2'),
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
        se_it_page,
        html.Div(id='page-content'),
    ]
)

@callback(
    [Output('bar-chart2', 'figure'),
     Output('heatmap2', 'figure'),
     Output('scatter-plot2', 'figure')],
    [Input('bar-chart2', 'figure'),
     Input('heatmap2', 'figure'),
     Input('scatter-plot2', 'figure')]
)

def update_figures2(bar_chart2, heatmap2, scatter_plot2):
    # Bar chart for average attendance percentage
    bar_chart2 = go.Figure()
    bar_chart2.add_trace(go.Bar(x=subjects_se, y=[df[f'{subject}_AVG'].mean() for subject in subjects_se], marker_color=colors))
    bar_chart2.update_xaxes(title_text='Subject')
    bar_chart2.update_yaxes(title_text='Average Attendance Percentage')

    # Heatmap for attendance percentage by month and subject
    attendance_data = [df[f'{subject}_AVG'].mean() for subject in subjects_se]
    heatmap2 = go.Figure(data=go.Heatmap(y=attendance_data, x=subjects_se, colorscale='Viridis'))
    heatmap2.update_xaxes(title_text='Subject')
    heatmap2.update_yaxes(title_text='Month')

    # Scatter plot for attendance percentage vs. lecture count
    scatter_plot2 = go.Figure()
    for i, subject in enumerate(subjects_se):
        scatter_plot2.add_trace(go.Scatter(x=df[f'{subject}_AVG'], 
                                          y=df[f'{subject}_AVG_no'] ,
                                          mode='markers', marker=dict(color=colors[i]), name=subject))
    scatter_plot2.update_xaxes(title_text='Total Lecture Count')
    scatter_plot2.update_yaxes(title_text='Attendance Percentage')

    # Pie chart for distribution of attendance ranges
    # attendance_ranges = [0, 20, 40, 60, 80, 100]
    # attendance_data = []
    # for subject in subjects:
    #     attendance_count=[
    #     sum(
    #         ((df[f'{subject}_JAN'] + df[f'{subject}_FEB'] + df[f'{subject}_MAR']) / 3 >= r1) &
    #         ((df[f'{subject}_JAN'] + df[f'{subject}_FEB'] + df[f'{subject}_MAR']) / 3 < r2)
    #     )
    #     for r1, r2 in zip(attendance_ranges[:-1], attendance_ranges[1:])]
    #     attendance_data.append(attendance_count)

    
    # pie_chart = go.Figure(
    #     data=[
    #         go.Pie(
    #             labels=[f'{r1}-{r2}%' for r1, r2 in zip(attendance_ranges[:-1], attendance_ranges[1:])],
    #             values=sum(attendance_data, []),
    #             name='Attendance Distribution'
    #         )
    #     ]
    # )

    layout_dark = go.Layout(
        plot_bgcolor='rgb(20, 20, 20)',  # Dark background color
        paper_bgcolor='rgb(20, 20, 20)',  # Dark background color for plot area
        font=dict(color='white'),  # Font color
    )
    bar_chart2.update_layout(layout_dark)
    heatmap2.update_layout(layout_dark)
    scatter_plot2.update_layout(layout_dark)
   # pie_chart.update_layout(layout_dark)

    return bar_chart2, heatmap2, scatter_plot2

