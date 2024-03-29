import os
from flask import request, current_app, send_file
import matplotlib
import pandas
import numpy
from sklearn import tree, preprocessing
from dtreeviz.trees import dtreeviz
from sklearn.compose import make_column_selector, make_column_transformer
import discovery_algorithm


def get_algorithms_scikit():
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


def get_algorithms_weka():
    algorithms = {}
    algorithms[0] = "JRip"
    return algorithms, 200


def get_decisiontree(filename, csv):
    csv_path = discovery_algorithm.exist_csv(filename, csv)
    if not csv_path:
        return "No file found.", 404
    folder = os.path.join(
        current_app.config['RESULTS_FOLDER'], filename)
    svg_path = os.path.join(folder, csv + '_decisiontree.svg')
    if not os.path.exists(svg_path):
        return "No decisiont tree found.", 404
    else:
        return send_file(svg_path)


def get_decisionrule(filename, csv, alg):
    csv_path = discovery_algorithm.exist_csv(filename, csv)
    if not csv_path:
        return "No file found.", 404
    folder = os.path.join(
        current_app.config['RESULTS_FOLDER'], filename)
    rule_path = os.path.join(folder, csv + '_' + alg + '.txt')
    if not os.path.exists(rule_path):
        return "No decisiont rule found.", 404
    else:
        with open(rule_path, "r") as f:
            rules = f.readlines()
        i = 0
        rules_dict = {}
        for rule in rules:
            rules_dict[i] = rule
            i += 1
        return rules_dict


def filter(args, partial_log):
    for key in args.keys():
        if args.get(key).__len__() != 0:
            arr = args.get(key).split(",")
            if partial_log[key].dtype == numpy.float_:
                arr = list(map(float, arr))
            elif partial_log[key].dtype == numpy.int_:
                arr = list(map(int, arr))
            elif partial_log[key].dtype == numpy.bool_:
                arr = list(map(bool, arr))
            partial_log = partial_log[partial_log[key].isin(arr)]
    return partial_log


def encoder_X_y(encoder, X, y):
    if encoder == "0":
        encoderX = preprocessing.OrdinalEncoder(
            handle_unknown='use_encoded_value', unknown_value=-1)
    else:
        encoderX = preprocessing.OneHotEncoder(handle_unknown='ignore')
    # only encode the columns which are categorical varibales
    ct = make_column_transformer((encoderX, make_column_selector(
        dtype_include='category')), remainder='passthrough', verbose_feature_names_out=False)
    # data_train = ct.fit_transform(X_train)
    # data_test = ct.fit_transform(X_test)
    # if encoder == "0" else ct.fit_transform(X).toarray()
    data = ct.fit_transform(X)
    feature_names = ct.get_feature_names_out()
    encoderX.fit(X)

    encodery = preprocessing.OrdinalEncoder(
        handle_unknown='use_encoded_value', unknown_value=-1)
    # target_train = y_train
    # target_test = y_test
    target = y
    if y.dtype == "category":
        # target_train = encodery.fit_transform(
        #     y_train.values.reshape(-1, 1)).reshape(1, -1)[0]
        # target_test = encodery.fit_transform(
        #     y_test.values.reshape(-1, 1)).reshape(1, -1)[0]
        target = encodery.fit_transform(
            y.values.reshape(-1, 1)).reshape(1, -1)[0]
    target_names = y.unique()
    # tmp = y.values.reshape(-1, 1)
    return data, target, feature_names, target_names


def visualize(clf, data, target, feature_names, target_names, svg_path):
    # dot_data = tree.export_graphviz(
    #     clf, out_file=None, filled=True, rounded=True,
    #     special_characters=True, feature_names=feature_names, class_names=list(target_names))
    # graph = graphviz.Source(dot_data)
    # graph.render(csv + "_" + alg, results_folder, format="png")
    matplotlib.pyplot.switch_backend('Agg')  # type: ignore
    viz = dtreeviz(clf, x_data=data, y_data=target,
                   target_name="class",
                   feature_names=feature_names,
                   class_names=list(target_names),
                   scale=2)
    viz.save(svg_path)
    # dot_path = os.path.join(results_folder, csv + "_" + alg + ".dot")
    # dotFile = open(dot_path, "w")
    # dotFile.write(viz.dot)
    # dotFile.close()


