# main.py
# learning notes

import sys
sys.path.append('_DataBase')  # Add database folder to Python path so imports work correctly
import questionary  # Library used for CLI user prompts
import importlib
importlib.reload(db)

import db

from db import get_db
from counter import Counter
from analyse import calculate_count
from timer import TimeEngine


def cli():
    """
    Command-line interface for interacting with the Habit Tracker.
    This function loops until the user chooses to exit.
    """

    db = get_db()  # Open or create the database
    engine = TimeEngine()  # The time simulation engine
    questionary.confirm('Are you ready?').ask()  # Ask user to start

    stop = False

    while not stop:
        # Present choices to the user using questionary
        choice = questionary.select(
            'What do you want to do?',
            choices=['Create', 'Increment', 'Analyse', 'Run Time Engine', 'Exit']
        ).ask()

        if choice == 'Create':
            # Ask for description and store a new counter in DB
            name = questionary.text("What's the name of your counter?").ask()
            desc = questionary.text("What's the description of your counter?").ask()
            counter = Counter(name, desc)  # Create object
            counter.store(db)  # Save to database

        elif choice == 'Increment':
            # Increment and register the event in database
            name = questionary.text("What's the name of your counter?").ask()
            counter = Counter(name, 'temporary description')
            counter.increment()  # Increase internal counter
            counter.add_event(db)  # Add row to tracker table

        elif choice == 'Analyse':
            # Count events related to chosen counter
            name = questionary.text("What's the name of your counter?").ask()
            count = calculate_count(db, name)
            print(f'{name} has been incremented {count} times')

        elif choice == 'Run Time Engine':
            # Start simulated time progression
            engine.start()  # Calls internal loop until user stops the engine

        else:
            print('Bye!')
            stop = True


if __name__ == '__main__':
    cli()