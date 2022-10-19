import os
from flask import request, current_app, send_file
import pandas
import pm4py


def exist_csv(filename, csv):
    csv_path = os.path.join(
        current_app.config['OUTPUT_FOLDER'], filename + "_" + csv + ".csv")
    if os.path.exists(csv_path): return csv_path
    if len(csv.split("&")) == 1 and len(filename.split("&")) > 1:
        for log in filename.split("&"):
            folder = os.path.join(
                current_app.config['OUTPUT_FOLDER'], log)
            if csv.rsplit("_", 1)[1] == "modified":
                csv_folder = os.path.join(folder, csv.rsplit("_", 1)[0])
            else:
                csv_folder = os.path.join(folder, csv)
            csv_path = os.path.join(csv_folder, csv + '.csv')
            if os.path.exists(csv_path): 
                return csv_path
    folder = os.path.join(
        current_app.config['OUTPUT_FOLDER'], filename)
    if csv.rsplit("_", 1)[1] == "modified":
        csv_folder = os.path.join(folder, csv.rsplit("_", 1)[0])
    else:
        csv_folder = os.path.join(folder, csv)
    csv_path = os.path.join(csv_folder, csv + '.csv')
    if not os.path.exists(csv_path):
        return False
    else:
        return csv_path


def get_events(filename, csv):
    # label = request.args.get("label", "")
    # if label == "":
    csv_path = exist_csv(filename, csv)
    if not csv_path:
        return "No file found.", 404
    json_path = csv_path.rsplit(".", 1)[0] + '.json'
    partial_log = pandas.read_csv(csv_path)
    # "records" -- The format of the JSON string [{column -> value}, … , {column -> value}]
    partial_log.to_json(json_path, orient="records")
    return send_file(json_path, as_attachment=False), 200
    # else:
    #     csv_path = exist_csv(filename, csv)
    #     if not csv_path:
    #         return "No file found.", 404
    #     partial_log = pandas.read_csv(csv_path)
    #     dict = {}
    #     i = 0
    #     for l in partial_log[label].dropna().unique():
    #         dict[i] = l
    #         i += 1
    #     return dict, 200


def delete_event(filename, csv, eventIndex):
    csv_path = exist_csv(filename, csv)
    if not csv_path:
        return "No file found.", 404
    partial_log = pandas.read_csv(csv_path)
    partial_log.drop(eventIndex, axis=0, inplace=True)  # Raises error?
    partial_log.reset_index(drop=True, inplace=True)
    partial_log.drop(columns="No.", inplace=True)
    partial_log.to_csv(csv_path, index_label="No.")  # without add an index column
    return "The chosen event from " + csv + ".csv has been successfully removed.", 200


def convert_level(level):
    if level == "Minutes":
        return "T"
    if level == "Hours":
        return "H"
    if level == "Days":
        return "D"
    if level == "Months":
        return "M"
    if level == "Years":
        return "Y"

def modify(filename, csv, level):
    csv_path = exist_csv(filename, csv)
    if not csv_path:
        return "No file found.", 404
    args = request.args.copy()
    selectedVariants = args.pop("variants", "").split(",")
    filtered_log = apply_variants_filter(csv_path, selectedVariants)
    coarsen_timestamps(filtered_log, level)
    csv_output_path = define_output_path(filename, csv)
    filtered_log.to_csv(csv_output_path, index=False)
    return f"File {csv}_modified.csv is saved."

def define_output_path(filename, csv):
    csv_path = os.path.join(
        current_app.config['OUTPUT_FOLDER'], filename + "_" + csv + ".csv")
    if os.path.exists(csv_path):
        csv_output_path = os.path.join(current_app.config['OUTPUT_FOLDER'], filename + '_' + csv + '_modified.csv')
    else: 
        csv_output_path = os.path.join(current_app.config['OUTPUT_FOLDER'], filename + '/' + csv + "/" + csv + '_modified.csv')
    return csv_output_path

def coarsen_timestamps(filtered_log, level):
    lev = convert_level(level)
    for i in filtered_log.get("No."):
        filtered_log.loc[i, "time:timestamp"] = pandas.Period(filtered_log.loc[i, "time:timestamp"], freq=lev)
    return None

def exist_file(filename):
    input_path = os.path.join(
        current_app.config['UPLOAD_FOLDER'], filename + '.xes')
    if not os.path.exists(input_path):
        return False
    else:
        return input_path

def get_variants(filename, csv):
    csv_path = exist_csv(filename, csv)
    if not csv_path:
        return "No file found.", 404
    partial_log = pandas.read_csv(csv_path)
    variants = pm4py.get_variants_as_tuples(partial_log)
    variants_dict = {}
    i = 0
    for var in variants:
        if i == 3: print(variants[var])
        variants_dict[i] = [var, variants[var]]
        i += 1
    return variants_dict, 200

def apply_variants_filter(csv_path, selectedVariants):
    partial_log = pandas.read_csv(csv_path)
    variants = pm4py.get_variants_as_tuples(partial_log)
    filterVariants = []
    i = 0
    for var in variants:
        if selectedVariants[i]=="true": filterVariants.append(var)
        i += 1
    fl = pm4py.filter_variants(partial_log, filterVariants)
    return fl
