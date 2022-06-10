import csv
import json
import os
from flask import request, current_app


def exist_csv(filename, csv):
    csv_path = os.path.join(
        current_app.config['OUTPUT_FOLDER'], filename + '/' + csv)
    if not os.path.exists(csv_path):
        return False
    else:
        return csv_path


def get_events(filename, csv):
    csv_path = exist_csv(filename, csv)
    if not csv_path:
        return "No file found.", 404
    json = {}
    return "events", 200


def delete_event(filename, csv, event):
    return "deleted", 200


def adapt_timestamps(filename, csv, level):
    return "level", 200


def get_algorithms():
    return "algorithms", 200


def appy_algorithm(filename, csv, alg):
    return "result", 200

# append ISC candidates
