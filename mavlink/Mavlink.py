import os
import logging
import time
import threading

from pymavlink import mavutil, mavwp
from pymavlink.mavutil import mavlink
import math
from .MavlinkController import MavlinkController
from .config import DronepointConfig as config

class Mavlink(MavlinkController):
    def __init__(self):
        super().__init__()
        self.listen_drone_messages()
        self.EXECUTING = False
        self.STATE = config.IDLE
    
    def test_command(self):
        print('TEST')
    
    def execute_test(self):
        self.EXECUTING = True
        self.STATE = config.GETTING_FROM_USER
        self.getting_from_user()
        self.STATE = config.TAKING_BATTERY
        self.taking_battery()
        self.STATE = config.LOADING_DRONE
        self.loading_drone_action()

        self.STATE = config.FLYING
        self.fly_sync()
        
        self.STATE = config.UNLOADING_DRONE
        self.unloading_drone_action()
        self.STATE = config.GIVING_BATTERY
        self.giving_battery()
        self.STATE = config.UNLOADING_TO_USER
        self.unloading_to_user()
        print('Test Executed')
        self.STATE = config.IDLE
        self.EXECUTING = False
    
    def test(self):
        thread_test = threading.Thread(target=self.execute_test)
        thread_test.start()
        print('Start Executing Test')
    
    def get_data(self):
        return {
            "pos": self.POS,
            "alt": self.ALT,
            "armed": self.ARMED,
            "landing_state": self.LANDING_STATE,
            "executing": self.EXECUTING,
            "state": self.STATE,
        }

if __name__ == '__main__':
    mavlink = Mavlink()