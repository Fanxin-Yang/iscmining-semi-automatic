import csv
import json
import os
from flask import request, current_app, send_file, send_from_directory
import pandas
from sklearn import tree, preprocessing
from sklearn.datasets import load_iris
import graphviz
import numpy
from sklearn.impute import SimpleImputer


# def exist_csv(filename, csv):
#     folder = os.path.join(
#         current_app.config['OUTPUT_FOLDER'], filename)
#     csv_folder = os.path.join(folder, csv)
#     csv_path = os.path.join(csv_folder, csv + '.csv')
#     if not os.path.exists(csv_path):
#         return False
#     else:
#         return csv_path


def exist_csv(filename, csv, level):
    folder = os.path.join(
        current_app.config['OUTPUT_FOLDER'], filename)
    if not level:
        csv_folder = os.path.join(folder, csv)
    else:
        csv_folder = os.path.join(folder, csv.rsplit("_", 1)[0])
    csv_path = os.path.join(csv_folder, csv + '.csv')
    if not os.path.exists(csv_path):
        return False
    else:
        return csv_path


def with_timestamps_level(csv):
    levels = ["Minutes", "Hours", "Days", "Months", "Years"]
    for l in levels:
        if csv.rsplit("_", 1)[1] == l:
            return csv.rsplit("_", 1)[1]
    return False


def get_events(filename, csv):
    level = with_timestamps_level(csv)
    csv_path = exist_csv(filename, csv, level)
    if not csv_path:
        return "No file found.", 404
    json_path = csv_path.rsplit(".", 1)[0] + '.json'
    data = pandas.read_csv(csv_path)
    # "records" -- The format of the JSON string [{column -> value}, … , {column -> value}]
    data.to_json(json_path, orient="records")
    return send_file(json_path, as_attachment=False), 200


def delete_event(filename, csv, eventIndex):
    csv_path = exist_csv(filename, csv, False)
    if not csv_path:
        return "No file found.", 404
    data = pandas.read_csv(csv_path)
    data.drop(eventIndex, axis=0, inplace=True)  # Raises error?
    data.reset_index(drop=True, inplace=True)
    data.drop(columns="No.", inplace=True)
    data.to_csv(csv_path, index_label="No.")  # without add an index column
    return "The chosen event from " + csv + ".csv has been successfully removed.", 200


def convert_level(level):
    if level == "T":
        return "Minutes"
    if level == "H":
        return "Hours"
    if level == "D":
        return "Days"
    if level == "M":
        return "Months"
    if level == "Y":
        return "Years"


def coarsen_timestamps(filename, csv):
    csv_path = exist_csv(filename, csv, False)
    if not csv_path:
        return "No file found.", 404
    levels = ["T", "H", "D", "M", "Y"]
    for level in levels:
        i = 0
        data = pandas.read_csv(csv_path)
        for i in range(0, data.get("time:timestamp").size):
            data.loc[i, "time:timestamp"] = pandas.Period(
                data.loc[i, "time:timestamp"], freq=level)
        csv_output_path = os.path.join(
            current_app.config['OUTPUT_FOLDER'], filename + '/' + csv + "/" + csv + '_' + convert_level(level) + '.csv')
        data.to_csv(csv_output_path, index=False)
    return None


def adapt_timestamps(filename, csv, level):
    coarsen_timestamps(filename, csv)
    return "Timestamps of events in " + csv + ".csv has been coarsened to " + level, 200


def get_algorithms():
    algorithms = {}
    algorithms[0] = "Decision Tree"
    algorithms[1] = "Logistic Regression"
    algorithms[2] = "Support Vector Machine"
    algorithms[3] = "Naive Bayes"
    algorithms[4] = "Stochastic Gradient Descent"
    algorithms[5] = "K-nearest Neighbor"
    algorithms[6] = "Random Forest"
    algorithms[7] = "Gradient Boosting Classifier"
    return algorithms, 200


def appy_algorithm(filename, csv, alg):
    level = with_timestamps_level(csv)
    csv_path = exist_csv(filename, csv, level)
    if not csv_path:
        return "No file found.", 404
    data = pandas.read_csv(csv_path)
    data.dropna(inplace=True)
    # data_convert = data.astype({"time:timestamp": "datetime64"})
    enc = preprocessing.OrdinalEncoder(
        handle_unknown='use_encoded_value', unknown_value=0)
    X = data.drop(["No.", "case:concept:name",
                   "org:resource", "concept:name", "time:timestamp"], axis=1)
    y = data["concept:name"]
    # Imputation of missing values https://scikit-learn.org/stable/modules/impute.html
    imp = SimpleImputer(strategy="constant", fill_value=0)
    X_out = imp.fit_transform(X)
    for type in X.dtypes:
        if type == object:
            enc = preprocessing.OneHotEncoder(sparse=False)
            X_out = enc.fit_transform(X_out)
            break
    clf = tree.DecisionTreeClassifier(
        criterion="gini", splitter="random", min_samples_leaf=3)
    clf = clf.fit(X_out, y)
    dot_data = tree.export_graphviz(
        clf, out_file=None, filled=True, rounded=True,
        special_characters=True, feature_names=enc.get_feature_names_out(input_features=X.columns), class_names=y.unique())
    graph = graphviz.Source(dot_data)
    graph.render(csv + "_" + alg, "results/" + filename, format="png")

    # X_tr = enc.inverse_transform(X_out)
    # print(X)
    # print("line")
    # print(X_out)
    # print("line")
    # print(X_tr)
    return "result", 200

    # append ISC candidates
