from flask import Flask, flash, request, send_from_directory
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
from pm4py.objects.log.importer.xes import importer as xes_importer
import pm4py
import graphviz
import projection_transformation_algorithm
import discovery_algorithm

UPLOAD_FOLDER = "./uploads"
OUTPUT_FOLDER = "./outputs"
GRAPH_FOLDER = "./processmodels"
RESULTS_FOLDER = "./results"
ALLOWED_EXTENSIONS = {"xes"}
app = Flask(__name__)
# The secret key will change after each start, and incalidate any signed cookies.
# So for now just set a random secret key
# secret = secrets.token_urlsafe(32)
# app.secret_key = secret
app.secret_key = "secret_key#!"

app.config.from_object(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['GRAPH_FOLDER'] = GRAPH_FOLDER
app.config['RESULTS_FOLDER'] = RESULTS_FOLDER
CORS(app, resources={r"/*": {'origins': "*"}})

# Centralized URL Map
# https://flask.palletsprojects.com/en/1.1.x/patterns/lazyloading/converting-to-centralized-url-map
app.add_url_rule('/projection_transformation/<filename>',
                 view_func=projection_transformation_algorithm.get_attributes)
app.add_url_rule('/projection_transformation/<filename>/<att>',
                 view_func=projection_transformation_algorithm.projection_transformation)
app.add_url_rule('/discovery/<filename>/<csv>',
                 view_func=discovery_algorithm.get_events)
app.add_url_rule('/discovery/<filename>/<csv>/<int:eventIndex>',
                 methods=['DELETE'],
                 view_func=discovery_algorithm.delete_event)
app.add_url_rule('/discovery/<filename>/<csv>/<string:level>',
                 methods=['PUT'],
                 view_func=discovery_algorithm.adapt_timestamps)
app.add_url_rule('/discovery',
                 view_func=discovery_algorithm.get_algorithms)
app.add_url_rule('/discovery/<filename>/<csv>/<string:alg>',
                 methods=['GET'],
                 view_func=discovery_algorithm.appy_algorithm)
app.add_url_rule('/decisiontree/<filename>/<csv>', methods=['GET'],
                 view_func=discovery_algorithm.get_decisiontree)


@app.route('/', methods=['GET'])
def greetings():
    return('Main Page')


@app.route('/processmodels/<name>', methods=['GET'])
def get_processmodels(name):
    return send_from_directory(app.config['GRAPH_FOLDER'], name)
    return send_from_directory(app.config['GRAPH_FOLDER'], name, as_attachment=True)


# check if the filname inculde "." and the suffix of it is allowed


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def mining_process_model(file_path):
    log = xes_importer.apply(file_path)
    bpmn_model = pm4py.discover_bpmn_inductive(log)
    gviz_model = pm4py.visualization.bpmn.visualizer.apply(
        bpmn_model)
    return gviz_model


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return "No file uploaded. Please select a file.", 400
        file = request.files['file']
        # If the user does not select a file, the browser submits an empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return"No file is selected.", 400
            # return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            processModel = mining_process_model(file_path)
            graph_path = os.path.join(app.config['GRAPH_FOLDER'], filename.rsplit('.', 1)[
                                      0].lower()+".gv")
            # pm4py.visualization.bpmn.visualizer.save(processModel, graph_path)
            processModel.save(graph_path)
            graphviz.render('dot', 'png', graph_path).replace('\\', '/')
            graph_path + '.png'
            return filename.rsplit('.', 1)[0].lower(), "The file has been successfully uploaded."
        else:
            return "This file type is not allowed. Please select a XES file.", 406
    else:
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
            return "no file uploaded yet", 404
        dataSets = os.listdir(app.config['UPLOAD_FOLDER'])
        if len(dataSets) == 0:
            return "no file uploaded yet", 404
        dataSets_dict = {}
        i = 0
        for dataSet in dataSets:
            dataSets_dict[i] = dataSet
            i += 1
        return dataSets_dict, 200


if __name__ == "__main__":
    app.run(debug=True)
