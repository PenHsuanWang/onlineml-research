import os, glob
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import base64
from PIL import Image
from io import BytesIO

from plotly.graph_objs import Layout
import numpy as np
from plotly import express as px



from serving.onlineml_model_serving import OnlineMachineLearningModelServing

# Static method to show figure from local file


# def tree_structure_inspect_display(display_fig_path: str):
#     if len(display_fig_path) > 0:
#         try:
#             image_filename = display_fig_path  # image path
#             encoded_image = base64.b64encode(open(image_filename, 'rb').read())
#             return html.Div([
#                 html.H3("current Hoeffding Tree Structure"),
#                 html.Br(),
#                 html.Img(
#                     src='data:image/png;base64,{}'.format(encoded_image.decode()),
#                     title='live check model structure'
#                 )
#             ])
#         except:
#             return html.Div([
#                 html.H3("Model Structure inspection figure path is not correct: {}, fail to load image!".format(image_filename)),
#             ])
#     else:
#         return html.Div([
#             html.H3("invalid input, please support correct input figure path: grid_layout_tree_structure_inspect_display(<path>)"),
#         ])


def card_content_image_synthesis_text_bottom(image_filename: str, style={}, figure_title_prefix=''):

    encoded_image = base64.b64encode(open(image_filename, 'rb').read())
    figure_title_from_file_name = image_filename.split('/')[-1].split('.')[0].split('_')[-1]
    card_content = [
        dbc.CardImg(src='data:image/png;base64,{}'.format(encoded_image.decode()), top=True, style=style),
        dbc.CardBody(
            [
                html.H4("{}: {}".format(figure_title_prefix, figure_title_from_file_name), className="card-title"),
                html.P(
                    "Some quick example text to build on the card title and "
                    "make up the bulk of the card's content.",
                    className="card-text",
                ),
                dbc.Button("Go somewhere", color="primary"),
            ]
        ),

    ]
    return card_content


def card_content_image_synthesis_text_right(image_filename: str, style={}):
    encoded_image = base64.b64encode(open(image_filename, 'rb').read())
    tree_name = image_filename.split('/')[-1].split('.')[0].split('_')[-1]
    card_content = [
        dbc.Row(
            [
                dbc.Col(
                    dbc.CardImg(src='data:image/png;base64,{}'.format(encoded_image.decode()), top=True, style=style),
                    className="col-md-4",
                ),
                dbc.Col(
                    dbc.CardBody(
                        [
                            html.H4("Card title", className="card-title"),
                            html.P(
                                "This is a wider card with supporting text "
                                "below as a natural lead-in to additional "
                                "content. This content is a bit longer.",
                                className="card-text",
                            ),
                            html.Small(
                                "Last updated 3 mins ago",
                                className="card-text text-muted",
                            ),
                        ]
                    ),
                    className="col-md-8",
                ),
            ],
            className="g-0 d-flex align-items-center",
        )
    ]
    return card_content


def listall_layout_tree_structure_inspace_display(display_fig_dir: str, file_filter_pattern='', figure_title_prefix=''):

    if os.path.isdir(display_fig_dir):
        listing_image = glob.glob(display_fig_dir+'*'+file_filter_pattern+'*.png')
        listing_image.sort()

    list_to_image_display = []

    style = {'height': '50', 'width': '50%'}

    for file in listing_image:

        list_to_image_display.extend([
            html.Br(),
            dbc.Row(
                [dbc.Col(dbc.Card(card_content_image_synthesis_text_bottom(
                    image_filename=file,
                    style=style,
                    figure_title_prefix=figure_title_prefix
                ), color='primary', outline=True))],
                align='center',
            ),
            html.Br()
        ])
    return html.Div(
        list_to_image_display
    )



