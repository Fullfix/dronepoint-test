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
        # Mission Execution param (bool)
        self.executing = False
        # Drone Controller
        self.drone_controller = DroneController()
        # Dronepoint Controller
        self.dronepoint_controller = DronepointController()

    @property
    def connected(self):
        return self.drone_controller.connected and self.dronepoint_controller.connected

    # Main Test
    def execute_test(self, cell):
        self.executing = True
        
        self.execute_iteration(cell)

        self.executing = False

    # Iterate for one cell (x, y, z)
    def execute_iteration(self, cell):
        # Debug
        print(f'Iteration for cell ({cell[0]}, {cell[1]}, {cell[2]}) started')

        # Time Counter
        start_time = time.time()

        # # Get from user
        # self.dronepoint_controller.execute_command(
        #     config.STATE_GETTING_FROM_USER,
        #     cell[0], cell[1], cell[2],
        # )
        # # Delay
        # time.sleep(config.DRONEPOINT_DELAY)

        # # Load Drone
        # self.dronepoint_controller.execute_command(
        #     config.STATE_LOADING_DRONE,
        #     cell[0], cell[1], cell[2], 3
        # )
        # # Delay
        # time.sleep(config.DRONEPOINT_DELAY)

        # Execute drone flight
        self.drone_controller.execute_flight()

        # # Delay
        # time.sleep(config.DRONEPOINT_DELAY)

        # # Unload Drone
        # self.dronepoint_controller.execute_command(
        #     config.STATE_UNLOADING_DRONE,
        #     cell[0], cell[1], cell[2], 3
        # )
        # # Delay
        # time.sleep(config.DRONEPOINT_DELAY)

        # # Unload to user
        # self.dronepoint_controller.execute_command(
        #     config.STATE_UNLOADING_TO_USER,
        #     cell[0], cell[1], cell[2],
        # )
        # Delay
        time.sleep(config.DRONEPOINT_DELAY)

        # Debug
        print(f'Iteration for cell ({cell[0]}, {cell[1]}, {cell[2]}) ended in {time.time() - start_time} s')
    
    def test(self, cell):
        # Debug
        print('Start Executing Test')
        # Start async thread for test execution
        thread_test = threading.Thread(target=self.execute_test, args=(cell,))
        thread_test.start()
    
    # Retrieve drone & dronepoint data
    def get_data(self):
        return {
            "pos": self.drone_controller.pos,
            "alt": self.drone_controller.alt,
            "armed": self.drone_controller.armed,
            "landing_state": self.drone_controller.landed_state,
            "executing": self.executing,
            "state": self.get_state(),
            "dronepoint_pos": [config.DRONEPOINT_LAT, config.DRONEPOINT_LON],
            "connection": {
                "drone": self.drone_controller.connected,
                "dronepoint": self.dronepoint_controller.connected,
            },
        }
    
    # Dynamically get state of test
    def get_state(self):
        # Check flight
        if self.drone_controller.connected and self.drone_controller.armed:
            return config.FLYING
        # Check dronepoint states
        state_to_test = {
            config.STATE_GETTING_FROM_USER: config.GETTING_FROM_USER,
            config.STATE_LOADING_DRONE: config.LOADING_DRONE,
            config.STATE_UNLOADING_DRONE: config.UNLOADING_DRONE,
            config.STATE_UNLOADING_TO_USER: config.UNLOADING_TO_USER,
            config.STATE_STANDBY: config.IDLE,
        }
        if not self.dronepoint_controller.connected:
            return config.IDLE
        if self.dronepoint_controller.custom_mode in state_to_test.keys():
            return state_to_test[self.dronepoint_controller.custom_mode]
        return config.IDLE
    
    def check_cell(self, cell):
        x, y, z = cell
        if y == 3:
            if x < 0 or x > 4:
                return False
            if z < 0 or z > 6:
                return False
            if (
                x == 1 and z == 1 or
                x == 3 and z == 1 or
                x == 1 and z == 2 or
                x == 2 and z == 2 or
                x == 3 and z == 2 or
                x == 1 and z == 3 or
                x == 2 and z == 3 or
                x == 3 and z == 3 ):
                return False
        elif y == 2:
            return False
        else:
            return False
        return True

if __name__ == '__main__':
    mavlink = Mavlink()