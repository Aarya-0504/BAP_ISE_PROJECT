import pandas as pd
import plotly.graph_objs as go
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State

df = pd.read_csv('F:\\React_projs2\\BAP_ISE_PROJECT\\data.csv')
# Assuming you have your data in a DataFrame named 'df'

# Create a list of subjects
subjects = ['DS_KKD', 'DWM_SK', 'INS - RP']

# Create a list of months
months = ['JAN', 'FEB', 'MAR']

# Create a list of colors for each subject
colors = ['rgb(255, 0, 0)', 'rgb(0, 255, 0)', 'rgb(0, 0, 255)']

# Create the app
app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css', 'assets/styles.css'], suppress_callback_exceptions=True)


# Define the sidebar layout
sidebar = html.Div(
    [
        html.H2('Navigation'),
        html.Button(
            'Toggle Sidebar',
            id='toggle-sidebar-button',
            n_clicks=0,
            style={'margin-bottom': '20px'},
        ),
        html.Ul(
            [
                html.Li(html.A('Introduction', href='/')),
                html.Li(html.A('BTECH IT Page', href='/btech-it')),
            ],
            style={'list-style-type': 'none', 'padding': 0},
        ),
    ],
    id='sidebar',
    className='sidebar'
   # style={'width': '240px'}
)

# Define the introduction layout
introduction_page = html.Div(
    [
        html.H1('Welcome to Attendance Dashboard'),
        html.P('This is an introduction page for the attendance dashboard.'),
    ],
    className='content',
)

# Define the BTECH IT page layout
btech_it_page = html.Div(
    [
        html.H1('BTECH IT Page'),
        dcc.Graph(id='bar-chart'),
        dcc.Graph(id='heatmap'),
        dcc.Graph(id='scatter-plot'),
        dcc.Graph(id='pie-chart'),
    ],
    className='content',
)

# Define the app layout
app.layout = html.Div(
    [
        dcc.Location(id='url', refresh=False),
        sidebar,
        html.Div(id='page-content'),
    ]
)

# Callback to update page content based on URL
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/btech-it':
        return btech_it_page
    else:
        return introduction_page
    
# @app.callback([Output('sidebar', 'style'),
#                Output('toggle-sidebar-button', 'n_clicks')],
#               [Input('toggle-sidebar-button', 'n_clicks')],
#               [State('sidebar', 'style'),
#                State('toggle-sidebar-button', 'n_clicks')])
# def toggle_sidebar_width(n_clicks, style, current_n_clicks):
#     if n_clicks is None:
#         n_clicks = 0
#     if n_clicks % 2 == 0:
#         style['width'] = '250px'
#     else:
#         style['width'] = '0px'
#     return style, current_n_clicks + 1

# Callbacks to update graphs
@app.callback(
    [Output('bar-chart', 'figure'),
     Output('heatmap', 'figure'),
     Output('scatter-plot', 'figure'),
     Output('pie-chart', 'figure')],
    [Input('bar-chart', 'figure'),
     Input('heatmap', 'figure'),
     Input('scatter-plot', 'figure'),
     Input('pie-chart', 'figure')])
def update_figures(bar_chart, heatmap, scatter_plot, pie_chart):
    # Bar chart for average attendance percentage
    bar_chart = go.Figure()
    bar_chart.add_trace(go.Bar(x=subjects, y=[df[f'{subject}_AVG'].mean() for subject in subjects], marker_color=colors))
    bar_chart.update_xaxes(title_text='Subject')
    bar_chart.update_yaxes(title_text='Average Attendance Percentage')

    # Heatmap for attendance percentage by month and subject
    attendance_data = [[df[f'{subject}_{month}'].mean() for subject in subjects] for month in months]
    heatmap = go.Figure(data=go.Heatmap(z=attendance_data, x=subjects, y=months, colorscale='Viridis'))
    heatmap.update_xaxes(title_text='Subject')
    heatmap.update_yaxes(title_text='Month')

    # Scatter plot for attendance percentage vs. lecture count
    scatter_plot = go.Figure()
    for i, subject in enumerate(subjects):
        scatter_plot.add_trace(go.Scatter(x=df[f'{subject}_JAN_no'] + df[f'{subject}_FEB_no'] + df[f'{subject}_MAR_no'],
                                          y=df[f'{subject}_JAN'] + df[f'{subject}_FEB'] + df[f'{subject}_MAR'],
                                          mode='markers', marker=dict(color=colors[i]), name=subject))
    scatter_plot.update_xaxes(title_text='Total Lecture Count')
    scatter_plot.update_yaxes(title_text='Attendance Percentage')

    # Pie chart for distribution of attendance ranges
    attendance_ranges = [0, 20, 40, 60, 80, 100]
    attendance_data = []
    for subject in subjects:
        attendance_count=[
        sum(
            ((df[f'{subject}_JAN'] + df[f'{subject}_FEB'] + df[f'{subject}_MAR']) / 3 >= r1) &
            ((df[f'{subject}_JAN'] + df[f'{subject}_FEB'] + df[f'{subject}_MAR']) / 3 < r2)
        )
        for r1, r2 in zip(attendance_ranges[:-1], attendance_ranges[1:])]
        attendance_data.append(attendance_count)

    
    pie_chart = go.Figure(
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
    bar_chart.update_layout(layout_dark)
    heatmap.update_layout(layout_dark)
    scatter_plot.update_layout(layout_dark)
    pie_chart.update_layout(layout_dark)

    return bar_chart, heatmap, scatter_plot, pie_chart


if __name__ == '__main__':
    app.run_server(debug=True)