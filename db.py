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


def increment_tracker(db, name, event_date, runstreak, attempts):
    db["tracker"].append([event_date, name, str(runstreak), str(attempts)])
    save_table("tracker.csv", db["tracker"])

def get_counter_frequence(db, name):
    # Return frequence of the 'counter' rows of the dictionary
    for row in db["counter"]:
        if row[0] == name:
            return int(row[2])
    return 1
    
def get_all_counters(db):
    '''
    Return the list of counter names
    '''
    return [row[0] for row in db['counter']]

def get_tracker_data(db, name):
    # Return the rows of the dictionary 'tracker' as a dictionary all_rows
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

def modify_habit(db, old_name, new_name, new_description, new_frequence):
    '''
    Modify a habit:
    - name change: update counter.csv + tracker.csv
    - description change: only counter.csv
    - frequence change: reset tracker.csv records for that habit
    '''

    # Detect changes
    name_changed = old_name != new_name
    freq_changed = False

    # Update dictionary 'counter' and save info in counter.csv
    for row in db['counter']:
        if row[0] == old_name:
            if row[2] != str(new_frequence):
                freq_changed = True
            row[0] = new_name
            row[1] = new_description
            row[2] = str(new_frequence)
            break

    save_table('counter.csv', db['counter'])

    # Update dictionary tracker and save info in tracker.csv
    new_tracker = []
    for row in db['tracker']:
        date_, name, runstreak, attempts = row

        # remove all records if frequency changed
        if freq_changed and name == old_name:
            continue

        # rename habit in tracker
        if name_changed and name == old_name:
            name = new_name

        new_tracker.append([date_, name, runstreak, attempts])

    db['tracker'] = new_tracker
    save_table('tracker.csv', db['tracker'])

def erase_habit(db, name):
    '''
    Erase a habit completely from dictionary, counter.csv and tracker.csv
    '''

    # remove from counter
    db['counter'] = [row for row in db['counter'] if row[0] != name]
    save_table('counter.csv', db['counter'])

    # remove from tracker
    db['tracker'] = [row for row in db['tracker'] if row[1] != name]
    save_table('tracker.csv', db['tracker'])

def display_table(db):
    #Transforms the dictionary into a table that can be displayed
    converted = {
    'Habit': [item[0] for item in db['counter']],
    'Description': [item[1] for item in db['counter']],
    'Frequency': [item[2] for item in db['counter']]
    }
    return converted