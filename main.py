# main.py 
import sys
sys.path.append('_DataBase') 
import questionary 
import importlib

import db

importlib.reload(db) 
from db import get_db
from counter import Counter
from analyse import calculate_count

def cli():
    db = get_db()
    questionary.confirm('Are you ready?').ask()
    stop = False
    choice = questionary.select(
        'What do you want to do?',
        choices = ['Create', 'Increment', 'Analyse', 'Exit'] 
    ).ask()
    
    name = questionary.text('What\'s the name of your counter?').ask()
    
    if choice == 'Create':
        desc = questionary.text('What\'s the description of your counter?').ask()
        counter = Counter(name, desc)
        counter.store(db)
        
    elif choice == 'Increment':
        counter = Counter(name, 'no description')
        counter.increment()
        counter.add_event(db)
        
    elif choice == 'Analyse':
        count = calculate_count(db, name)
        print(f'{name} has been incremented {count} times')
        
    else:
        print('Bye!') 
        stop = True
    
if __name__ == '__main__':
    cli()