from flask import Flask
from markupsafe import escape
from flask import render_template
from flask import request
import requests as req
import json
import ast
import time

app = Flask(__name__)

@app.route("/activate/")
def activate():
    return render_template('activate.html')

@app.route("/form", methods=["POST"])
def form():
    username = request.form.get("username")
    password = request.form.get("password")
    address = request.form.get("ip")

    url = "https://10.145.72.133/mgmt/shared/authn/login"
    data = {"username": username, "password": password}
    r = req.post(url, json=data, verify=False)
    parsed = json.loads(r.content)
    token = parsed["token"]["token"]


    s = req.Session()
    s.headers.update({"X-F5-Auth-Token": token})

    url = "https://10.145.72.133/mgmt/cm/device/tasks/licensing/pool/member-management"
    data = {"licensePoolName":"test", 
            "command":"assign", 
            "address":address, 
            "user": username, 
            "password":password}

    r = s.post(url, json=data, verify=False)

    return token
