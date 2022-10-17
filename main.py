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
from pip._vendor import requests
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import json
from flask_wtf import FlaskForm as Form
import sys
from wtforms import BooleanField, StringField, validators, SelectMultipleField
from flask import request
from multiprocessing import Process
import requests
import datetime
import wtforms_validators
from wtforms_validators import ActiveUrl, Alpha, AlphaSpace, AlphaNumeric


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

class NameForm(Form):
    name = StringField('TS Name', [validators.Length(min=1, max=50,message=u"Huh, little too short."),
                                        validators.InputRequired(u"Please enter a name for the Time Series"), validators.Regexp('^[a-zA-Z0-9 ]*$', message="Time Series name can only contain letters, numbers and spaces.")])
    description = StringField('Description', [validators.Length(min=1, max=50,message=u"Huh, little too short."),
                                        validators.InputRequired(u"Please enter a description for the Time Series"), validators.Regexp('^[a-zA-Z0-9 ]*$', message="Time Series description can only contain letters, numbers and spaces.")])
    domain = StringField('Application domain(s)', [validators.Length(min=1, max=50,message=u"Huh, little too short."),
                                        validators.InputRequired(u"Please enter a domain."), validators.Regexp('^[a-zA-Z0-9 ]*$', message="Time Series description can only contain letters, numbers and spaces.")])
    contributors = StringField('Contributors', [validators.Length(min=0, max=50, message=u"Huh, little too short."),
                                   validators.Regexp('^[a-zA-Z0-9 ]*$',message="Time Series name can only contain letters, numbers and spaces.")])
    reference = StringField('Paper reference', [validators.Length(min=0, max=50, message=u"Huh, little too short."),
                                   validators.Regexp('^[a-zA-Z0-9 ]*$',message="Time Series name can only contain letters, numbers and spaces.")])
    referenceLink = StringField('Referece link', [validators.Length(min=0, max=50, message=u"Huh, little too short."),
                                   validators.Regexp('^[a-zA-Z0-9 ]*$',message="Time Series name can only contain letters, numbers and spaces.")])


# #                                         validators.InputRequired(u"Please enter a name for the Time Series")])

# class NameForm(Form):
#       name = StringField('TS Name', [DataRequired(), AlphaNumeric(), AlphaSpace()])
#       # name = StringField('TS Name', [DataRequired(), Alpha()])
#     name = StringField('TS Name', [validators.Length(min=1, max=50,message=u"Huh, little too short."),
#                                         validators.InputRequired(u"Please enter a name for the Time Series")])
#     name = StringField('TS Name', [validators.Length(min=1, max=50,message=u"Huh, little too short."),
#                                         validators.InputRequired(u"Please enter a name for the Time Series")])

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
    return render_template("home.html")

@app.route('/buckets', methods=["GET", "POST"])
def buckets():
    url = 'https://us-west-2-2.aws.cloud2.influxdata.com/api/v2/buckets'
    headers = {
        'Authorization': 'Token Urle4ZrRmKg_L1XG9BjzO_oBMc1zj-Fy84779erAppxBGUYgLMArHF_QnzgAPv_l0xiIRpXNwccYHm_eWGHjlg=='}
    r = requests.get(url, headers=headers)
    testr = json.loads(r.text)
    # testr['buckets'].pop(3)
    # testr['buckets'].pop
    badNames = ['_monitoring', '_tasks']
    badNamesIndex = 0
    for i in range(0,len(testr['buckets'])):
        if testr['buckets'][i]['name'] == '_monitoring':
            badNamesIndex = i
    testr['buckets'].pop(badNamesIndex)
    testr['buckets'].pop(badNamesIndex)
    write_api = client.write_api(write_options=SYNCHRONOUS)
    query_api = client.query_api()

    # p = Point("% of females ages 15-49 having comprehensive correct knowledge about HIV (2 prevent ways and reject 3 misconceptions)").tag("location", "Arab World").tag("country_code", "ARB").field("temperature",
    #                                                             25.3)
    # measurement = "poop"
    # tag_set = "location=location1,poop=hehe"
    # field_set = "temperature=25"
    # date_in_nano = str(int(datetime.datetime.utcnow().timestamp() * 1000000000))
    # p = f"{measurement},{tag_set} {field_set} {date_in_nano}"
    # write_api.write(bucket='123', record=p)
    return render_template("display.html", items = testr['buckets'])



