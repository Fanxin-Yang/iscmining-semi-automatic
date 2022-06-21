import csv
import json
import os
from flask import request, current_app, send_from_directory
import pandas
from sklearn import tree


def exist_csv(filename, csv):
    csv_path = os.path.join(
        current_app.config['OUTPUT_FOLDER'], filename + '/' + csv + '.csv')
    if not os.path.exists(csv_path):
        return False
    else:
        return csv_path


def get_events(filename, csv):
    csv_path = exist_csv(filename, csv)
    if not csv_path:
        return "No file found.", 404
    json_path = os.path.join(
        current_app.config['OUTPUT_FOLDER'], filename + '/' + csv + '.json')
    data = pandas.read_csv(csv_path)
    # "records" -- The format of the JSON string [{column -> value}, … , {column -> value}]
    data.to_json(json_path, orient="records")
    return send_from_directory(os.path.join(
        current_app.config['OUTPUT_FOLDER'], filename + '/'), csv.rsplit('.', 1)[0] + '.json', as_attachment=False), 200


def delete_event(filename, csv, eventIndex):
    csv_path = exist_csv(filename, csv)
    if not csv_path:
        return "No file found.", 404
    data = pandas.read_csv(csv_path)
    data.drop(eventIndex, axis=0, inplace=True)  # Raises error?
    data.reset_index(drop=True, inplace=True)
    data.drop(columns="No.", inplace=True)
    data.to_csv(csv_path, index_label="No.")  # without add an index column
    return "The " + str(eventIndex) + " event from " + csv + ".csv has been successfully removed.", 200


def adapt_timestamps(filename, csv, level):
    csv_path = exist_csv(filename, csv)
    if not csv_path:
        return "No file found.", 404
    data = pandas.read_csv(csv_path)
    i = 0
    if level == "Seconds":
        csv_output_path = csv_path
    else:
        if level == "Minutes":
            for i in range(0, data.get("time:timestamp").size):
                data.loc[i, "time:timestamp"] = pandas.Period(
                    data.loc[i, "time:timestamp"], freq="T")
        if level == "Hours":
            for i in range(0, data.get("time:timestamp").size):
                data.loc[i, "time:timestamp"] = pandas.Period(
                    data.loc[i, "time:timestamp"], freq="H")
        if level == "Days":
            for i in range(0, data.get("time:timestamp").size):
                data.loc[i, "time:timestamp"] = pandas.Period(
                    data.loc[i, "time:timestamp"], freq="D")
        if level == "Months":
            for i in range(0, data.get("time:timestamp").size):
                data.loc[i, "time:timestamp"] = pandas.Period(
                    data.loc[i, "time:timestamp"], freq="M")
        if level == "Years":
            for i in range(0, data.get("time:timestamp").size):
                data.loc[i, "time:timestamp"] = pandas.Period(
                    data.loc[i, "time:timestamp"], freq="Y")
        csv_output_path = os.path.join(
            current_app.config['OUTPUT_FOLDER'], filename + '/' + csv + '_' + level + '.csv')
    data.to_csv(csv_output_path, index=False)
    return "Timestamps of events in " + csv + ".csv has been coarsened to " + level, 200


def get_algorithms():
    algorithms = {}
    algorithms[0] = "Decision Trees"
    return algorithms, 200


def appy_algorithm(filename, csv, alg):
    print(csv)
    csv_path = exist_csv(filename, csv)
    if not csv_path:
        return "No file found.", 404
    data = pandas.read_csv(csv_path)
    X, y = data.data, data.target
    if alg == "decisiontrees":
        clf = tree.DecisionTreeClassifier()
        clf = clf.fit(X, y)
    return "result", 200

# append ISC candidates
