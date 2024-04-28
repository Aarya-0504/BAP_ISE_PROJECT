import pandas as pd
import plotly.graph_objs as go
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
from pages.se_it import se_it_page, update_figures2
from pages.te_ds_ml_dc import te_ds_page, update_figures3, update_figures4
from pages.marks_vs_att_corr import corr_page, update_scatter_plot
df = pd.read_csv('F:\\React_projs2\\BAP_ISE_PROJECT\\data.csv')
df2=pd.read_csv('F:\\React_projs2\\BAP_ISE_PROJECT\\te_cs_nlp.csv')
df3=pd.read_csv('F:\\React_projs2\\BAP_ISE_PROJECT\\marks_att_corr.csv')
subjects_te=['ML','DC']
subjects_nlp=['NLP_TH']
subjects_bap=['BAP']
subjects_bct=['BCT']
#df2=pd.read_csv('F:\\React_projs2\\BAP_ISE_PROJECT\\sample_data_se_it.csv')
# Assuming you have your data in a DataFrame named 'df'

# Create a list of subjects
subjects = ['DS_KKD', 'DWM_SK', 'INS - RP', 'ML_NK', 'ITL_AH']
#subjects_se=['DAA','CCN','DSGT','OS','LA']

# Create a list of months
months = ['JAN', 'FEB', 'MAR']

# Create a list of colors for each subject
colors = ['rgb(255, 0, 0)',  # Red
    'rgb(0, 255, 0)',  # Green
    'rgb(0, 0, 255)',  # Blue
    'rgb(255, 255, 0)',  # Yellow
    'rgb(255, 0, 255)',]

# Create the app
app = dash.Dash(__name__, pages_folder='pages', use_pages=True, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css', 'assets/styles.css'], suppress_callback_exceptions=True)
#app.layout = se_it.layout
#dash.register_page("se_it")

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
                html.Li(html.A('TE IT Page', href='/btech-it')),
                html.Li(html.A('SE IT Page', href='/se-it')),
                html.Li(html.A('TE DS Page', href='/te-ds')),
                html.Li(html.A('Marks vs Attendance Correlation', href='/te-compsA')),
                 
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
        html.H1('TE IT Page'),
        html.Div(
            [
                html.Div(
                    dcc.Graph(id='bar-chart'),
                    className='figure-container',
                ),
                html.Div(
                    dcc.Graph(id='heatmap'),
                    className='figure-container',
                ),
            ],
            className='grid-container',
        ),
        html.Div(
            [
                html.Div(
                    dcc.Graph(id='scatter-plot'),
                    className='figure-container',
                ),
                html.Div(
                    dcc.Graph(id='pie-chart'),
                    className='figure-container',
                ),
            ],
            className='grid-container',
        ),
    ],
    className='content',
)

@app.callback(
    Output('dynamic-plots-container', 'children'),
    [Input('subject-dropdown', 'value')]
)
def update_dynamic_plots(selected_subjects):
    dynamic_divs = []
    for subject in selected_subjects:
        if subject == 'NLP':
            nlp_plots_div=html.Div(
    [
        html.H3('TE DS NLP'),
        html.Div(
            [
                html.Div(
                    dcc.Graph(id='bar-chart4'),
                    className='figure-container',
                ),
                html.Div(
                    dcc.Graph(id='heatmap4'),
                    className='figure-container',
                ),
            ],
            className='grid-container',
        ),
        html.Div(
            [
                html.Div(
                    dcc.Graph(id='scatter-plot4'),
                    className='figure-container',
                ),
                html.Div(
                    dcc.Graph(id='pie-chart4'),
                    className='figure-container',
                ),
            ],
            className='grid-container',
        ),
    ],
    className='content',
)
            dynamic_divs.append(nlp_plots_div)
        if subject == 'BCT':
            bct_plots_div=html.Div(
    [
        html.H1('TE DS BCT Page'),
        html.Div(
            [
                html.Div(
                    dcc.Graph(id='bar-chart5'),
                    className='figure-container',
                ),
                html.Div(
                    dcc.Graph(id='heatmap5'),
                    className='figure-container',
                ),
            ],
            className='grid-container',
        ),
        html.Div(
            [
                html.Div(
                    dcc.Graph(id='scatter-plot5'),
                    className='figure-container',
                ),
                html.Div(
                    dcc.Graph(id='pie-chart5'),
                    className='figure-container',
                ),
            ],
            className='grid-container',
        ),
    ],
    className='content',
)
            dynamic_divs.append(bct_plots_div)
    return dynamic_divs
    
# Define the app layout
app.layout = html.Div(
    [
        dcc.Location(id='url', refresh=False),
        sidebar,
        html.Div(id='page-content'),
    #     html.Div([
    #     html.Div(
    #         dcc.Link(f"{page['name']} - {page['path']}", href=page["relative_path"])
    #     ) for page in dash.page_registry.values()
    # ]),
        dash.page_container
    ]
)

# Callback to update page content based on URL
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/btech-it':
        return btech_it_page
    elif pathname == '/se-it':  # Add this elif block for the SE IT page
        return se_it_page
    elif pathname=='/te-ds':
        return te_ds_page
    elif pathname=='/te-compsA':
        return corr_page
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

