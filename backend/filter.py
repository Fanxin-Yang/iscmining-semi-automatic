import os
from flask import current_app, request
import pm4py, pandas
import discovery_algorithm

def exist_file(filename):
    input_path = os.path.join(
        current_app.config['UPLOAD_FOLDER'], filename + '.xes')
    if not os.path.exists(input_path):
        return False
    else:
        return input_path

def get_variants(filename, csv):
    csv_path = discovery_algorithm.exist_csv(filename, csv)
    if not csv_path:
        return "No file found.", 404
    partial_log = pandas.read_csv(csv_path)
    # log = xes_importer.apply("uploads/loan_process.xes")
    variants = pm4py.get_variants_as_tuples(partial_log)
    # variants = pm4py.statistics.variants.log.get.get_variants(partial_log)
    
    variants_dict = {}
    i = 0
    for var in variants:
        if i == 3: print(variants[var])
        variants_dict[i] = [var, variants[var]]
        i += 1
    return variants_dict, 200

def apply_variants_filter(filename, csv, level):
    args = request.args.copy()
    selectedVariants = args.pop("variants", "").split(",")

    csv_path = discovery_algorithm.exist_csv(filename, csv)
    if not csv_path:
        return "No file found.", 404
    partial_log = pandas.read_csv(csv_path)
    variants = pm4py.get_variants_as_tuples(partial_log)
    filterVariants = []
    i = 0
    for var in variants:
        if selectedVariants[i]=="true": filterVariants.append(var)
        i += 1
    fl = pm4py.filter_variants(partial_log, filterVariants)
    percent = "{:.2f}".format(fl.shape[0]/partial_log.shape[0]*100)
    return f"{fl.shape[0]}/{partial_log.shape[0]} ({percent}%) events", 200