def get_rules(clf, feature_names, class_names):
    tree_ = clf.tree_
    feature_name = [
        feature_names[i] if i != tree._tree.TREE_UNDEFINED else "undefined!"
        for i in tree_.feature
    ]

    paths = []
    path = []

    def recurse(node, path, paths):

        if tree_.feature[node] != tree._tree.TREE_UNDEFINED:  # type: ignore
            name = feature_name[node]
            threshold = tree_.threshold[node]
            p1, p2 = list(path), list(path)
            p1 += [f"({name} <= {numpy.round(threshold, 3)})"]
            recurse(tree_.children_left[node], p1, paths)
            p2 += [f"({name} > {numpy.round(threshold, 3)})"]
            recurse(tree_.children_right[node], p2, paths)
        else:
            path += [(tree_.value[node], tree_.n_node_samples[node])]
            paths += [path]

    recurse(0, path, paths)

    # sort by samples count
    samples_count = [p[-1][1] for p in paths]
    ii = list(numpy.argsort(samples_count))
    paths = [paths[i] for i in reversed(ii)]

    rules = []
    for path in paths:
        rule = "if "

        for p in path[:-1]:
            if rule != "if ":
                rule += " and "
            rule += str(p)
        rule += " then "
        if class_names is None:
            rule += "response: "+str(numpy.round(path[-1][0][0][0], 3))
        else:
            classes = path[-1][0][0]
            l = numpy.argmax(classes)
            rule += f"class: {class_names[l]} (proba: {numpy.round(100.0*classes[l]/numpy.sum(classes),2)}%)"
        rule += f" | based on {path[-1][1]:,} samples"
        rules += [rule]

    return rules


def apply_algorithm_scikit(filename, csv, alg):
    args = request.args.copy()
    label = args.pop("classLabel", "")
    samples = args.pop("inputSamples", "").split(",")
    encoder = args.pop("encoder", "0")
    ccp_alpha = -1
    if "ccp_alpha" in args:
        ccp_alpha = args.pop("ccp_alpha")

    csv_path = discovery_algorithm.exist_csv(filename, csv)
    if not csv_path:
        return "No file found.", 404
    partial_log = pandas.read_csv(csv_path, index_col="No.")
    partial_log = filter(args, partial_log)

    # Only for Loan_example: only keep two days
    # partial_log.drop(partial_log[(partial_log["concept:name"] !=
    #                               "approve loan") & (partial_log["concept:name"] !=
    #                                                  "arrange loan")].index, inplace=True)
    # partial_log.drop(partial_log[(partial_log["time:timestamp"] !=
    #                               "2016-07-19") & (partial_log["time:timestamp"] !=
    #                                                "2016-07-20")].index, inplace=True)
    # print(partial_log)
    # partial_log["time:timestamp"] = partial_log["time:timestamp"].astype(
    #     'category')

    for tmp in partial_log:
        if partial_log[tmp].dtype == object:
            partial_log[tmp] = partial_log[tmp].astype("category")
    partial_log_new = partial_log[samples].assign(label=partial_log[label])
    partial_log_new.dropna(inplace=True)
    if partial_log_new.empty:
        return "Selected target values input samples includes missing value.", 405
    X = partial_log_new[samples]
    y = partial_log_new["label"]

    # Imputation of missing values https://scikit-learn.org/stable/modules/impute.html
    # imp = SimpleImputer(strategy="constant", fill_value=-1)
    # data = imp.fit_transform(X)
    # feature_names = list(X.columns)

    # X_train, X_test, y_train, y_test = train_test_split(
    #     X, y, test_size=.20, random_state=45)

    data, target, feature_names, target_names = encoder_X_y(encoder, X, y)

    if ccp_alpha == -1:
        clf = tree.DecisionTreeClassifier(criterion="gini", splitter="random")
        # options = cost_complexity_pruning(data, target, clf)
    else:
        ccp_alpha = float(ccp_alpha)
        clf = tree.DecisionTreeClassifier(
            criterion="gini", splitter="random", ccp_alpha=ccp_alpha)
    options = cost_complexity_pruning(data, target, clf)
    clf = clf.fit(data, target)
    if clf.tree_.node_count > 100:
        if ccp_alpha == -1:
            return options, 202
        else:
            # options bigger than ccp_alpha
            greaterOptions = {}
            i = 0
            for j in range(len(options)):
                if(options[j] > ccp_alpha):
                    greaterOptions[i] = options[j]
                    i += 1
            return greaterOptions, 202

    results_folder = os.path.join(
        current_app.config['RESULTS_FOLDER'], filename)
    if not os.path.exists(results_folder):
        os.makedirs(results_folder)

    rule_path = os.path.join(results_folder, csv + "_" + "decisionrule.txt")
    rules = get_rules(clf, feature_names, target_names)
    with open(rule_path, "w+") as f:
        for r in rules:
            f.write(r + "\n")

    svg_path = os.path.join(results_folder, csv + "_" + alg + ".svg")
    visualize(clf, data, target, feature_names, target_names, svg_path)

    if ccp_alpha == -1:
        return options, 201
    else:
        return f"With selected ccp_alpha value {ccp_alpha} decision tree has {clf.tree_.node_count} nodes and max depth {clf.tree_.max_depth}.", 200


