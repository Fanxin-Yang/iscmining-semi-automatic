import csv
import json
import os
from unicodedata import category
from flask import jsonify, make_response, request, current_app, send_file, send_from_directory
import matplotlib
from matplotlib import transforms
import pandas
from sklearn import tree, preprocessing
from sklearn.datasets import load_iris
import graphviz
import numpy
from sklearn.impute import SimpleImputer
from dtreeviz.trees import dtreeviz
# from sklearn import datasets
# from sklearn.datasets import load_iris, load_boston
from sklearn.compose import make_column_selector, make_column_transformer
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.tree._tree import TREE_LEAF
from traitlets import Undefined


def exist_csv(filename, csv):
    folder = os.path.join(
        current_app.config['OUTPUT_FOLDER'], filename)
    level = with_timestamps_level(csv)
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
    label = request.args.get("label", "")
    if label == "":
        csv_path = exist_csv(filename, csv)
        if not csv_path:
            return "No file found.", 404
        json_path = csv_path.rsplit(".", 1)[0] + '.json'
        dataset = pandas.read_csv(csv_path)
        # "records" -- The format of the JSON string [{column -> value}, … , {column -> value}]
        dataset.to_json(json_path, orient="records")
        return send_file(json_path, as_attachment=False), 200
    else:
        csv_path = exist_csv(filename, csv)
        if not csv_path:
            return "No file found.", 404
        dataset = pandas.read_csv(csv_path)
        dict = {}
        i = 0
        for l in dataset[label].dropna().unique():
            dict[i] = l
            i += 1
        return dict, 200


def delete_event(filename, csv, eventIndex):
    csv_path = exist_csv(filename, csv)
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
    csv_path = exist_csv(filename, csv)
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


def get_decisiontree(filename, csv):
    csv_path = exist_csv(filename, csv)
    if not csv_path:
        return "No file found.", 404
    folder = os.path.join(
        current_app.config['RESULTS_FOLDER'], filename)
    svg_path = os.path.join(folder, csv + '_decisiontree.svg')
    if not os.path.exists(svg_path):
        return "No decisiont tree found.", 404
    else:
        return send_file(svg_path)


def filter(args, dataset):
    for key in args.keys():
        if args.get(key).__len__() != 0:
            arr = args.get(key).split(",")
            if dataset[key].dtype == numpy.float_:
                print("float")
                arr = list(map(float, arr))
            elif dataset[key].dtype == numpy.int_:
                print("int")
                arr = list(map(int, arr))
            elif dataset[key].dtype == numpy.bool_:
                print("bool")
                arr = list(map(bool, arr))
            print(arr)
            dataset = dataset[dataset[key].isin(arr)]
    print(dataset.head)
    return dataset


def appy_algorithm(filename, csv, alg):
    args = request.args.copy()
    label = args.pop("classLabel", "")
    samples = args.pop("inputSamples", "").split(",")
    csv_path = exist_csv(filename, csv)
    if not csv_path:
        return "No file found.", 404
    dataset = pandas.read_csv(csv_path, index_col="No.")
    dataset = filter(args, dataset)

    # dataset_convert = dataset.astype({"time:timestamp": "datetime64"})
    for tmp in dataset:
        if dataset[tmp].dtype == object:
            dataset[tmp] = dataset[tmp].astype("category")
    dataset_new = dataset[samples].assign(label=dataset[label])
    if dataset_new.empty:
        return "No event exist after filtering.", 405
    dataset_new.dropna(inplace=True)
    if dataset_new.empty:
        return "Selected target values input samples includes missing value.", 405
    print(dataset_new.head)
    X = dataset_new[samples]
    y = dataset_new["label"]

    # Imputation of missing values https://scikit-learn.org/stable/modules/impute.html
    # imp = SimpleImputer(strategy="constant", fill_value=-1)
    # data = imp.fit_transform(X)
    # feature_names = list(X.columns)

    # https://scikit-learn.org/stable/auto_examples/tree/plot_cost_complexity_pruning.html#
    # Post pruning decision trees with cost complexity pruning
    # cost_complexity_pruning
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=.20, random_state=45)

    encoderX = preprocessing.OrdinalEncoder(
        handle_unknown='use_encoded_value', unknown_value=-1)
    ct = make_column_transformer((encoderX, make_column_selector(
        dtype_include='category')), remainder='passthrough', verbose_feature_names_out=False)
    data_train = ct.fit_transform(X_train)
    data_test = ct.fit_transform(X_test)
    feature_names = ct.get_feature_names_out()

    encodery = preprocessing.OrdinalEncoder(
        handle_unknown='use_encoded_value', unknown_value=-1)
    target_train = y_train
    target_test = y_test
    if y.dtype == "category":
        target_train = encodery.fit_transform(
            y_train.values.reshape(-1, 1)).reshape(1, -1)[0]
        target_test = encodery.fit_transform(
            y_test.values.reshape(-1, 1)).reshape(1, -1)[0]
    target_names = y.unique()

    clf = decision_tree_classification(data_train, target_train)

    results_folder = os.path.join(
        current_app.config['RESULTS_FOLDER'], filename)
    if not os.path.exists(results_folder):
        os.makedirs(results_folder)

    dot_data = tree.export_graphviz(
        clf, out_file=None, filled=True, rounded=True,
        special_characters=True, feature_names=feature_names, class_names=list(target_names))
    graph = graphviz.Source(dot_data)
    graph.render(csv + "_" + alg, results_folder, format="png")

    matplotlib.pyplot.switch_backend('Agg')
    viz = dtreeviz(clf, x_data=data_test, y_data=target_test,
                   target_name="class",
                   feature_names=feature_names,
                   class_names=list(target_names),
                   scale=2)
    svg_path = os.path.join(results_folder, csv + "_" + alg + ".svg")
    viz.save(svg_path)

    dot_path = os.path.join(results_folder, csv + "_" + alg + ".dot")
    dotFile = open(dot_path, "w")
    dotFile.write(viz.dot)
    dotFile.close()

    return "Result has been saved!", 200

    # append ISC candidates


