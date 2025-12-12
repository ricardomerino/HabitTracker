# analyse.py
from db import get_counter_data
def calculate_count(db, counter):
    ''' Calculate the count of the counter.
    :param db: on initialized sqlite3 database connection
    :param counter: name of hte counter present in the DB
    :return
    : length of the counter increment events '''
    data = get_counter_data(db, counter)
    return len(data)