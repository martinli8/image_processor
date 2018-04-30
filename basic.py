import datetime
import models
from flask import Flask, jsonify, request
from flask_cors import CORS
from main import *

app = Flask(__name__)
CORS(app)


@app.route("/api/post_image", methods=["POST"])
def userCreation():

    userCreationFlag = True
    print("HERE0")
    try:
        r = request.get_json()
        user_email = r["user_email"]
        user_picture = r["picture64bit"]
        process_requested = r["process_requested"]
    except:
        return 'Input data error! Make sure you have correct data formats'

    upload_time = datetime.datetime.now()
    print("HERE1")

    try:
        print(process_requested)
        add_user_data(user_email, user_picture, process_requested,
                      upload_time)
        userCreationFlag = False
    except:
        create_user(user_email, user_picture, process_requested,
                    upload_time)
        userCreationFlag = True
    print("HERE2")
    print(process_requested)
    print("HERE3")
    encodedResult = process_image(user_email, process_requested, user_picture)

    if userCreationFlag is True:
        return "User Created"
    else:
        return "User already exists, data appended"


@app.route("/api/<user_email>", methods=["GET"])
def getInfo(user_email):
    userJson = return_metadata(user_email)
    return jsonify(userJson)
#
# @app.route("/api/latest/<user_email>", methods=