def grid_layout_tree_structure_inspect_display(display_fig_dir: str, file_filter_pattern=''):

    listing_image = []

    if os.path.isdir(display_fig_dir):
        # TODO: Make glob add function to provide regex explaining pattern to filter file.
        listing_image = glob.glob(display_fig_dir+'*'+file_filter_pattern+'*.png')
        listing_image.sort()

    style = {'height': '200px', 'width': '100%'}

    return html.Div(
        [
            html.Br(),
            dbc.Row(
                [
                    dbc.Col(dbc.Card(card_content_image_synthesis_text_bottom(
                        image_filename=listing_image[1],
                        style=style,
                        figure_title_prefix='Tree Number'
                    ), color='primary', outline=True)),
                    dbc.Col(dbc.Card(card_content_image_synthesis_text_bottom(
                        image_filename=listing_image[2],
                        style=style,
                        figure_title_prefix='Tree Number'
                    ), color='primary', outline=True)),
                    dbc.Col(dbc.Card(card_content_image_synthesis_text_bottom(
                        image_filename=listing_image[3],
                        style=style,
                        figure_title_prefix='Tree Number'
                    ), color='primary', outline=True))
                ],
                align='center',
            ),
            html.Br(),
            dbc.Row(
                [
                    dbc.Col(dbc.Card(card_content_image_synthesis_text_bottom(
                        image_filename=listing_image[4],
                        style=style,
                        figure_title_prefix='Tree Number'
                    ), color='primary', outline=True)),
                    dbc.Col(dbc.Card(card_content_image_synthesis_text_bottom(
                        image_filename=listing_image[5],
                        style=style,
                        figure_title_prefix='Tree Number'
                    ), color='primary', outline=True)),
                    dbc.Col(dbc.Card(card_content_image_synthesis_text_bottom(
                        image_filename=listing_image[6],
                        style=style,
                        figure_title_prefix='Tree Number'
                    ), color='primary', outline=True))
                ],
                align='center',
            ),
            html.Br(),
            dbc.Row(
                [
                    dbc.Col(dbc.Card(card_content_image_synthesis_text_bottom(
                        image_filename=listing_image[7],
                        style=style,
                        figure_title_prefix='Tree Number'
                    ), color='primary', outline=True)),
                    dbc.Col(dbc.Card(card_content_image_synthesis_text_bottom(
                        image_filename=listing_image[8],
                        style=style,
                        figure_title_prefix='Tree Number'
                    ), color='primary', outline=True)),
                    dbc.Col(dbc.Card(card_content_image_synthesis_text_bottom(
                        image_filename=listing_image[9],
                        style=style,
                        figure_title_prefix='Tree Number'
                    ), color='primary', outline=True))
                ],
                align='center',
            ),

        ]
    )


