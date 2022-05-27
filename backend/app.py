from flask import Flask, abort, jsonify, flash, make_response, request, redirect, url_for
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
from pm4py.objects.log.importer.xes import importer as xes_importer
import pm4py

UPLOAD_FOLDER = "./uploads"
ALLOWED_EXTENSIONS = {"xes"}
app = Flask(__name__)
# The secret key will change after each start, and incalidate any signed cookies.
# So for now just set a random secret key
# secret = secrets.token_urlsafe(32)
# app.secret_key = secret
app.secret_key = "secret_key#!"

app.config.from_object(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app, resources={r"/*": {'origins': "*"}})


@app.route('/', methods=['GET'])
def greetings():
    return('Main Page')

# check if the filname inculde "." and the suffix of it is allowed


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def mining_pmodel(file_path):
    log = xes_importer.apply(file_path)
    print(log[0])  # prints the first trace of the log
    print(log[0][0])  # prints the first event of the first trace
    bpmn_model = pm4py.discover_bpmn_inductive(log)
    # gviz_model = pm4py.visualization.bpmn.visualizer.apply(
    #     bpmn_model)
    # print(gviz_model)
    pm4py.view_bpmn(bpmn_model)
    return


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        print(request)
        # check if the post request has the file part
        if 'file' not in request.files:
            print('No file part')
            return "No file uploaded. Please select a file.", 400
            # return redirect(request.url)
        file = request.files['file']
        print(file)
        # If the user does not select a file, the browser submits an empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return"No file is selected.", 400
            # return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print(filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            pmodel = mining_pmodel(file_path)
            # print((url_for('download_file', name=filename)))
            # return redirect(url_for('download_file', name=filename))
            return "The file has been successfully uploaded.", 200
        else:
            print("not allowed type")
            return "This file type is not allowed. Please select a XES file.", 406
            # return redirect(request.url)
    else:
        return ("Upload a new dataset")


if __name__ == "__main__":
    app.run(debug=True)
