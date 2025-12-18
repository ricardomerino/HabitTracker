# main.py
# learning notes

import sys
sys.path.append('_DataBase')  # Add database folder to Python path so imports work correctly
import questionary  # Library used for CLI user prompts
import importlib
import pandas as pd

import db
importlib.reload(db)

from db import get_db, get_tracker_data, get_counter_frequence
from counter import Counter
from analyse import calculate_count
from timer import TimeEngine


def cli():
    """
    Command-line interface for interacting with the Habit Tracker.
    This function loops until the user chooses to exit.
    """
    
    # Open or create the database
    db_instance = get_db()  

    # Configurates the time simulation engine (60min/sec)
    time_engine = TimeEngine(tick_minutes=60, real_interval=1)
    # time_engine = TimeEngine() # Default 10min/sec
    # Defines an Example Table with 5 Habits with 3 different Frequences
    for i in range(5):
        example = {
            'Habit': ['read', 'podcast', 'bike', 'shopping', 'series'],
            'Description': ['finish a book', 'lisen culture', 'use it', 
            'buy groceries', 'watch it'],
            'Frequence (days)': ['30', '1', '1', '3', '3'],
    }
    df = pd.DataFrame(example)
    print(f'Example of Habits\n\n{df}\n\n Welcome to the Habit Tracker CLI!')
    questionary.confirm('Are you ready?').ask()  # Ask user to start

    stop = False

    while not stop:
        # Present choices to the user using questionary
        choice = questionary.select(
            f'What do you want to do?',
            choices=['Create', 'Increment', 'Analyse', 'Run Time Engine', 
            'Display Virtual Time', 'Exit']
        ).ask()

        if choice == 'Create':
            # Ask for description and store a new counter in DB
            name = questionary.text("What's the name of your Habit?").ask()
            desc = questionary.text("What's the description of your Habit?").ask()
            freq = questionary.text("What frequency in days you want to achieve this Habit?").ask()
            counter = Counter(name, desc, freq)  # Create object
            counter.store(db_instance)  # Save to database

        elif choice == 'Increment':
            # Increment and register the event in database
            name = questionary.text("What's the name of your counter?").ask()
            
            freq = get_counter_frequence(db_instance, name)
            counter = Counter(name, 'temporary description', freq) 
            # Add row to tracker table
            counter.add_event(db_instance, time_engine.get_current_time().date())

            data = get_tracker_data(db_instance, name)
            last = data[-1]

            print(
                f"Habit '{name}' incremented successfully \n"
                f"Runstreak: {last['runstreak']}\n"
                f"Attempts: {last['attempts']}"
            )

        elif choice == 'Analyse':
            # Count events related to chosen counter
            name = questionary.text("What's the name of your counter?").ask()
            max_runstreak, total_attempts = calculate_count(db_instance, name)
            print(f'{name} has been maintained a max runstreak of {max_runstreak} '
                  f'in a total of {total_attempts} attempts')

        elif choice == 'Run Time Engine':
            # Start simulated time progression
            time_engine.start()  # Calls internal loop until user stops the engine
            print(time_engine.get_current_time())  # Display current simulated time

        elif choice == 'Display Virtual Time':
            # Displayd current simulated time
            print(time_engine.get_current_time())  # Display current simulated time

        else:
            print('Bye!')
            stop = True


if __name__ == '__main__':
    cli()