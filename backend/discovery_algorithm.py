import os
from flask import request, current_app, send_file
import pandas
import pm4py


def exist_csv(filename, csv):
    csv_path = os.path.join(
        current_app.config['OUTPUT_FOLDER'], filename + "_" + csv + ".csv")
    if os.path.exists(csv_path):
        return csv_path
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
    if len(csv.split("_")) > 1:
        if csv.rsplit("_", 1)[1] == "modified":
            csv_folder = os.path.join(folder, csv.rsplit("_", 1)[0])
        else:
            csv_folder = os.path.join(folder, csv)
    else:
        csv_folder = os.path.join(folder, csv)
    csv_path = os.path.join(csv_folder, csv + '.csv')
    if not os.path.exists(csv_path):
        return False
    else:
        return csv_path


def get_events(filename, csv):
    csv_path = exist_csv(filename, csv)
    if not csv_path:
        return "No file found.", 404
    json_path = csv_path.rsplit(".", 1)[0] + '.json'
    partial_log = pandas.read_csv(csv_path)
    # "records" -- The format of the JSON string [{column -> value}, … , {column -> value}]
    partial_log.to_json(json_path, orient="records")
    return send_file(json_path, as_attachment=False), 200


def delete_event(filename, csv):
    args = request.args.copy()
    eventIndex = int(args.pop("eventIndex", ""))
    csv_path = exist_csv(filename, csv)
    if not csv_path:
        return "No file found.", 404
    log = pandas.read_csv(csv_path)
    log = remove_with_index(log, eventIndex)
    # without add an index column
    log.to_csv(csv_path, index_label="No.")

    csv_path_modified = csv_path.rsplit(".", 1)[0] + "_modified.csv"
    if os.path.exists(csv_path_modified):
        log_modified = pandas.read_csv(csv_path)
        log_modified = remove_with_index(log_modified, eventIndex)
        log_modified.to_csv(csv_path_modified, index_label="No.")
    return "The chosen event from " + csv + ".csv has been successfully removed.", 200

def remove_with_index(log, eventIndex):
    log.drop(eventIndex, axis=0, inplace=True)  # Raises error?
    log.reset_index(drop=True, inplace=True)
    log.drop(columns="No.", inplace=True)
    return log

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
        return "No CSV file found.", 404
    args = request.args.copy()
    selectedVariants = args.pop("variants", "").split(",")
    filtered_log = apply_variants_filter(csv_path, selectedVariants)
    coarsen_timestamps_Period(filtered_log, level)
    csv_output_path = define_output_path(filename, csv)
    filtered_log.to_csv(csv_output_path, index=False)  # type: ignore

    xes_path = csv_path.rsplit(".", 1)[0] + ".xes"
    arff_path = csv_path.rsplit(".", 1)[0] + ".arff"
    log = pm4py.read_xes(xes_path)
    df = pm4py.convert_to_dataframe(log)
    if not os.path.exists(arff_path) or not os.path.exists(xes_path):
        return "No ARFF or XES file found.", 404
    coarsen_timestamps_Datetime(df, level)
    import weka.core.jvm as jvm
    try:
        jvm.start(max_heap_size="512m", system_cp=True)
        arff_output_path = csv_output_path.rsplit(".", 1)[0] + ".arff"
        import projection_transformation_algorithm
        projection_transformation_algorithm.df2arff(df, arff_output_path, csv)
        jvm.stop()
    except:
        return "Something went wrong!"
    return f"File {csv}_modified.csv is saved."


def define_output_path(filename, csv):
    if len(csv.split("&")) == 1 and len(filename.split("&")) > 1:
        for log in filename.split("&"):
            folder = os.path.join(
                current_app.config['OUTPUT_FOLDER'], log)
            csv_folder = os.path.join(folder, csv)
            csv_path = os.path.join(csv_folder, csv + '.csv')
            if os.path.exists(csv_path):
                csv_output_path = os.path.join(
                    csv_folder, csv + '_modified.csv')
                return(csv_output_path)
    csv_path = os.path.join(
        current_app.config['OUTPUT_FOLDER'], filename + "_" + csv + ".csv")
    if os.path.exists(csv_path):
        csv_output_path = os.path.join(
            current_app.config['OUTPUT_FOLDER'], filename + '_' + csv + '_modified.csv')
    else:
        csv_output_path = os.path.join(
            current_app.config['OUTPUT_FOLDER'], filename + '/' + csv + "/" + csv + '_modified.csv')
    return csv_output_path


def coarsen_timestamps_Period(filtered_log, level):
    lev = convert_level(level)
    for i in filtered_log.get("No."):
        filtered_log.loc[i, "time:timestamp"] = pandas.Period(
            filtered_log.loc[i, "time:timestamp"], freq=lev)
    return None


def coarsen_timestamps_Datetime(df, level):
    flag = True
    if level != "Seconds" and flag:
        new_df = pandas.DataFrame(
            {'time:timestamp': [x.replace(second=0) for x in df["time:timestamp"]]})
        df.update(new_df, overwrite=True)
    else:
        flag = False
    if level != "Minutes" and flag:
        new_df = pandas.DataFrame(
            {'time:timestamp': [x.replace(minute=0) for x in df["time:timestamp"]]})
        df.update(new_df, overwrite=True)
    else:
        flag = False
    if level != "Hours" and flag:
        new_df = pandas.DataFrame(
            {'time:timestamp': [x.replace(hour=0) for x in df["time:timestamp"]]})
        df.update(new_df, overwrite=True)
    else:
        flag = False
    if level != "Days" and flag:
        new_df = pandas.DataFrame(
            {'time:timestamp': [x.replace(day=1) for x in df["time:timestamp"]]})
        df.update(new_df, overwrite=True)
    else:
        flag = False
    if level != "Months" and flag:
        new_df = pandas.DataFrame(
            {'time:timestamp': [x.replace(month=1) for x in df["time:timestamp"]]})
        df.update(new_df, overwrite=True)
    else:
        flag = False
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
        variants_dict[i] = [var, variants[var]]
        i += 1
    return variants_dict, 200


def apply_variants_filter(csv_path, selectedVariants):
    partial_log = pandas.read_csv(csv_path)
    variants = pm4py.get_variants_as_tuples(partial_log)
    filterVariants = []
    i = 0
    for var in variants:
        if i == min([len(selectedVariants), len(variants)]):
            break
        if selectedVariants[i] == "true":
            filterVariants.append(var)
        i += 1
    fl = pm4py.filter_variants(partial_log, filterVariants)
    return fl