def decision_tree_classification(data, target):
    # not worth the higher training time for entropy criterion
    clf = tree.DecisionTreeClassifier(
        criterion="gini", splitter="random", min_samples_leaf=3)
    clf = clf.fit(data, target)
    # target_train_pred = clf.predict(data_train)
    # target_test_pred = clf.predict(data_test)
    # print('Before pruning')
    # print(f'Node count: {clf.tree_.node_count}')
    # print(f'Depth: {clf.tree_.max_depth}')
    # print(f'Train accuracy: {round(accuracy_score(target_train, target_train_pred), 2)} and Test accuracy: {round(accuracy_score(target_test, target_test_pred), 2)}')

    # max_ccp_alpha = cost_complexity_pruning(data_train, data_test,
    #                                         target_train, target_test, clf)
    # clf = tree.DecisionTreeClassifier(
    #     criterion="gini", splitter="random", min_samples_leaf=3, ccp_alpha=max_ccp_alpha)
    # clf = clf.fit(data_train, target_train)
    # target_train_pred = clf.predict(data_train)
    # target_test_pred = clf.predict(data_test)
    # print('After pruning')
    # print(f'Node count: {clf.tree_.node_count}')
    # print(f'Depth: {clf.tree_.max_depth}')
    # print(f'Train accuracy: {round(accuracy_score(target_train, target_train_pred), 2)} and Test accuracy: {round(accuracy_score(target_test, target_test_pred), 2)}')
    return clf


def cost_complexity_pruning(data_train, data_test, target_train, target_test, clf):
    path = clf.cost_complexity_pruning_path(data_train, data_train)
    ccp_alphas, impurities = path.ccp_alphas, path.impurities
    # print(f'ccp_alphas: {ccp_alphas}')

    clfs = []
    # Accuracy vs alpha
    acc_train, acc_test = [], []
    for ccp_alpha in ccp_alphas:
        clf = tree.DecisionTreeClassifier(
            criterion="gini", splitter="random", min_samples_leaf=3, ccp_alpha=ccp_alpha)
        clf.fit(data_train, target_train)
        target_train_pred = clf.predict(data_train)
        target_test_pred = clf.predict(data_test)
        acc_train.append(accuracy_score(target_train, target_train_pred))
        acc_test.append(accuracy_score(target_test, target_test_pred))
        clfs.append(clf)
    # print(f'acc_train: {acc_train}')
    # print(f'acc_test: {acc_test}')

    acc_sum = [x + y for (x, y) in zip(acc_train, acc_test)]

    # max_acc_test = max(acc_test)
    # max_index = acc_test.index(max_acc_test)
    # print(
    #     f"max accuracy of test is {round(max_acc_test, 2)} and index is {max_index}")

    max_acc_sum = max(acc_sum)
    max_index = acc_sum.index(max_acc_sum)
    print(
        f"max accuracy of sum is {round(max_acc_sum, 2)} and index is {max_index}")

    # Number of nodes vs alpha & Depth vs alpha
    # clfs = clfs[:-1]
    # ccp_alphas = ccp_alphas[:-1]
    # print(f'ccp_alphas: {ccp_alphas}')
    # node_counts = [clf.tree_.node_count for clf in clfs]
    # depth = [clf.tree_.max_depth for clf in clfs]

    return ccp_alphas[max_index]


def test(filename, csv, alg):
    return "test", 200