class ModelPerformanceMonitor:

    _instance = None

    @staticmethod
    def get_instance():
        if ModelPerformanceMonitor._instance is None:
            ModelPerformanceMonitor._instance = ModelPerformanceMonitor()
        return ModelPerformanceMonitor._instance

    def __init__(self):

        self._online_ml_server = OnlineMachineLearningModelServing.get_instance()
        self.dash_display = Dash(__name__+'dash', external_stylesheets=[dbc.themes.BOOTSTRAP])

        # Multiple components can update everytime interval gets fired.
        @self.dash_display.callback(Output('live-update-acc-graph', 'figure'),
                                    Input('interval-component', 'n_intervals'))
        def update_acc_trend_live(n):
            x_list = self._online_ml_server.get_x_axis()
            y_list = self._online_ml_server.get_accuracy()
            y_batch_list = self._online_ml_server.get_batch_acc()
            fig_acc = go.Figure()
            fig_acc.add_trace(go.Scatter(
                x=x_list, y=y_list, name='Accuracy',
                line=dict(color='firebrick', width=4)
            ))
            fig_acc.add_trace(go.Scatter(
                x=x_list, y=y_batch_list, name='Batch Accuracy',
                line=dict(color='#545454', width=4, dash='dash')
            ))
            fig_acc.update_layout(
                title='Accuracy Trend Plot',
                xaxis_title='Iteration(s)',
                yaxis_title='Accuracy',
                yaxis_range=[0.5, 1]
            )
            return fig_acc

        @self.dash_display.callback(Output('live-update-f1-graph', 'figure'),
                                    Input('interval-component', 'n_intervals'))
        def update_f1_trend_live(n):
            x_list = self._online_ml_server.get_x_axis()
            y_list = self._online_ml_server.get_f1_score()
            y_batch_list = self._online_ml_server.get_batch_f1()
            fig_f1 = go.Figure()
            fig_f1.add_trace(go.Scatter(
                x=x_list, y=y_list, name='f1-score',
                line=dict(color='blue', width=4)
            ))
            fig_f1.add_trace(go.Scatter(
                x=x_list, y=y_batch_list, name='Batch f1-score',
                line=dict(color='#545454', width=4, dash='dash')
            ))
            fig_f1.update_layout(
                title='f1 scores Trend Plot',
                xaxis_title='Iteration(s)',
                yaxis_title='f1 Score',
                yaxis_range=[0.5, 1]
            )
            return fig_f1

        @self.dash_display.callback(Output('live-update-predict-proba', 'figure'),
                                    Input('interval-component', 'n_intervals'))
        def show_predict_proba_distribution(n):
            img = None
            try:
                encoded_image = base64.b64encode(open('../../output_plot/web_checker_online_display/online_pred_proba_distribution/pred_proba_check.png', 'rb').read())
                img = Image.open(BytesIO(base64.b64decode(encoded_image)))
            except FileNotFoundError:
                pass

            layout = Layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            fig_proba_dist = go.Figure(layout=layout)
            fig_proba_dist.update_xaxes(visible=False, showticklabels=False)
            fig_proba_dist.update_yaxes(visible=False, showticklabels=False)

            fig_proba_dist.add_layout_image(
                source=img,
                xref="paper",
                yref="paper",
                x=0.1,
                y=1,
                sizex=1,
                sizey=1,
            )

            return fig_proba_dist

        @self.dash_display.callback(Output('live-update-tree-structure', 'figure'),
                                    Input('interval-component', 'n_intervals'))
        def show_online_tree_structure(n):
            encoded_image = base64.b64encode(
                open('../../output_plot/web_checker_online_display/online_tree_inspection/current_tree_structure_tree_0.png',
                     'rb').read())
            img = Image.open(BytesIO(base64.b64decode(encoded_image)))

            layout = Layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            fig_tree = go.Figure(layout=layout)
            fig_tree.update_xaxes(visible=False, showticklabels=False)
            fig_tree.update_yaxes(visible=False, showticklabels=False)

            fig_tree.add_layout_image(
                source=img,
                xref="paper",
                yref="paper",
                x=0.1,
                y=1,
                sizex=1,
                sizey=1,
            )

            return fig_tree



        @self.dash_display.callback(Output('model-performance-page', 'children'),
                                    [Input('url', 'pathname')])
        def display_page(pathname):
            if pathname == '/inference_performance':
                return html.Div([
                    dbc.Row([
                        dbc.Col(
                            dcc.Graph(id='live-update-acc-graph'),
                        ),
                        dbc.Col(
                            dcc.Graph(id='live-update-f1-graph'),
                        )
                    ]),
                    dcc.Graph(id='live-update-predict-proba'),
                    dcc.Graph(id='live-update-tree-structure'),
                    dcc.Interval(
                        id='interval-component',
                        interval=1 * 1000,  # in milliseconds
                        n_intervals=0
                    ),
                ])

            elif pathname == '/current_model_structure':
                return grid_layout_tree_structure_inspect_display(
                    display_fig_dir='../../output_plot/web_checker_online_display/online_tree_inspection/'
                )
            elif pathname == '/predict_proba_distribution_history':
                return listall_layout_tree_structure_inspace_display(
                    display_fig_dir='../../output_plot/web_checker_historical_check/model_pred_proba_distribution/',
                    figure_title_prefix='snapshot timestamp'
                )
            else:
                return html.Div([
                    dcc.Link(children='Go to Model Inference Performance Page.',
                             href='/inference_performance'
                             ),
                    html.Br(),
                    dcc.Link(children='Go to Model Prediction Proba Distribution history check',
                             href='/predict_proba_distribution_history'),
                    html.Br(),
                    dcc.Link(children='Go to Model Structure inspection page.',
                             href='/current_model_structure'
                             )
                ])


    def run_dash(self):

        colors = {
            'background': '#111111',
            'text': '#7FDBFF'
        }

        self.dash_display.layout = html.Div(

            [
                dcc.Location(id='url', refresh=False),

                # first division for title and web mete message
                html.Div(
                    style={'backgroundColor': colors['background']},
                    children=[
                        html.H1(
                            children='Online Machine Learning Checker',
                            style={
                                'textAlign': 'center',
                                'color': colors['text']
                            }
                        ),
                        html.Div(
                            children=
                            '''
                            Model Performance live-updating monitor
                            ''',
                            style={
                                'textAlign': 'center',
                                'color': colors['text']
                            }
                        ),
                    ]
                ),

                # definition of plot at display function
                html.Div(id="model-performance-page")

            ]
        )

        self.dash_display.run_server()
        # self._future = self._pool.submit(self.dash_display.run_server)
