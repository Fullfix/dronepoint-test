import os
import logging
import time
import threading

from pymavlink import mavutil, mavwp
from pymavlink.mavutil import mavlink
import math
from .DroneController import DroneController
from .DronepointController import DronepointController
from .config import DronepointConfig as config

class Mavlink:
    def __init__(self):
        # Current state of execution
        self.state = config.IDLE
        # Mission Execution param (bool)
        self.executing = False
        # Drone Controller
        self.drone_controller = DroneController()
        # Dronepoint Controller
        self.dronepoint_controller = DronepointController()
    
    def execute_test(self):
        self.executing = True
        # Execute drone flight
        self.state = config.FLYING
        self.drone_controller.execute_flight()
        # Delay
        time.sleep(config.DRONEPOINT_DELAY)

        # Unload Drone
        self.state = config.UNLOADING_DRONE
        self.dronepoint_controller.execute_command(
            config.STATE_UNLOADING_DRONE,
            0, 3, 0, 3
        )
        # Delay
        time.sleep(config.DRONEPOINT_DELAY)

        # Unload to user
        self.state = config.UNLOADING_TO_USER
        self.dronepoint_controller.execute_command(
            config.STATE_UNLOADING_TO_USER,
            0, 3, 0,
        )
        # Delay
        time.sleep(config.DRONEPOINT_DELAY)

        # Get from user
        self.state = config.GETTING_FROM_USER
        self.dronepoint_controller.execute_command(
            config.STATE_GETTING_FROM_USER,
            0, 3, 0,
        )
        # Delay
        time.sleep(config.DRONEPOINT_DELAY)

        # Load Drone
        self.state = config.LOADING_DRONE
        self.dronepoint_controller.execute_command(
            config.STATE_LOADING_DRONE,
            0, 3, 0, 3
        )
        # Delay
        time.sleep(config.DRONEPOINT_DELAY)

        # Execute drone flight again
        self.state = config.FLYING
        self.drone_controller.execute_flight()

        # Debug
        print('Test Executed')
        
        # Return to IDLE
        self.state = config.IDLE
        self.executing = False
    
    def test(self):
        # Start async thread for test execution
        thread_test = threading.Thread(target=self.execute_test)
        thread_test.start()
        # Debug
        print('Start Executing Test')
    
    # Retrieve drone & dronepoint data
    def get_data(self):
        return {
            "pos": self.drone_controller.pos,
            "alt": self.drone_controller.alt,
            "armed": self.drone_controller.armed,
            "landing_state": self.drone_controller.landed_state,
            "executing": self.executing,
            "state": self.state,
            "dronepoint_pos": [config.DRONEPOINT_LAT, config.DRONEPOINT_LON]
        }

if __name__ == '__main__':
    mavlink = Mavlink()