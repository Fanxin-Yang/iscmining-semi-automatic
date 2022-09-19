from flask import Flask, flash, request, send_from_directory
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
from pm4py.objects.log.importer.xes import importer as xes_importer
import pm4py, pandas
import projection_transformation_algorithm, discovery_algorithm, classification
from pm4py.algo.filtering.dfg import dfg_filtering

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
app.add_url_rule(
    '/projection_transformation/<filename>/<att>',
    view_func=projection_transformation_algorithm.projection_transformation)
app.add_url_rule('/discovery/<filename>/<csv>',
                 view_func=discovery_algorithm.get_events)
app.add_url_rule('/discovery/<filename>/<csv>/<int:eventIndex>',
                 methods=['DELETE'],
                 view_func=discovery_algorithm.delete_event)
app.add_url_rule('/filter/<filename>/<csv>',
                 view_func=discovery_algorithm.get_variants)
app.add_url_rule('/modify/<filename>/<csv>/<string:level>',
                 view_func=discovery_algorithm.modify)
app.add_url_rule('/classification', view_func=classification.get_algorithms)
app.add_url_rule('/classification/<filename>/<csv>/<string:alg>',
                 methods=['GET'],
                 view_func=classification.appy_algorithm)
app.add_url_rule('/decisiontree/<filename>/<csv>',
                 methods=['GET'],
                 view_func=classification.get_decisiontree)

@app.route('/', methods=['GET'])
def greetings():
    return ('Main Page')


@app.route('/processmodel/<filename>', methods=['GET'])
def get_processmodel(filename):
    if not os.path.exists(app.config['GRAPH_FOLDER']):
                os.makedirs(app.config['GRAPH_FOLDER'])
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename + ".xes")
    bpmn_path = os.path.join(app.config['GRAPH_FOLDER'], filename + ".bpmn")
    args = request.args.copy()
    perc = float(args.pop("perc", 1))
    mining_process_model(file_path, bpmn_path, perc)
    return send_from_directory(app.config['GRAPH_FOLDER'], filename + ".bpmn")


# check if the filname inculde "." and the suffix of it is allowed
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def mining_process_model(file_path, bpmn_path, perc):
    log = xes_importer.apply(file_path)
    dfg, sa, ea = pm4py.discover_directly_follows_graph(log)
    activities_count = pm4py.get_event_attribute_values(log, "concept:name")
    # filtering on the paths percentage
    dfg, sa, ea, activities_count = dfg_filtering.filter_dfg_on_paths_percentage(dfg, sa, ea, activities_count, perc)
    filtered_log = pm4py.play_out(dfg, sa, ea)
    tree = pm4py.discover_bpmn_inductive(filtered_log)
    pm4py.write_bpmn(tree, bpmn_path)
    return
    

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
            return "No file is selected.", 400
            # return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            return filename.rsplit(
                '.', 1)[0].lower(), "The file has been successfully uploaded."
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

@app.route('/summary/<filename>/<csv>', methods=['GET'])
def summary(filename, csv):
    csv_path = discovery_algorithm.exist_csv(filename, csv)
    if not csv_path:
        return "No file found.", 404
    csv_modified_path = discovery_algorithm.exist_csv(filename, csv + "_modified")
    partial_log = pandas.read_csv(csv_path)
    events_sum = partial_log.shape[0]
    variants_sum = len(pm4py.get_variants_as_tuples(partial_log))
    cases_sum = len(partial_log["case:concept:name"].unique())
    if not csv_modified_path:
        summary = {}
        summary["variants"] = [variants_sum, variants_sum]
        summary["cases"] = [cases_sum, cases_sum]
        summary["events"] = [events_sum, events_sum]
    else:
        partial_log_modified = pandas.read_csv(csv_modified_path)
        events = partial_log_modified.shape[0]
        variants = len(pm4py.get_variants_as_tuples(partial_log_modified))
        cases = len(partial_log_modified["case:concept:name"].unique())
        summary = {}
        summary["variants"] = [variants, variants_sum]
        summary["cases"] = [cases, cases_sum]
        summary["events"] = [events, events_sum]
    return summary, 200

# python3 app.py
if __name__ == "__main__":
    app.run(host="::1", port=8050, debug=True)

# flask run (default at http://127.0.0.1:5000)
# flask run --host=::1 --port=8050