def cost_complexity_pruning(data, target, clf):
    path = clf.cost_complexity_pruning_path(data, target)
    ccp_alphas, impurities = path.ccp_alphas, path.impurities
    # keep only positive value
    ccp_alphas = [ccp for ccp in ccp_alphas if ccp >= 0]
    # keep unique values
    ccp_alphas_set = set(ccp_alphas)
    ccp_alphas = list(ccp_alphas_set)
    ccp_alphas.sort()

    clfs = []
    # Total impurity of leaves
    # for ccp_alpha in ccp_alphas:
    #     clf = tree.DecisionTreeClassifier(random_state=0, ccp_alpha=ccp_alpha)
    #     clf.fit(data, target)
    #     if clf.tree_.node_count < 100: clfs.append(clf)
    #     print(
    #         "Number of nodes in the last tree is: {} with ccp_alpha: {}".format(
    #             clf.tree_.node_count, ccp_alpha
    #         )
    #     )
    # print([clf.tree_.node_count for clf in clfs])
    # print([clf.tree_.max_depth for clf in clfs])

    node_counts = [clf.tree_.node_count for clf in clfs]
    depths = [clf.tree_.max_depth for clf in clfs]
    # Accuracy vs alpha
    # acc_train, acc_test = [], []
    # for ccp_alpha in ccp_alphas:
    #     clf = tree.DecisionTreeClassifier(
    #         criterion="gini", splitter="random", min_samples_leaf=3, ccp_alpha=ccp_alpha)
    #     clf.fit(data_train, target_train)
    #     target_train_pred = clf.predict(data_train)
    #     target_test_pred = clf.predict(data_test)
    #     acc_train.append(accuracy_score(target_train, target_train_pred))
    #     acc_test.append(accuracy_score(target_test, target_test_pred))
    #     clfs.append(clf)
    # print(f'acc_train: {acc_train}')
    # print(f'acc_test: {acc_test}')

    # acc_sum = [x + y for (x, y) in zip(acc_train, acc_test)]

    # max_acc_test = max(acc_test)
    # max_index = acc_test.index(max_acc_test)
    # print(
    #     f"max accuracy of test is {round(max_acc_test, 2)} and index is {max_index}")

    # max_acc_sum = max(acc_sum)
    # max_index = acc_sum.index(max_acc_sum)
    # print(
    #     f"max accuracy of sum is {round(max_acc_sum, 2)} and index is {max_index}")

    # Number of nodes vs alpha & Depth vs alpha
    # clfs = clfs[:-1]
    # ccp_alphas = ccp_alphas[:-1]
    # print(f'ccp_alphas: {ccp_alphas}')
    # node_counts = [clf.tree_.node_count for clf in clfs]
    # depth = [clf.tree_.max_depth for clf in clfs]

    options = {}
    index = 0
    for i in range(len(ccp_alphas)):
        options[index] = ccp_alphas[i]
        index += 1
    return options


