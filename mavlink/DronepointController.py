import os
import logging
import time
import threading

from pymavlink import mavutil, mavwp
from pymavlink.mavutil import mavlink
import math
from .config import DronepointConfig


class DronepointController():
    def dronepoint_action(self, mode, *args):
        try:
            # self.mavconn.mav.command_long_send(
            #     self.mavconn.target_system, 
            #     self.mavconn.target_component, 
            #     mavlink.MAV_CMD_DO_SET_MODE, 
            #     1, 
            #     mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED, 
            #     mode, 
            #     3, 0, 0, 0, 0)
            print('Dronepoint action executed successfully')
        except BaseException as e:
            print(e)
    
    def loading_drone_action(self):
        self.dronepoint_action(self.CUSTOM_MODE_LOADING_DRONE)
        time.sleep(10)
    
    def unloading_drone_action(self):
        self.dronepoint_action(self.CUSTOM_MODE_UNLOADING_DRONE)
        time.sleep(10)
    
    def unloading_to_user(self):
        self.dronepoint_action(self.CUSTOM_MODE_UNLOADING_TO_USER)
        time.sleep(10)
    
    def getting_from_user(self):
        self.dronepoint_action(self.CUSTOM_MODE_GETTING_FROM_USER)
        time.sleep(10)
    
    def taking_battery(self):
        self.dronepoint_action(self.CUSTOM_MODE_CHANGING_BATTERY)

    def giving_battery(self):
        self.dronepoint_action(self.CUSTOM_MODE_CHANGING_BATTERY)
    