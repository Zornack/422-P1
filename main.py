import influxdb_client, os, time
import flask_wtf
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from flask import Flask, request, render_template
from flask_restful import Resource, Api
import os
import flask

from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

import sys

from flask import request
from multiprocessing import Process



import webbrowser
from threading import Timer

from multiprocessing import Process



app = Flask(__name__)
api = Api(app)

app.config['SECRET_KEY'] = 'C2HWGVoMGfNTBsrYQg8EcMrdTimkZfAb'

NFLUXDB_TOKEN="gomxXR2r81BLraj5T9wsUp1jWydoieYICCyqVJQE_fW_4_ZMVW3e5-95gDU3maNC9XCjPL9xVQLc-oGVO2C7WQ=="

token = NFLUXDB_TOKEN
org = "jcsdavis@gmail.com"
url = "https://us-west-2-2.aws.cloud2.influxdata.com"

client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

write_api = client.write_api(write_options=SYNCHRONOUS)

sensor_names = {"LI":"light", "HU":"humidity", "ST":"soil_temp",
                "AT":"air_temp", "SM":"soil_moisture"}

server = Process(target=app.run)

def shutdown_flask(self):
    from win32api import GenerateConsoleCtrlEvent
    CTRL_C_EVENT = 0
    GenerateConsoleCtrlEvent(CTRL_C_EVENT, 0)


@app.route("/", methods=['GET', 'POST'])
def index():
    # if request.method == 'POST':
    #     if request.form.get('action1') == 'VALUE1':
    #         from win32api import GenerateConsoleCtrlEvent
    #         CTRL_C_EVENT = 0
    #         GenerateConsoleCtrlEvent(CTRL_C_EVENT, 0)
    #     elif request.form.get('action2') == 'VALUE2':
    #         webbrowser.open_new('https://www.google.com/')  # do something else
    user = "Jaryd"
    return render_template("home.html",
                            user_name = "Jaryd",
                            graph_code = "<i>put graph here</i>")

@app.route('/upload', methods=["GET", "POST"])
def get_data():
    # data = request.files['file']
    # print("hi")
    bucket = "test"
    # data = request.form
    # data = dict(data)
    # for value in range(5):
    #     point = (
    #         Point("measurement1")
    #             .tag("tagname1", "tagvalue1")
    #             .field("field1", value)
    #     )
    # write_api.write(bucket=bucket, org="jcsdavis@gmail.com", record=point)
    query_api = client.query_api()

    query = """from(bucket: "test2")
     |> range(start: -525600m)
     |> filter(fn: (r) => r._measurement == "measurement1")"""
    tables = query_api.query(query, org="jcsdavis@gmail.com")

    for table in tables:
        for record in table.records:
            print(record)
    return "success"


@app.route('/postmethod', methods=["GET", "POST"])
def get_post_javascript_data():
    from win32api import GenerateConsoleCtrlEvent
    CTRL_C_EVENT = 0
    GenerateConsoleCtrlEvent(CTRL_C_EVENT, 0)
    return "success"



# @app.route('/getmethod/<jsdata>')
# def get_javascript_data(jsdata):
#     if request.method == 'GET':
#         if request.form.get('action1') == 'VALUE1':
#             from win32api import GenerateConsoleCtrlEvent
#             CTRL_C_EVENT = 0
#             GenerateConsoleCtrlEvent(CTRL_C_EVENT, 0)

@app.route("/write", methods = ['POST'])
def write():
    user = "Jaryd"
    d = parse_line(request.data.decode("UTF-8"), "Jaryd")
    print(d, flush=True)
    return {'result': "OK"}, 200

def parse_line(line, user_name):
    data = {"device" : line[:2],
            "sensor_name" : sensor_names.get(line[2:4], "unkown"),
            "value" : line[4:],
            "user": user_name}
    return data


def open_browser():
    webbrowser.open_new('http://localhost:5000/')

if __name__ == '__main__':
    from waitress import serve
    open_browser()
    serve(app, host="0.0.0.0", port = 5000)