def apply_algorithm_weka(filename, arff, alg):
    args = request.args.copy()
    cls_options = args.pop("cls_options", "")
    class_name = args.pop("class_name", "")
    arff_path = exist_arff(filename, arff)
    if not arff_path:
        return "No file found.", 404
    results_folder = os.path.join(
        current_app.config['RESULTS_FOLDER'], filename)
    if not os.path.exists(results_folder):
        os.makedirs(results_folder)
    result_path = os.path.join(results_folder, arff + "_" + alg)

    if alg == "JRip":
        return apply_JRip(arff_path, cls_options, class_name, result_path)
    # for other algorithms
    return "No support for this algorithm yet."


def apply_JRip(arff_path, cls_options, class_name, result_path):
    cls_cmdline = "weka.classifiers.rules.JRip " + cls_options
    result_path += ".txt"

    import weka.core.jvm as jvm
    # try:
    jvm.start(max_heap_size="512m", system_cp=True)
    import weka.core.converters as converters
    loader = converters.Loader(classname="weka.core.converters.ArffLoader")
    data = loader.load_file(arff_path, class_index=0)
    if class_name in data.attribute_names():
        classIndex = data.attribute_names().index(class_name)
    else:
        classIndex = 0
    if data.class_index != classIndex:
        data = loader.load_file(arff_path, class_index=classIndex)
    # usually the first is "concept:name"
    # the class label will not be removed by weka.filters.unsupervised.attribute.*

    # classIndex = data.attribute_names().index("concept:name")

    # from weka.classifiers import Classifier
    from weka.core.classes import to_commandline, from_commandline
    # cls = Classifier(classname="weka.classifiers.rules.JRip",
    #                  options=["-N", "5.0"])
    # cmdline = 'weka.classifiers.rules.JRip -F 3 -N 5.0 -O 2 -S 1'
    cls = from_commandline(
        cls_cmdline, classname="weka.classifiers.Classifier")

    # Filter string because JRip cannot handle string
    from weka.filters import Filter
    remove = Filter(
        classname="weka.filters.unsupervised.attribute.RemoveType", options=["-T", "string"])
    remove.inputformat(data)
    filtered_data = remove.filter(data)
    # print(f"Attributes after filter: {filtered_data.attribute_names()}")

    from javabridge.jutil import JavaException
    try:
        cls.build_classifier(filtered_data)  # type: ignore
    except JavaException:
        return "JRip cannot handle string class! Since string attributes have been removed. The class label is string type"

    # save rule set in txt file
    with open(result_path, "w+") as f:
        for r in str(cls).split("\n"):
            f.write(r + "\n")
    jvm.stop()
    # except:
    #     return "Something went wrong!"
    return "The rule set by applying JRip is saved."


def exist_arff(filename, arff):
    arff_path = os.path.join(
        current_app.config['OUTPUT_FOLDER'], filename + "_" + arff + ".arff")
    if os.path.exists(arff_path):
        return arff_path
    if len(arff.split("&")) == 1 and len(filename.split("&")) > 1:
        for log in filename.split("&"):
            folder = os.path.join(
                current_app.config['OUTPUT_FOLDER'], log)
            if arff.rsplit("_", 1)[1] == "modified":
                arff_folder = os.path.join(folder, arff.rsplit("_", 1)[0])
            else:
                arff_folder = os.path.join(folder, arff)
            arff_path = os.path.join(arff_folder, arff + '.arff')
            if os.path.exists(arff_path):
                return arff_path
    folder = os.path.join(
        current_app.config['OUTPUT_FOLDER'], filename)
    if len(arff.split("_")) > 1:
        if arff.rsplit("_", 1)[1] == "modified":
            arff_folder = os.path.join(folder, arff.rsplit("_", 1)[0])
        else:
            arff_folder = os.path.join(folder, arff)
    else:
        arff_folder = os.path.join(folder, arff)
    arff_path = os.path.join(arff_folder, arff + '.arff')
    if not os.path.exists(arff_path):
        return False
    else:
        return arff_path


def get_alg_description(alg):
    if alg == "JRip":
        import weka.core.jvm as jvm
        try:
            jvm.start(max_heap_size="512m", system_cp=True)
            from weka.classifiers import Classifier
            cls = Classifier(classname="weka.classifiers.rules.JRip",
                             options=["-N", "5.0"])
            description = cls.description()
            jvm.stop()
        except:
            return "Something went wrong!"
        return str(description).split("\n", 1)[0]
