# db.py Store the data (CSV version)

import csv
import os

from datetime import date, datetime, timedelta

def get_db():
    '''
    Read data from a CSV and build a dictionary called db
    '''
    db = {'counter': [], 'tracker': []}

    # Reads 'counter.csv' if exists and add it into the dictionary
    if os.path.exists('counter.csv'):
        with open('counter.csv', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            db['counter'] = list(reader)

    # Reads tracker.csv if exists and add it into the dictionary
    if os.path.exists('tracker.csv'):
        with open('tracker.csv', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            db['tracker'] = list(reader)

    return db


def save_table(filename, rows):
    # Write a list of rows to a CSV file
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(rows)


def add_counter(db, name, description, frequence):
    # Append new row in the dictionary and save it in 'counter.csv'
    db['counter'].append([name, description, frequence])
    save_table('counter.csv', db['counter'])


def increment_counter(db, name, event_date, runstreak, attempts):
    db["tracker"].append([event_date, name, str(runstreak), str(attempts)])
    save_table("tracker.csv", db["tracker"])

def get_all_counters(db):
    '''
    Return all the rows of 'counter.csv' as a dictionary
    '''
    return [row[0] for row in db['counter']]

def get_counter_frequence(db, name):
    for row in db["counter"]:
        if row[0] == name:
            return int(row[2])
    return 1

def get_counter_data(db, name):
    '''
    Return all the rows of 'tracker.csv' as a dictionary
    '''
    all_rows = []
    for row in db['tracker']:
        if row[1] == name:
            all_rows.append({
                'date': row[0],
                'name': row[1],
                'runstreak': int(row[2]),
                'attempts': int(row[3])
            })
    return all_rows

def display_table(db):
    '''
    Transforms the dictionary into a table that can be displayed
    '''
    converted = {
    'Habit': [item[0] for item in db['counter']],
    'Description': [item[1] for item in db['counter']],
    'Frequency': [item[2] for item in db['counter']]
    }
    return converted