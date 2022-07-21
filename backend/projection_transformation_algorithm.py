# This script re-implements the projection and transformation algorithm based on the project https://github.com/WinterKaro/iscmining-edoc17
# The algorithm is presented in the Paper "Discovering Instance-Spanning Constraints from Process Execution Logs based on Classification Techniques" by Karolin Winter and Stefanie Rinderle-Ma (https://ieeexplore.ieee.org/document/8089866).
# It takes one *.xes file and an event attribute as input and produces one or several *.arff files.
# The event attribute is used for dimension reduction, e.g. if there is more than one organizational resource (org:resource) in the log file, then one *.arff file per resource is produced. Otherwise the whole log is transferred into one *.arff file.


import os
from flask import request, current_app
import pm4py

def exist_file(filename):
    input_path = os.path.join(
        current_app.config['UPLOAD_FOLDER'], filename + '.xes')
    if not os.path.exists(input_path):
        return False
    else:
        return input_path


def get_attributes(filename):
    attributes = {"org:resource", "concept:name"}
    input_path = exist_file(filename)
    if input_path == False:
        return "No file found.", 404
    log = pm4py.read_xes(input_path)
    # variant = xes_importer.Variants.ITERPARSE
    # parameters = {variant.value.Parameters.TIMESTAMP_SORT: True}
    # https://pm4py.fit.fraunhofer.de/static/assets/api/2.1.0/pm4py.objects.log.html?highlight=eventlog#pm4py.objects.log.log.EventLog
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
    input_path = exist_file(filename)
    if not input_path:
        return "No file found.", 404
    # check if att is contained in the file?
    log = pm4py.read_xes(input_path)  
    # values: all attribute values of selected attribute and the number each of them occur
    attValues = pm4py.get_event_attribute_values(log, att)

    if not os.path.exists("outputs/" + filename):
        os.makedirs("outputs/" + filename)
    for key in attValues.keys():
        filterLog = pm4py.filter_event_attribute_values(log, att, [key], level="case", retain=True)
        dataframe = pm4py.convert_to_dataframe(filterLog)
        if not os.path.exists("outputs/" + filename + "/" + str(key)):
            os.makedirs("outputs/" + filename + "/" + str(key))
        output_path = os.path.join(
            current_app.config['OUTPUT_FOLDER'], filename + "/" + str(key) + "/" + str(key) + ".csv")
        dataframe.to_csv(output_path, index_label="No.")
    return attValues, 200
