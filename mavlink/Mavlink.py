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
from .PrintObserver import observer

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

    # Validate if cell exists
    def validate_cell(self, cell):
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

    # Validate if it's possible to start test
    def validate_test(self, test_type):
        if test_type == 'drone':
            return self.drone_controller.connected
        elif test_type == 'dronepoint':
            return self.dronepoint_controller.connected
        elif test_type == 'full':
            return self.connected

    # Main Test
    def execute_test(self, cell, test_type):
        # Validate Cell
        if test_type != 'drone' and not self.validate_cell(cell):
            return observer.write(f"Can't start {test_type} test. Invalid Cell")

        # Validate Test Type
        if not self.validate_test(test_type):
            return observer.write(f"Can't start {test_type} Test. Drone or Dronepoint not connected")
        
        observer.write(f'Test Dronepoint type "{test_type}"')
        self.executing = True

        # Start Iteration depending on test type
        if test_type == 'drone':
            self.execute_flight()
        elif test_type == 'dronepoint':
            self.execute_iteration(cell, flight=False)
        elif test_type == 'full':
            self.execute_iteration(cell, flight=True)
        else:
            observer.write('Error. Invalid Test Type')

        self.executing = False
    
    def execute_flight(self):
        observer.write(f'Iteration flight started')
        start_time = time.time()

        self.drone_controller.execute_flight()

        observer.write(f'Flight Ended in {time.time() - start_time} s')

    # Iterate for one cell (x, y, z)
    def execute_iteration(self, cell, flight=False):
        # Debug
        observer.write(f'Iteration for cell ({cell[0]}, {cell[1]}, {cell[2]}) started')

        # Time Counter
        start_time = time.time()

        # Delay
        time.sleep(config.DRONEPOINT_DELAY)

        # Get from user
        time_get_from_user = self.dronepoint_controller.execute_command(
            config.STATE_GETTING_FROM_USER,
            cell[0], cell[1], cell[2],
        )
        # Delay
        time.sleep(config.DRONEPOINT_DELAY)

        # Load Drone
        time_load_drone = self.dronepoint_controller.execute_command(
            config.STATE_LOADING_DRONE,
            cell[0], cell[1], cell[2], 3
        )
        # Delay
        time.sleep(config.DRONEPOINT_DELAY)

        # Delay
        time.sleep(config.DRONEPOINT_DELAY)

        # Execute drone flight
        if flight:
            time_flight = self.drone_controller.execute_flight()
        else:
            time_flight = 0.0

        # Delay
        time.sleep(config.DRONEPOINT_DELAY)

        time_unload_drone = self.dronepoint_controller.execute_command(
            config.STATE_UNLOADING_DRONE,
            cell[0], cell[1], cell[2], 3
        )

        # Delay
        time.sleep(config.DRONEPOINT_DELAY)

        # Unload Drone
        time_unload_to_user = self.dronepoint_controller.execute_command(
            config.STATE_UNLOADING_TO_USER,
            cell[0], cell[1], cell[2],
        )

        # Delay
        time.sleep(config.DRONEPOINT_DELAY)

        time_total = time_get_from_user + time_load_drone + time_flight + time_unload_drone + time_unload_to_user

        # Debug
        observer.write(f'Iteration for cell ({cell[0]}, {cell[1]}, {cell[2]}) ended in {time.time() - start_time} s')

        # Final Message
        observer.write(f'Get From User: {round(time_get_from_user, 2)} s')
        observer.write(f'Load Drone: {round(time_load_drone, 2)} s')
        observer.write(f'Flight: {round(time_flight, 2)} s')
        observer.write(f'Unload Drone: {round(time_unload_drone, 2)} s')
        observer.write(f'Unload To User: {round(time_unload_to_user, 2)} s')
        observer.write(f'Total (no delay): {round(time_total, 2)} s')
        observer.write(f'Total: {round(time.time() - start_time, 2)} s')
    
    def test(self, cell, test_type):
        # Debug
        observer.write('Start Executing Test')
        # Start async thread for test execution
        thread_test = threading.Thread(target=self.execute_test, args=(cell, test_type))
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
            "drone_history": self.drone_controller.history,
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
            config.STATE_CLOSING: config.CLOSING,
            config.STATE_OPENING: config.OPENING,
        }
        if not self.dronepoint_controller.connected:
            return config.IDLE
        if self.dronepoint_controller.custom_mode in state_to_test.keys():
            return state_to_test[self.dronepoint_controller.custom_mode]
        return config.IDLE

if __name__ == '__main__':
    mavlink = Mavlink()