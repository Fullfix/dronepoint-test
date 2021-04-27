import os
import logging
import time
import threading

from pymavlink import mavutil, mavwp
from pymavlink.mavutil import mavlink
import math
from .config import DronepointConfig
from .MavlinkListener import MavlinkListener
from .DronepointController import DronepointController

logging.basicConfig(level=logging.INFO)
wp = mavwp.MAVWPLoader()


class MavlinkController(DronepointConfig, MavlinkListener, DronepointController):
    def __init__(self):
        DronepointController.__init__(self)
        self.url = os.environ.get('MAVLINK_ENDPOINT', self.DRONE_CONNECTION)
        self.mavconn = mavutil.mavlink_connection(self.url, source_system=255)
        print('Drone initialized. Waiting for connection')
        self.mavconn.wait_heartbeat()
        print('Connected to Drone')
    
    def listen_drone_messages(self):
        thread_drone_msg = threading.Thread(target=self.receive_drone_messages)
        thread_drone_msg.start()
        print('Start Receiving Drone Messages')
    
    def set_home(self, homelocation, altitude):
        print('Setting Home')
        self.mavconn.mav.command_long_send(
            self.mavconn.target_system, self.mavconn.target_component,
            mavutil.mavlink.MAV_CMD_DO_SET_HOME,
            1, # set position
            0, # param1
            0, # param2
            0, # param3
            0, # param4
            homelocation[0], # lat
            homelocation[1], # lon
            altitude)
    
    def fly_sync(self):
        self.execute_flight()
        time.sleep(3)
        while self.ARMED:
            time.sleep(5)
            print('Flying')
        print('Finished Flight')
    
    def execute_flight(self):
        print('Initiating Flight Mission')
        wp.clear()
        # Frame
        frame = mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT
        p = mavlink.MAVLink_mission_item_message(
            self.mavconn.target_system,
            self.mavconn.target_component,
            0,
            mavlink.MAV_FRAME_MISSION,
            mavlink.MAV_CMD_DO_CHANGE_SPEED,
            0,
            1,
            0, 30, 0, 0,
            0,
            0,
            0,
        )
        wp.add(p)
        # Takeoff
        p = mavlink.MAVLink_mission_item_message(
            self.mavconn.target_system,
            self.mavconn.target_component,
            0,
            frame,
            mavlink.MAV_CMD_NAV_TAKEOFF,
            0,
            1,
            15, 0, 0, math.nan,
            self.POS[0],
            self.POS[1],
            self.FLIGHT_ALT,
        )
        wp.add(p)
        # Flight
        point = [self.POS[0] + self.FLIGHT_DISTANCE, self.POS[1]]
        p = mavlink.MAVLink_mission_item_message(
            self.mavconn.target_system,
            self.mavconn.target_component,
            1,
            frame,
            mavlink.MAV_CMD_NAV_WAYPOINT,
            0,
            1,
            0, 10, 0, math.nan,
            point[0],
            point[1],
            self.FLIGHT_ALT,
        )
        wp.add(p)
        # Land
        p = mavlink.MAVLink_mission_item_message(
            self.mavconn.target_system,
            self.mavconn.target_component,
            2,
            frame,
            mavlink.MAV_CMD_NAV_LAND,
            0,
            1,
            0, 0, 0, math.nan,
            self.POS[0],
            self.POS[1],
            0,
        )
        wp.add(p)

        # Send waypoints
        self.mavconn.waypoint_clear_all_send()
        self.mavconn.waypoint_count_send(wp.count())

        for i in range(wp.count()):
            msg = self.mavconn.recv_match(type=['MISSION_REQUEST'], blocking=True)
            print(msg)
            self.mavconn.mav.send(wp.wp(msg.seq))
            print(f'Sending waypoint {msg.seq}')

        # Start Mission
        time.sleep(1)
        self.mavconn.set_mode_auto()
        print('Started Mission')