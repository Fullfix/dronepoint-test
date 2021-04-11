import os
import logging
import time
import threading

from pymavlink import mavutil, mavwp
from pymavlink.mavutil import mavlink
import math
from MavlinkController import MavlinkController

def execute_test():
    mavlinkController = MavlinkController()
    mavlinkController.listen_drone_messages()

    time.sleep(3)
    mavlinkController.getting_from_user()
    mavlinkController.taking_battery()
    mavlinkController.loading_drone_action()

    mavlinkController.fly_sync()
    
    mavlinkController.unloading_drone_action()
    mavlinkController.giving_battery()
    mavlinkController.unloading_to_user()
    print('Test Executed')


# execute_test()