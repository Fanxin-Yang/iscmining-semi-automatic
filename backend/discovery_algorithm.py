import csv
import json
import os
from flask import request, current_app, send_file, send_from_directory
import matplotlib
import pandas
from sklearn import tree, preprocessing
from sklearn.datasets import load_iris
import graphviz
import numpy
from sklearn.impute import SimpleImputer
from dtreeviz.trees import dtreeviz
# from sklearn import datasets
# from sklearn.datasets import load_iris, load_boston


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
    dataset = pandas.read_csv(csv_path)
    # "records" -- The format of the JSON string [{column -> value}, … , {column -> value}]
    dataset.to_json(json_path, orient="records")
    return send_file(json_path, as_attachment=False), 200


def delete_event(filename, csv, eventIndex):
    csv_path = exist_csv(filename, csv, False)
    if not csv_path:
        return "No file found.", 404
    dataset = pandas.read_csv(csv_path)
    dataset.drop(eventIndex, axis=0, inplace=True)  # Raises error?
    dataset.reset_index(drop=True, inplace=True)
    dataset.drop(columns="No.", inplace=True)
    dataset.to_csv(csv_path, index_label="No.")  # without add an index column
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
        dataset = pandas.read_csv(csv_path)
        for i in range(0, dataset.get("time:timestamp").size):
            dataset.loc[i, "time:timestamp"] = pandas.Period(
                dataset.loc[i, "time:timestamp"], freq=level)
        csv_output_path = os.path.join(
            current_app.config['OUTPUT_FOLDER'], filename + '/' + csv + "/" + csv + '_' + convert_level(level) + '.csv')
        dataset.to_csv(csv_output_path, index=False)
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
    label = request.args.get("selectedLabel", "")
    samples = request.args.get("selectedSamples", "").split(",")
    level = with_timestamps_level(csv)
    csv_path = exist_csv(filename, csv, level)
    if not csv_path:
        return "No file found.", 404
    dataset = pandas.read_csv(csv_path)
    # dataset_convert = dataset.astype({"time:timestamp": "datetime64"})
    dataset_new = dataset[samples].assign(label=dataset[label])
    dataset_new.dropna(inplace=True)
    X = dataset_new[samples]
    y = dataset_new["label"]
    # Imputation of missing values https://scikit-learn.org/stable/modules/impute.html
    imp = SimpleImputer(strategy="constant", fill_value=-1)
    data = imp.fit_transform(X)
    feature_names = list(X.columns)
    for type in X.dtypes:
        if type == object:
            encoderX = preprocessing.OrdinalEncoder(
                handle_unknown='use_encoded_value', unknown_value=-1)
            # encoderX = preprocessing.OneHotEncoder(sparse=False)
            data = encoderX.fit_transform(data)
            feature_names = encoderX.get_feature_names_out(
                input_features=X.columns)
            break

    encodery = preprocessing.OrdinalEncoder(
        handle_unknown='use_encoded_value', unknown_value=-1)
    target = y
    if y.dtype == object:
        target = encodery.fit_transform(
            y.values.reshape(-1, 1)).reshape(1, -1)[0]
    target_names = y.unique()

    # not worth the higher training time for entropy criterion
    clf = tree.DecisionTreeClassifier(
        criterion="gini", splitter="random", min_samples_leaf=3)
    clf = clf.fit(data, target)

    # dot_data = tree.export_graphviz(
    #     clf, out_file=None, filled=True, rounded=True,
    #     special_characters=True, feature_names=enc.get_feature_names_out(input_features=X.columns), class_names=y.unique())
    # graph = graphviz.Source(dot_data)
    # graph.render(csv + "_" + alg, "results/" + filename, format="png")

    matplotlib.pyplot.switch_backend('Agg')
    viz = dtreeviz(clf, x_data=data, y_data=target,
                   target_name="class",
                   feature_names=feature_names,
                   class_names=list(target_names))
    viz.save("results/" + filename + "/" + csv + "_" + alg + ".svg")

    # X_tr = enc.inverse_transform(X_out)
    return "result", 200

    # append ISC candidates


def test(filename, csv, alg):
    label = request.args.get("selectedLabel", "")
    samples = request.args.get("selectedSamples", "").split(",")
    level = with_timestamps_level(csv)
    csv_path = exist_csv(filename, csv, level)
    if not csv_path:
        return "No file found.", 404
    dataset = pandas.read_csv(csv_path)
    # dataset.dropna(inplace=True)
    # dataset_convert = dataset.astype({"time:timestamp": "datetime64"})
    dataset_new = dataset[samples].assign(label=dataset[label])
    dataset_new.dropna(inplace=True)
    print(dataset_new)
    X = dataset_new[samples]
    # y = dataset_new["label"]
    # print(y)

    return "test", 200
