from flask import Flask, flash, request, send_from_directory
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
from pm4py.objects.log.importer.xes import importer as xes_importer
import pm4py
import projection_transformation_algorithm
import discovery_algorithm
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
app.add_url_rule('/discovery/<filename>/<csv>/<string:level>',
                 methods=['PUT'],
                 view_func=discovery_algorithm.adapt_timestamps)
app.add_url_rule('/discovery', view_func=discovery_algorithm.get_algorithms)
app.add_url_rule('/discovery/<filename>/<csv>/<string:alg>',
                 methods=['GET'],
                 view_func=discovery_algorithm.appy_algorithm)
app.add_url_rule('/decisiontree/<filename>/<csv>',
                 methods=['GET'],
                 view_func=discovery_algorithm.get_decisiontree)


@app.route('/', methods=['GET'])
def greetings():
    return ('Main Page')


@app.route('/processmodel/<filename>', methods=['GET'])
def get_processmodel(filename):
    if not os.path.exists(app.config['GRAPH_FOLDER']):
                os.makedirs(app.config['GRAPH_FOLDER'])
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename + ".xes")
    bpmn_path = os.path.join(app.config['GRAPH_FOLDER'], filename + ".bpmn")
             # (must be one of ['bmp', 'canon', 'cgimage', 'cmap', 'cmapx', 'cmapx_np', 'dot', 'dot_json', 'eps', 'exr', 'fig', 'gd', 'gd2', 'gif', 'gtk', 'gv', 'ico', 'imap', 'imap_np', 'ismap', 'jp2', 'jpe', 'jpeg', 'jpg', 'json', 'json0', 'pct', 'pdf', 'pic', 'pict', 'plain', 'plain-ext', 'png', 'pov', 'ps', 'ps2', 'psd', 'sgi', 'svg', 'svgz', 'tga', 'tif', 'tiff', 'tk', 'vml', 'vmlz', 'vrml', 'wbmp', 'webp', 'x11', 'xdot', 'xdot1.2', 'xdot1.4', 'xdot_json', 'xlib'])
            # vis_path = os.path.join(app.config['GRAPH_FOLDER'],
            #                         filename.rsplit('.', 1)[0].lower() + ".png")
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
    # Filtering activities/paths
    dfg, sa, ea = pm4py.discover_directly_follows_graph(log)
    activities_count = pm4py.get_event_attribute_values(log, "concept:name")
    dfg, sa, ea, activities_count = dfg_filtering.filter_dfg_on_paths_percentage(dfg, sa, ea, activities_count, perc)
    filtered_log = pm4py.play_out(dfg, sa, ea)
    tree = pm4py.discover_bpmn_inductive(filtered_log)
    pm4py.write_bpmn(tree, bpmn_path)
    return


@app.route('/pm4pytest', methods=['GET'])
def pm4pytest():
    filename = 'loan_process.xes'
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(app.config['GRAPH_FOLDER']):
                os.makedirs(app.config['GRAPH_FOLDER'])
    bpmn_path = os.path.join(app.config['GRAPH_FOLDER'],
                             filename.rsplit('.', 1)[0].lower() + ".bpmn")
    # (must be one of ['bmp', 'canon', 'cgimage', 'cmap', 'cmapx', 'cmapx_np', 'dot', 'dot_json', 'eps', 'exr', 'fig', 'gd', 'gd2', 'gif', 'gtk', 'gv', 'ico', 'imap', 'imap_np', 'ismap', 'jp2', 'jpe', 'jpeg', 'jpg', 'json', 'json0', 'pct', 'pdf', 'pic', 'pict', 'plain', 'plain-ext', 'png', 'pov', 'ps', 'ps2', 'psd', 'sgi', 'svg', 'svgz', 'tga', 'tif', 'tiff', 'tk', 'vml', 'vmlz', 'vrml', 'wbmp', 'webp', 'x11', 'xdot', 'xdot1.2', 'xdot1.4', 'xdot_json', 'xlib'])
    vis_path = os.path.join(app.config['GRAPH_FOLDER'],
                            filename.rsplit('.', 1)[0].lower() + ".png")
    # net, initial_marking, final_marking = mining_process_model(file_path)
    # pm4py.write_petri_net(net, initial_marking, final_marking, pnml_path)
    # pm4py.save_vis_petri_net(net, initial_marking, final_marking, vis_path)
    log = xes_importer.apply(file_path)

    # Filtering activities/paths
    dfg, sa, ea = pm4py.discover_directly_follows_graph(log)
    activities_count = pm4py.get_event_attribute_values(log, "concept:name")
    args = request.args.copy()
    perc = float(args.pop("perc", 1))
    dfg, sa, ea, activities_count = dfg_filtering.filter_dfg_on_paths_percentage(dfg, sa, ea, activities_count, perc)
    # dfg, sa, ea, activities_count = dfg_filtering.filter_dfg_on_activities_percentage(dfg, sa, ea, activities_count, perc)
    filtered_log = pm4py.play_out(dfg, sa, ea)
    print(sa)
    print(ea)
    print(activities_count)

    tree = pm4py.discover_bpmn_inductive(filtered_log)
    pm4py.write_bpmn(tree, bpmn_path)
    pm4py.save_vis_bpmn(tree, vis_path)
    # graphviz.render('dot', 'png', vis_path).replace('\\', '/')
    return send_from_directory(app.config['GRAPH_FOLDER'], 'loan_process.png')


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

# python3 app.py
if __name__ == "__main__":
    app.run(host="::1", port=8050, debug=True)

# flask run (default at http://127.0.0.1:5000)
# flask run --host=::1 --port=8050