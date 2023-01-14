from application import app
from flask import render_template
from application.models import *
from application import tasks
from flask import send_from_directory, after_this_request
import os
# @app.route("/") 
# def welcome():
#     return render_template("index.html")


@app.route("/hello") 
def hello():
    # job = tasks.just_say_hello.delay("Viraj")
    job = tasks.just_say_hello.apply_async(countdown=10, expires=60) # countdown for 10 sec then print
    result = job.wait()
    return str(result),200


# download file and then remove it
@app.route("/<name>/download")
def downloadfile(name):
    @after_this_request
    def delete(response):
        path = os.getcwd()
        os.remove(path+"/static/{}".format(name))
        return response
    return send_from_directory('../static/',name,as_attachment=True)

