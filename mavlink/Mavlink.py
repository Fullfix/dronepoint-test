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

    # Main Test
    def execute_test(self):
        self.executing = True

        cell = [0, 3, 0]
        self.execute_iteration(cell)

        self.executing = False

    # Iterate for one cell (x, y, z)
    def execute_iteration(self, cell):
        # Debug
        print(f'Iteration for cell ({cell[0]}, {cell[1]}, {cell[2]}) started')

        # Time Counter
        start_time = time.time()

        # Get from user
        self.state = config.GETTING_FROM_USER
        self.dronepoint_controller.execute_command(
            config.STATE_GETTING_FROM_USER,
            cell[0], cell[1], cell[2],
        )
        # Delay
        time.sleep(config.DRONEPOINT_DELAY)

        # Load Drone
        self.state = config.LOADING_DRONE
        self.dronepoint_controller.execute_command(
            config.STATE_LOADING_DRONE,
            cell[0], cell[1], cell[2], 3
        )
        # Delay
        time.sleep(config.DRONEPOINT_DELAY)

        # Execute drone flight again
        self.state = config.FLYING
        self.drone_controller.execute_flight()

        # Delay
        time.sleep(config.DRONEPOINT_DELAY)

        # Unload Drone
        self.state = config.UNLOADING_DRONE
        self.dronepoint_controller.execute_command(
            config.STATE_UNLOADING_DRONE,
            cell[0], cell[1], cell[2], 3
        )
        # Delay
        time.sleep(config.DRONEPOINT_DELAY)

        # Unload to user
        self.state = config.UNLOADING_TO_USER
        self.dronepoint_controller.execute_command(
            config.STATE_UNLOADING_TO_USER,
            cell[0], cell[1], cell[2],
        )
        # Delay
        time.sleep(config.DRONEPOINT_DELAY)

        # Debug
        print(f'Iteration for cell ({cell[0]}, {cell[1]}, {cell[2]}) ended in {time.time() - start_time} s')
        
        # Return to IDLE
        self.state = config.IDLE
    
    def test(self):
        # Debug
        print('Start Executing Test')
        # Start async thread for test execution
        thread_test = threading.Thread(target=self.execute_test)
        thread_test.start()
    
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