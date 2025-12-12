# timer.py
# https://docs.python.org/3/library/datetime.html

import time
from datetime import datetime, timedelta

class TimeEngine:
    """
    A simulated time engine that increases time in fixed steps (default: 60 seconds).
    The time progression is shown only when user ask it (also for testing the TimeEngine).
    """

    def __init__(self, step: int = 60):
        self.current_time = datetime.now()  # Initial simulated time
        self.step = timedelta(seconds=step)  # Time increment size = 60 seconds
        #self.step = timedelta(minutes=step)  # Time increment size = 60 minutes
        self.running = False

    def start(self):
        """
        Start the time engine loop. It updates the current simulated time
        each second in real-time until the user presses Ctrl+C.
        """
        print("Starting time engine. Press CTRL + C to stop.")
        self.running = True

        try:
            while self.running:
                time.sleep(1)  # Wait one second in real time
                self.current_time += self.step  # Advance simulated time
                # For testing the time progression
                # print(f"Simulated time → {self.current_time}") 

        except KeyboardInterrupt:
            print("Time engine stopped.")
            self.running = False
