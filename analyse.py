# analyse.py
from db import get_tracker_data
def calculate_count(db, name):
    '''
    Return all the rows of 'tracker.csv' with the required 
    Habit as a dictionary
    '''
    rows = get_tracker_data(db, name)
    # print(rows)
    if not rows:
        return 0, 0

    # Returns: max_runstreak and total_attempts of a given Habit
    max_runstreak = max(r['runstreak'] for r in rows)
    total_attempts = sum(r['attempts'] for r in rows)

    return max_runstreak, total_attempts