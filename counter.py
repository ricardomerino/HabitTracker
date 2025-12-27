# counter.py
from db import add_counter, increment_tracker, get_tracker_data
from datetime import datetime, timedelta, date

class Counter:
    def __init__(self, name:str, description: str, frequence: str):
        '''Counter class, to count events 
        :param name: the name of the counter 
        :param description: the description of the counter ''' 
        self.name = name
        self.description = description
        self.frequence = frequence
                
    def store(self, db):
        add_counter(db, self.name, self.description, self.frequence)
        
    def add_event(self, db, event_date = None):
        # Register one increment event in the database
        if event_date:
            event_day = event_date
        else:
            event_day = date.today()
        
        # Previous represents all previous rows in 'tracker.csv'
        previous = get_tracker_data(db, self.name)

        freq_value = int(self.frequence)

        if previous:
            last = previous[-1] # format: str 'YYYY-MM-DD'
            # Transform the last recorded date string in date format: (YYYY, MM, DD)
            last_day = datetime.strptime(last['date'], '%Y-%m-%d').date()
            # Extract last runstreak and attempts values from the last dictionary
            last_runstreak = int(last.get('runstreak', 0))
            # print(last_runstreak) to debug
            last_attempts = int(last.get('attempts', 1))
            # print(last_attempts) to debug
            days_since_last = (event_day - last_day).days
            # print(days_since_last) to debug
    
            if days_since_last <= freq_value:
                # check-off Habit in the defined frequence. Good done!
                print('Good job! Habit maintained!')
                new_runstreak = last_runstreak + 1
                new_attempts = last_attempts
            else:
                # Habit broken in the defined frequence. Keep on trying!
                print('Habit broken, but keep on trying!')
                new_runstreak = 1
                new_attempts = last_attempts + 1
        else:
            # 1st runstreak and 1st attempt recorded
            print('First time habit is being recorded!')
            new_runstreak = 1
            new_attempts = 1
    
        # call db.py and save in 'tracker.csv' : date, runstreak, attempts
        increment_tracker(db, self.name, event_date=event_day.isoformat(),
                          runstreak=new_runstreak, attempts=new_attempts)