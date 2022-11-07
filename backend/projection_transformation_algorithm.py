# This script re-implements the projection and transformation algorithm based on the project https://github.com/WinterKaro/iscmining-edoc17
# The algorithm is presented in the Paper "Discovering Instance-Spanning Constraints from Process Execution Logs based on Classification Techniques" by Karolin Winter and Stefanie Rinderle-Ma (https://ieeexplore.ieee.org/document/8089866).
# It takes one *.xes file and an event attribute as input and produces one or several *.arff files.
# The event attribute is used for dimension reduction, e.g. if there is more than one organizational resource (org:resource) in the log file, then one *.arff file per resource is produced. Otherwise the whole log is transferred into one *.arff file.


import os
from flask import current_app
import pm4py
import pandas


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
    df = pm4py.convert_to_dataframe(log)
    df.dropna(axis=0, subset=att, inplace=True)
    # values: all attribute values of selected attribute and the number each of them occur
    attValues = pm4py.get_event_attribute_values(df, att)
    if not os.path.exists("outputs/" + filename):
        os.makedirs("outputs/" + filename)
    attValuesDict = {}
    i = 0
    for key in attValues.keys():
        filteredDf = pm4py.filter_event_attribute_values(
            df, att, [key], level="event", retain=True)
        filteredDf = pandas.DataFrame(filteredDf)
        # Remove the coloum is it is all NaN
        filteredDf.dropna(axis=1, how="all", inplace=True)
        filteredDf.reset_index(drop=True, inplace=True)  # type: ignore
        key_name = str(key).replace(" ", "_")
        if not os.path.exists("outputs/" + filename + "/" + key_name):
            os.makedirs("outputs/" + filename + "/" + key_name)
        output_path = os.path.join(
            current_app.config['OUTPUT_FOLDER'], filename + "/" + key_name + "/" + key_name + ".csv")
        filteredDf.to_csv(output_path, index_label="No.")
        output_path_arff = os.path.join(
            current_app.config['OUTPUT_FOLDER'], filename + "/" + key_name + "/" + key_name + ".arff")
        filteredDf.drop(["case:concept:name"], axis=1, inplace=True)
        # csv2arff(output_path, output_path_arff)
        df2arff(filteredDf, output_path_arff, key)
        attValuesDict[i] = key
        i += 1
    return attValuesDict, 200


def csv2arff(csv_path, output_path_arff):
    return "csv2arff"


def df2arff(df, output_path_arff, key):
    print(
        f"------------------------{output_path_arff}------------------------")
    with open(output_path_arff, "w+") as arff:
        arff.write("@RELATION " + key + "\n")
        for att in df:
            if df[att].dtype == "object":
                if len(df[att].unique()) == 1:
                    arff.write(f'@ATTRIBUTE "{att}" STRING\n')
                else:
                    arff.write(
                        f'@ATTRIBUTE "{att}" {str(set(df[att].unique()))}\n')
            elif df[att].dtype == "int64" or df[att].dtype == "float64":
                arff.write(f'@ATTRIBUTE "{att}" NUMERIC\n')
            elif type(df[att].dtype) == pandas.core.dtypes.dtypes.DatetimeTZDtype:
                timestamps = df[att].unique()
                timestamps_set = set(timestamps)
                format_timestamps_set = {tt.isoformat()
                                         for tt in timestamps_set}
                # Return the time formatted according to ISO 8610.
                arff.write(
                    f'@ATTRIBUTE "{att}" {str(format_timestamps_set)}\n')
        arff.write("@DATA\n")
        for event in df.values:
            line = ""
            for i in range(df.shape[1]):
                if str(event[i]) == "nan":
                    # use ? for missing value
                    line += '?'
                elif type(event[i]) == pandas._libs.tslibs.timestamps.Timestamp:
                    line += f'"{event[i].isoformat()}"'
                elif type(event[i]) == int or type(event[i]) == float:
                    line += str(event[i])
                else:
                    line += f'"{event[i]}"'
                if i != df.shape[1] - 1:
                    line += ', '
            line += '\n'
            arff.write(line)
    return "df2arff"


def merge(filename, projection):
    logs = filename.split("&")
    projections = projection.split("&")
    df = pandas.DataFrame()
    for i in logs:
        for j in projections:
            input_path = os.path.join(
                current_app.config['OUTPUT_FOLDER'], i + "/" + j + "/" + j + ".csv")
            if os.path.exists(input_path):
                tmp = pandas.read_csv(input_path, index_col="No.")
                if df.size == 0:
                    df = pandas.concat(
                        [df, tmp], join="outer", ignore_index=True)
                else:
                    df = pandas.concat(
                        [df, tmp], join="inner", ignore_index=True)
    output_path = os.path.join(
        current_app.config['OUTPUT_FOLDER'], filename + "_" + projection + ".csv")
    df.to_csv(output_path, index_label="No.")
    return "Merged csv file has been saved."