@app.route('/submit', methods=["GET", "POST"])
def make_bucket():
    url = 'https://us-west-2-2.aws.cloud2.influxdata.com/api/v2/buckets'
    # r = requests.get('http://localhost:8086/api/v2/authorizations/', headers=headers)
    form = NameForm()
    if form.validate_on_submit() and request.method == "POST" and "name" in request.form:
        bucketName = request.form["name"]
        description = request.form["description"]
        domain = request.form["domain"]
        contributors = request.form["contributors"]
        reference = request.form["reference"]
        if request.form["contributors"] == "":
            contributors = "_none"
        if request.form["reference"] == "":
            reference = "_none"
        headers = {'Authorization': 'Token Urle4ZrRmKg_L1XG9BjzO_oBMc1zj-Fy84779erAppxBGUYgLMArHF_QnzgAPv_l0xiIRpXNwccYHm_eWGHjlg=='}
        payload = {
            "description": description,
            "name": bucketName,
            "orgID": "96172a9aa4f7cc00",
            "retentionRules": [
                {
                    "everySeconds": 86400,
                    "shardGroupDurationSeconds": 0,
                    "type": "expire"
                }
            ],
            "rp": "0",
            "schemaType": "implicit"
        }
        # payload = {
        #     "orgID": "96172a9aa4f7cc00",
        #     "name": "hihi",
        #     "description": "create a bucket",
        #     "rp": "myrp",
        #     "retentionRules": [
        #         {
        #             "type": "expire",
        #             "everySeconds": 86400
        #         }
        #     ]
        # }
        # print(bucketName)
        r = requests.post(url, headers=headers, json=payload)
        # print(r.text)
        measurement='_metadata'
        field_set='meta=1'
        tag_set = 'description='+description+',domain='+domain+',contributors='+contributors+",reference="+reference
        print(tag_set)
        p = f"{measurement},{tag_set} {field_set} "
        write_api.write(bucket=bucketName, record=p)
        print(tag_set)
    return render_template("submit.html", form=form)

# @app.route('/submit', methods=["GET", "POST"])
# def submit_time():
#     url = 'https://us-west-2-1.aws.cloud2.influxdata.com/api/v2/bucket'
#     headers = {'Authorization': 'Token R4KajLyAoKlFbzArRbpNy_5gQ4lEt5QW_cfREO59E_10nUKj44RmMr5-tBYwdYa4476KXMoCEvR9tYcDYdIxhw=='}
#     payload = {
#     "orgID": "96172a9aa4f7cc00",
#     "name": "mybucket",
#     "description": "create a bucket",
#     "rp": "myrp",
#     "retentionRules":[
#     {
#     "type": "expire",
#     "everySeconds": 86400
#     }
#     ]
#     }
#     # r = requests.get('http://localhost:8086/api/v2/authorizations/', headers=headers)
#     r = requests.post(url, headers=headers, json=payload)
#     form = RegisterForm()
#     if form.validate_on_submit() and request.method == "POST" and "username" in request.form:
#         username = request.form["username"]
#         password = hash_password(request.form["password"])
#         obj = {'username':username, 'password':password}
#         registerStuff = requests.post(f'http://{backAddr}:{backPort}/register', obj)
#         if registerStuff.status_code == 201:
#             flash("Registered! Now please log in.")
#             next = request.args.get("next")
#             if not is_safe_url(next):
#                 abort(400)
#             return redirect(next or url_for('login'))
#         else:
#             flash(registerStuff.text)
#     return render_template("register.html", form=form)

# @app.route('/upload', methods=["GET", "POST"])
# def get_data():
#     # data = request.files['file']
#     # print("hi")
#     bucket = "test"
#     # data = request.form
#     # data = dict(data)
#     # for value in range(5):
#     #     point = (
#     #         Point("measurement1")
#     #             .tag("tagname1", "tagvalue1")
#     #             .field("field1", value)
#     #     )
#     # write_api.write(bucket=bucket, org="jcsdavis@gmail.com", record=point)
#     # query_api = client.query_api()
#     #
#     # query = """from(bucket: "test2")
#     #  |> range(start: -525600m)
#     #  |> filter(fn: (r) => r._measurement == "measurement1")"""
#     # tables = query_api.query(query, org="jcsdavis@gmail.com")
#     #
#     # for table in tables:
#     #     for record in table.records:
#     #         print(record)
#     url = 'https://us-west-2-2.aws.cloud2.influxdata.com/api/v2/buckets'
#     headers = {'Authorization': 'Token Drle4ZrRmKg_L1XG9BjzO_oBMc1zj-Fy84779erAppxBGUYgLMArHF_QnzgAPv_l0xiIRpXNwccYHm_eWGHjlg=='}
#     r = requests.get(url, headers=headers)
#     testr = json.loads(r.text)
#     for i in testr['buckets']:
#         print(i['name'])
#     return "success"



@app.route('/postmethod', methods=["GET", "POST"])
def get_post_javascript_data():
    from win32api import GenerateConsoleCtrlEvent
    CTRL_C_EVENT = 0
    GenerateConsoleCtrlEvent(CTRL_C_EVENT, 0)
    # os._exit(0)
    # sys.exit()
    return "success"

@app.route('/info/<string:bucket>', methods=["GET", "POST"])
def info(bucket = None):
    query_api = client.query_api()
    tables = query_api.query(f'from(bucket: \"{bucket}\") |> range(start: -525600h) |> filter(fn: (r) => r._measurement == "_metadata")', org="jcsdavis@gmail.com")
    info = tables[0].records[0]
    stuff = []
    stuff.append(info['description'])
    stuff.append(info['domain'])
    if info['contributors'] != "_none":
        stuff.append(info['contributors'])
    if info['refrence'] != "_none":
        stuff.append(info['refrence'])
    # bucketName = request.form["name"]
    # description = request.form["description"]
    # domain = request.form["domain"]
    # contributors = request.form["contributors"]
    # reference = request.form["reference"]
    print(stuff)
    return render_template("info.html", items = stuff)



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