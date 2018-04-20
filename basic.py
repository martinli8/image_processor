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

    try:
        r = request.get_json()
        user_email = r["user_email"]
        user_picture = r["picture64bit"]
        process_requested = r["process_requested"]
        image_size = r["image_size"]
    except:
        return 'Input data error! Make sure you have correct data formats'

    upload_time = datetime.datetime.now()

    try:
        add_user_data(user_email, user_picture, process_requested,
                      upload_time, image_size)
        userCreationFlag = False
    except:
        create_user(user_email, user_picture, process_requested,
                    upload_time, image_size)
        userCreationFlag = True

    if process_requested is "histogram_eq":
        process_duration = histogram_eq()[0]
        pass

    if process_requested is "contrast_stretching":
        process_duration = contrast_stretching()[0]
        pass

    if process_requested is "log_compression":
        process_duration = log_compression()[0]
        pass

    if process_requested is "reverse_video":
        process_duration = reverse_video()[0]
        pass

    if process_requested is "other":
        process_duration = other()[0]
        pass

    process_duration = 3
    write_duration_time(user_email, process_duration)

    if userCreationFlag is True:
        return "User Created"
    else:
        return "User already exists, data appended"


@app.route("/api/<user_email>", methods=["GET"])
def getInfo(user_email):
    userJson = return_metadata(user_email)
    return jsonify(userJson)
