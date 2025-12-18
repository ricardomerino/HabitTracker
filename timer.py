import threading
import time

from datetime import datetime, timedelta

class TimeEngine:
    '''
    Simulated time engine.
    Accelerates time for testing purposes, testing unite = 1 minute.
    - __init__(): Default speed: 10min/sec
    - start(): starts a background thread (Default: 10min/sec)
    - get_current_time(): returns the current simulated datetime
    
    Parameters:
    - start_time: initial datetime when clock starts
    - tick_minutes: number of minutes the simulated clock advances per tick
    - real_interval: seconds to wait between ticks in real time

    Libraries:
    - Threading: allow to execute tasks in parallel, waiting for user input. 
    https://docs.python.org/3/library/threading.html
    - Time: allow to create a TimeMachine that give a virtual time for testing the App
    https://docs.python.org/3/library/datetime.html

    Comments:
    - In order to allow the main menu while the timer is running it is necessary to introduce the Threading library.
    '''

    def __init__(self, start_time = None, tick_minutes: int = 10, real_interval: float = 1):
        # Initialize simulated time, if no start_time is provided, use the real current datetime.
        self.current_time = start_time or datetime.now()
        # how much simulated time advances per tick of clock. Default: 10min/sec
        self._tick = timedelta(minutes=tick_minutes)  
        # real time or tick of the clock
        self._real_interval = real_interval
        #  class threading.Event(): The flag is initially FALSE : (Event initially stopped)
        self._stop_event = threading.Event()
        self._thread = None # Reference to the background thread threading.Thread()

    def _run(self):
        '''
        Background code that make advance the TimeMachine at the 
        defined speed (60min/sec or Default: 10min/sec)
        '''
        while not self._stop_event.is_set():      # threading.Event().is_set() -> Return TRUE
            time.sleep(self._real_interval)       # wait for a real second to pass
            self.current_time += self._tick       # advance simulated time with defined speed.

            
    def start(self):
        if self._thread and self._thread.is_alive(): # .is_alive() -> Return True when run()
            return  # already running
        # threading.Event().clear () ->Reset the internal flag to FALSE (Subsequently threads)
        self._stop_event.clear() 
        # threading.Thread with targe that invokes .run() method
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def get_current_time(self):
        # returns the virtual time of TimeEngine to user
        return self.current_time 
        print(self.current_time)
