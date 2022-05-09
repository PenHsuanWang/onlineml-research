import time

from flask import Flask, request, Response, abort
import pickle
from concurrent import futures
import pandas as pd
from pandas import json_normalize
import json

# Model validation related
from sklearn.metrics import recall_score, accuracy_score, f1_score
# Metrics render via web page
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import plotly.graph_objects as go


class OnlineMachineLearningModelServing:

    def __init__(self):
        """
        Serving
        """
        self._pool = futures.ThreadPoolExecutor(2)
        self._future = None

        self.app = Flask(__name__)

        self.__model = None

        # variable for metrics display
        self.__x_counter = 0
        self.__x_axis = []
        self.__appending_acc = []
        self.__appending_recall = []
        self.__appending_f1 = []

        self.dash_display = Dash(__name__+'dash')

        @self.app.route('/model/', methods=['POST'])
        def model_load():

            try:
                raw_request_message = request.get_json()
                read_path = raw_request_message['model_path']
                print(read_path)
                self.load_model(read_path)

                result_json = {'message': 'Success'}

                return Response(result_json, status=200, mimetype="application/json")

            except:
                print("get model path error, please check key is correct!")
                abort(404)
                pass

        @self.app.route('/model/inference/', methods=['POST'])
        def model_inference() -> Response:
            """
            Model inference api, request contain dataset which want to do predict
            label is not expect to be access in this api.
            :return: http response with prediction result in payload in json format
            """

            try:

                df = extract_http_data_payload(request)

                proba_list, is_target_list = self.inference(df)

                return Response(json.dumps(proba_list), status=200, headers={'content-type': 'application/json'})

            except Exception as e:
                e.with_traceback()
                print("can not extract data, please check!")
                abort(404)


        @self.app.route('/model/validation/', methods=['POST'])
        def model_validation():

            try:

                df = extract_http_data_payload(request)

                #TODO : let label name (Y) configurable
                y = df.pop('Y')

                proba_list, is_target_list = self.inference(df)

                acc = accuracy_score(y, is_target_list)
                recall = recall_score(y, is_target_list)
                f1 = f1_score(y, is_target_list)

                self.__x_axis.append(self.__x_counter)
                self.__x_counter += 1
                self.__appending_acc.append(acc)
                self.__appending_recall.append(recall)
                self.__appending_f1.append(f1)

                print("Accuracy: {}\n recall-rate: {}\n f1 score: {}\n".format(acc, recall, f1))

                return Response(
                    json.dumps(
                        {"accuracy": acc, "recall-rate": recall, "f1 score": f1}
                    ),
                    status=200,
                    headers={'content-type': 'application/json'}
                )


            except Exception as e:
                e.with_traceback()
                print("can not extract data, please check!")
                abort(404)

        # Multiple components can update everytime interval gets fired.
        @self.dash_display.callback(Output('live-update-graph', 'figure'),
                                    Input('interval-component', 'n_intervals'))
        def update_graph_live(n):
            x_list = self.get_x_axis()
            y_list = self.get_accuracy()
            fig_acc = go.Figure()
            fig_acc.add_trace(go.Scatter(
                x=x_list, y=y_list, name='Accuracy',
                line=dict(color='firebrick', width=4)
            ))
            fig_acc.update_layout(
                title='Accuracy Trend Plot',
                xaxis_title='Iteration(s)',
                yaxis_title='Accuracy'
            )
            return fig_acc

        def extract_http_data_payload(request_from_http: request) -> pd.DataFrame:
            """
            extract dataframe from http request
            :param request_from_http: http requests
            :return: dataframe
            """

            receive_data_payload = request_from_http.get_json()
            df = pd.read_json(receive_data_payload)

            return df

    def get_x_axis(self):
        return self.__x_axis

    def get_accuracy(self):
        return self.__appending_acc

    def run(self):
        self._future = self._pool.submit(self.app.run)
        # self.app.run()

    def run_dash(self):

        colors = {
            'background': '#111111',
            'text': '#7FDBFF'
        }

        self.dash_display.layout = html.Div(
            style={'backgroundColor': colors['background']},
            children=[
                html.H1(
                    children='Hello Dash',
                    style={
                        'textAlign': 'center',
                        'color': colors['text']
                    }
                ),
                html.Div(
                    children=
                    '''
                    Dash: A web application framework for your data.
                    ''',
                    style={
                        'textAlign': 'center',
                        'color': colors['text']
                    }
                ),
                dcc.Graph(id='live-update-graph'),
                dcc.Interval(
                    interval=1*1000,  # in milliseconds
                    n_intervals=1000
                )
            ])

        # self.dash_display.run_server()
        self._future = self._pool.submit(self.dash_display.run_server)


    def load_model(self, path: str):
        """
        The implementation of the trigger acceptance api to load model from specify file path.
        :param path: path of model to load
        :return:
        """
        with open(path, 'rb') as f:
            self.__model = pickle.load(f)

    def inference(self, data: pd.DataFrame, proba_cut_point=0.5) -> (list, list):
        """
        The implementation of hoeffding tree model inference.
        return two list,\n
        the first one is the list of prediction probability if this inference is target (float). e.g. 0.35 -> 35% of change is target\n
        the second one is the list of prediction true/false if this inference is target (int). e.g. 1 -> this is target\n
        :param data: input data frame
        :param proba_cut_point: float
        :return: (prediction_probability in list, prediction_is_target)
        """

        pred_target_proba = []
        pred_is_target = []

        for index, raw in data.iterrows():

            result = self.__model.predict_proba_one(raw)

            try:

                pred_target_proba.append(result.get(1))

                if proba_cut_point is not None:
                    if result.get(1) >= proba_cut_point:
                        pred_is_target.append(1)
                    else:
                        pred_is_target.append(0)

            except Exception as e:
                pred_target_proba.append(None)
                pred_is_target.append(None)
                e.with_traceback()

        return pred_target_proba, pred_is_target



if __name__ == '__main__':

    online_model_serving = OnlineMachineLearningModelServing()
    online_model_serving.run()
    online_model_serving.run_dash()