# Callback to update figures on SE IT page
@app.callback(
    [Output('bar-chart2', 'figure'),
     Output('heatmap2', 'figure'),
     Output('scatter-plot2', 'figure')],
    [Input('bar-chart2', 'figure'),
     Input('heatmap2', 'figure'),
     Input('scatter-plot2', 'figure')]
)
def update_figures_se_it(bar_chart2, heatmap2, scatter_plot2):
    # Call the update_figures2 function from se_it.py to update figures on SE IT page
    return update_figures2(bar_chart2, heatmap2, scatter_plot2)


@app.callback(
    [Output('bar-chart3', 'figure'),
     Output('heatmap3', 'figure'),
     Output('scatter-plot3', 'figure'),
     Output('pie-chart3', 'figure'),
     ],
    [Input('subject-dropdown', 'value'),
     Input('bar-chart3', 'figure'),
     Input('heatmap3', 'figure'),
     Input('scatter-plot3', 'figure'),
     Input('pie-chart3', 'figure')],)
def update_figures_te_ds(selected_subjects,bar_chart3, heatmap3, scatter_plot3, pie_chart3):
    if not selected_subjects:  # Default subjects if nothing selected
        selected_subjects = ['ML', 'DC']
        return update_figures3(bar_chart3, heatmap3, scatter_plot3, pie_chart3)


@app.callback(
    [Output('bar-chart4', 'figure'),
     Output('heatmap4', 'figure'),
     Output('scatter-plot4', 'figure'),
     Output('pie-chart4', 'figure')],
    [Input('subject-dropdown', 'value')])
def update_figures_te_ds_nlp(selected_subjects):
    if 'NLP' in selected_subjects:
        bar_chart4 = go.Figure()
        bar_chart4.add_trace(go.Bar(x=subjects_nlp, y=[df2[f'{subject}_AVG'].mean() for subject in subjects_nlp], marker_color=colors))
        bar_chart4.update_xaxes(title_text='Subject')
        bar_chart4.update_yaxes(title_text='Average Attendance Percentage')

        # Heatmap for attendance percentage by month and subject
        attendance_data = [[df2[f'{subject}_{month}'].mean() for subject in subjects_nlp] for month in months]
        heatmap4 = go.Figure(data=go.Heatmap(z=attendance_data, x=subjects_nlp, y=months, colorscale='Viridis'))
        heatmap4.update_xaxes(title_text='Subject')
        heatmap4.update_yaxes(title_text='Month')

        # Scatter plot for attendance percentage vs. lecture count
        scatter_plot4 = go.Figure()
        for i, subject in enumerate(subjects_nlp):
            scatter_plot4.add_trace(go.Scatter(x=df2[f'{subject}_JAN_no'] + df2[f'{subject}_FEB_no'] + df2[f'{subject}_MAR_no'],
                                            y=df2[f'{subject}_JAN'] + df2[f'{subject}_FEB'] + df2[f'{subject}_MAR'],
                                            mode='markers', marker=dict(color=colors[i]), name=subject))
        scatter_plot4.update_xaxes(title_text='Total Lecture Count')
        scatter_plot4.update_yaxes(title_text='Attendance Percentage')

        # Pie chart for distribution of attendance ranges
        attendance_ranges = [0, 20, 40, 60, 80, 100]
        attendance_data = []
        for subject in subjects_nlp:
            attendance_count=[
            sum(
                ((df2[f'{subject}_JAN'] + df2[f'{subject}_FEB'] + df2[f'{subject}_MAR']) / 3 >= r1) &
                ((df2[f'{subject}_JAN'] + df2[f'{subject}_FEB'] + df2[f'{subject}_MAR']) / 3 < r2)
            )
            for r1, r2 in zip(attendance_ranges[:-1], attendance_ranges[1:])]
            attendance_data.append(attendance_count)

        
        pie_chart4 = go.Figure(
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
        bar_chart4.update_layout(layout_dark)
        heatmap4.update_layout(layout_dark)
        scatter_plot4.update_layout(layout_dark)
        pie_chart4.update_layout(layout_dark)

        return bar_chart4, heatmap4, scatter_plot4, pie_chart4
    return None,None,None,None

@app.callback(
    Output('attendance-marks-scatter', 'figure'),
    [Input('gender-dropdown', 'value'),
     Input('subject-dropdown', 'value')]
)
def update_scatter_plot(selected_gender, selected_subject):
    filtered_df = df3[(df3['Gender'] == selected_gender) & (df3[selected_subject + '_Th_%Attended'].notna())]

    scatter_plot = go.Figure()
    scatter_plot.add_trace(go.Scatter(
        x=filtered_df[selected_subject + '_Th_%Attended'],
        y=filtered_df[selected_subject + '_Marks'],
        mode='markers',
        marker=dict(color='blue'),  # Customize marker color if needed
        text=filtered_df['Name'],  # Hover text with student names
        hoverinfo='text+x+y',
        name=selected_subject  # Legend label
    ))
    scatter_plot.update_layout(
        title='Attendance vs Marks',
        xaxis_title='Attendance Percentage',
        yaxis_title='Marks',
        showlegend=True,
    )

    return scatter_plot

if __name__ == '__main__':
    app.run_server(debug=True)