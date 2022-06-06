# This script re-implements the projection and transformation algorithm based on the project https://github.com/WinterKaro/iscmining-edoc17
# The algorithm is presented in the Paper "Discovering Instance-Spanning Constraints from Process Execution Logs based on Classification Techniques" by Karolin Winter and Stefanie Rinderle-Ma (https://ieeexplore.ieee.org/document/8089866).
# It takes one *.xes file and an event attribute as input and produces one or several *.arff files.
# The event attribute is used for dimension reduction, e.g. if there is more than one organizational resource (org:resource) in the log file, then one *.arff file per resource is produced. Otherwise the whole log is transferred into one *.arff file.


# @app.route('/projection_transformation/<path:name>', methods=['GET'])
import os
import pandas
from flask import request, current_app
from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.objects.conversion.log import converter as log_converter
from sympy import false


def convert(type):
    if type == "string":
        return "STRING"
    if type == "date":
        return 'DATE "yyyy-MM-dd\'T\'HH:mm:ss.SSSZ"'
    if type == "float":
        return "NUMERIC"
    if type == "int":
        return "NUMERIC"
    if type == "boolean":
        return "STRING"
    return type


def exist_file(filename):
    input_path = os.path.join(
        current_app.config['UPLOAD_FOLDER'], filename + '.xes')
    if not os.path.exists(input_path):
        return false
    else:
        return input_path


def get_attributes(filename):
    print(request)
    attributes = {"org:resource", "concept:name"}
    input_path = exist_file(filename)
    if input_path == false:
        return "No file found.", 404
    log = xes_importer.apply(input_path)
    # variant = xes_importer.Variants.ITERPARSE
    # parameters = {variant.value.Parameters.TIMESTAMP_SORT: True}
    # log = xes_importer.apply(
    #     input_path, variant=variant, parameters=parameters)
    # https://pm4py.fit.fraunhofer.de/static/assets/api/2.1.0/pm4py.objects.log.html?highlight=eventlog#pm4py.objects.log.log.EventLog
    # print(log.classifiers, log.attributes)
    i = 0
    for trace in log:
        for event in trace:
            for att in event:
                if att not in attributes:
                    attributes.add(att)
    attributes_dict = {}
    for att in attributes:
        attributes_dict[i] = att
        i += 1
    return attributes_dict, 200


def projection_transformation(filename, att):
    print(request)
    input_path = exist_file(filename)
    if input_path == false:
        return "No file found.", 404
    # check if att is contained in the file?
    log = xes_importer.apply(input_path)
    output_path = os.path.join(current_app.config['OUTPUT_FOLDER'])

    dataframe = log_converter.apply(
        log, variant=log_converter.Variants.TO_DATA_FRAME)
    dataframe.to_csv("attribute_value.csv")

    # print(log[0][0]['concept:name'])
    # return send_from_directory(app.config['GRAPH_FOLDER'], name, as_attachment=True)
    return "yes", 200
