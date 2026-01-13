# main.py
# learning notes

import sys
sys.path.append('_DataBase')  # Add database folder to Python path so imports work correctly
import questionary  # Library used for CLI user prompts
import importlib
import pandas as pd

import db
importlib.reload(db)

from db import (
    get_db,
    get_tracker_data,
    get_counter_frequence,
    display_table,
    modify_habit,
    erase_habit
)
from counter import Counter
from analyse import analyse_menu
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
    
# Open or create the database
    db_instance = get_db()
    # Prepare the Task data in a intuitive Table for the user
    # db_display = display_table(db_instance)
    # display_tasks = pd.DataFrame(db_display)

    # Setup the TimeEngine
    time_engine = TimeEngine(tick_minutes=60, real_interval=1)

    # Starts the Main 
    questionary.confirm('Are you ready?').ask()  # Ask user to start

    stop = False

    while not stop:
        # Transform with Pandas the 'db_instance' date into an intuitive Table for the user
        db_display = display_table(db_instance)
        display_tasks = pd.DataFrame(db_display)

        # Present choices to the user using questionary
        choice = questionary.select(
            f'What do you want to do?',
            choices=['Habits', 'Increment', 'Analyse', 'Run Time Engine', 'Display Virtual Time', 'Exit']
        ).ask()

        if choice == 'Habits':
            # submenu for Habits
            h_choice = questionary.select(
                'Habits - what do you want?',
                choices=['Create', 'Modify', 'Erase', 'Back']
            ).ask()

            if h_choice == 'Create':
                # Displays the Table of the Tasks in a intuitive way
                print(f'These are the Habits you have already introduced\n\n{display_tasks}\n\n')
                # Requests the Name, Description and Frequence for the Habit
                name = questionary.text("What's the name of your Habit?").ask()
                desc = questionary.text("What's the description of your Habit?").ask()
                freq = questionary.text("What's the frequency in days you want to achieve?").ask()
                # Call 
                counter = Counter(name, desc, int(freq))
                counter.store(db_instance)

            elif h_choice == 'Modify':
                # Displays the Table of the Tasks in a intuitive way
                print(f'Which Habits you want to modify\n\n{display_tasks}\n\n')
                # Requests the Name, Description and Frequence for the Habit
                old_name = questionary.text("What's the CURRENT name of the Habit?").ask()
                new_name = questionary.text("What's the NEW name of the Habit?").ask()
                desc = questionary.text("What's the NEW description of your Habit?").ask()
                freq = questionary.text("What's the NEW frequency in days?").ask()

                modify_habit(
                    db_instance,
                    old_name=old_name,
                    new_name=new_name,
                    new_description=desc,
                    new_frequence=int(freq)
                )

                print(f"Habit '{old_name}' modified successfully.")

            elif h_choice == 'Erase':
                # Displays the Table of the Tasks in a intuitive way
                print(f'Which Habits you want to erase\n\n{display_tasks}\n\n')
                name = questionary.text("What's the name of the Habit you want to erase?").ask()
                confirm = questionary.confirm(
                    f"Are you sure you want to permanently erase '{name}'?\n"
                    f"All history will be lost."
                ).ask()

                if confirm:
                    erase_habit(db_instance, name)
                    print(f"Habit '{name}' erased successfully.") 

            # 'Back' goes back to the main menu

        elif choice == 'Increment':
            # Displays the Table of the Tasks in a intuitive way
            print(f'These are the habits you can complete now\n\n{display_tasks}\n\n')
            # Increment and register the event in database
            name = questionary.text("What's the name of your counter?").ask()
            
            freq = get_counter_frequence(db_instance, name)
            counter = Counter(name, 'temporary description', freq) 
            # Add row to tracker table
            counter.add_event(db_instance, time_engine.get_current_time().date())

            accoplished_data = get_tracker_data(db_instance, name)
            last = accoplished_data[-1]

            print(
                f"Habit '{name}' incremented successfully \n"
                f"Runstreak: {last['runstreak']}\n"
                f"Attempts: {last['attempts']}"
            )

        elif choice == 'Analyse':
            # call submenu for Anlyse
            analyse_menu(db_instance)

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