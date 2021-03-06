import os
import logging
from socket import timeout
import time
import threading

from pymavlink import mavutil, mavwp
from pymavlink.mavutil import mavlink
import math
from .config import DronepointConfig as config
from .PrintObserver import observer

# Initialize waypoint
wp = mavwp.MAVWPLoader()

class DroneController:
    def __init__(self):
        # Drone connection url
        url = config.DRONE_CONNECTION
        # Is connected
        self.connected = False
        # Listen messages
        self.listening = True
        # Drone parameters
        self.pos = [0, 0]
        self.alt = 0
        self.armed = False
        self.landed_state = 0
        # History of position
        self.history = []
        # Mavlink message handlers
        self.handlers = {
            mavlink.MAVLINK_MSG_ID_GLOBAL_POSITION_INT: self.GLOBAL_POSITION_INT_HANDLER,
            mavlink.MAVLINK_MSG_ID_EXTENDED_SYS_STATE: self.EXTENDED_SYS_STATE_HANDLER,
            mavlink.MAVLINK_MSG_ID_HEARTBEAT: self.HEARTBEAT_HANDLER,
            mavlink.MAVLINK_MSG_ID_GPS_RAW_INT: self.GLOBAL_POSITION_INT_HANDLER,
        }
        self.mavconn = mavutil.mavlink_connection(url, source_system=255)
        # Debug
        observer.write(f'Drone initialized {url}. Waiting for connection')
        # Start sending heartbeat
        thread_send = threading.Thread(target=self.send_heartbeats)
        thread_send.start()
        # Start listening mavlink messages
        thread_listen = threading.Thread(target=self.listen_messages)
        thread_listen.start()
        # Cooldown
        time.sleep(1)
    
    # Listen for mavlink messages and apply message handlers
    def listen_messages(self):
        observer.write('Started watching messages')
        while True:
            if not self.listening:
                time.sleep(1)
                continue
            msg = self.mavconn.recv_match(blocking=True, timeout=config.DRONE_CONNECTION_TIMEOUT)
            # Check if msg is None
            if not msg:
                # Set state to disconnected
                if self.connected == True:
                    # Debug
                    observer.write('Drone disconnected')
                self.connected = False
                continue
            else:
                if self.connected == False:
                    # Debug
                    observer.write('Drone connected')
                # Set state to connected
                self.connected = True
            # Style messages
            msg_dict = msg.to_dict()
            msg_dict['msgid'] = msg.get_msgId()
            msg_dict['sysid'] = msg.get_srcSystem()
            msg_dict['compid'] = msg.get_srcComponent()
            del msg_dict['mavpackettype']
            # Convert NaN to None
            for key in msg_dict:
                if isinstance(msg_dict[key], float) and math.isnan(msg_dict[key]):
                    msg_dict[key] = None
            # Check if handler exists
            if msg_dict['msgid'] in self.handlers.keys():
                # Execute handlers
                self.handlers[msg_dict['msgid']](msg_dict)
            # if msg_dict['msgid'] in range(37, 48):
            #     observer.write('TRAITOR')
            #     observer.write(msg_dict['msgid'])
            # if msg_dict['msgid'] == 47:
            #     observer.write(f'mission ack {msg_dict["type"]}')
            #     observer.write(msg.get_type())
    
    # Send random heartbeats to receive messages from Drone
    def send_heartbeats(self):
        while True:
            self.mavconn.mav.heartbeat_send(
                0,
                0,
                0,
                0,
                0,
            )
            time.sleep(0.5)
    
    # Global position int listener: update drone's position
    def GLOBAL_POSITION_INT_HANDLER(self, msg_dict):
        # Get GPS Position
        pos = [msg_dict['lat'] / 10000000, msg_dict['lon'] / 10000000]

        # Check if Difference is big enough
        last_pos = self.history[-1] if len(self.history) > 0 else self.pos[:]
        pos_difference = [abs(pos[i] - last_pos[i]) * 10000000 for i in range(len(pos))]
        alt = msg_dict['alt'] / 1000
        alt_difference = abs(self.alt - alt)
        self.pos = pos[:]
        self.alt = alt
        # If difference is big enough, update history
        if pos_difference[0] > config.MIN_POS_DIFFERENCE or pos_difference[1] > config.MIN_POS_DIFFERENCE:
            self.history.append(pos[:])
        # observer.write(f'Update pos to {self.pos[0]} {self.pos[1]} {self.alt}')
    
    # Heartbeat listener: update drone's state (armed)
    def HEARTBEAT_HANDLER(self, msg_dict):
        self.armed = msg_dict["system_status"] == 4
    
    # Extended sys state listener: update drone's landed_state
    def EXTENDED_SYS_STATE_HANDLER(self, msg_dict):
        # Get landed state
        landed_state = msg_dict['landed_state']
        # Check if different from previous
        if landed_state != self.landed_state:
            self.landed_state = landed_state
            observer.write(f"Updated Landed State to {landed_state}")
    
    # Set home
    def set_home(self, homelocation, altitude):
        observer.write('Setting Home')
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
    
    def execute_flight(self):
        # Clear old history
        self.history = [self.pos[:]]
        # Start mission
        self.start_flight_mission()
        # Cooldown
        time.sleep(3)
        # Time Counter
        start_time = time.time()

        while self.armed:
            # Debug
            time.sleep(5)
            observer.write('Flying')
        # Debug
        observer.write(f'Finished Flight in {time.time() - start_time} s')
        return time.time() - start_time

    # Initiate flight mission
    def start_flight_mission(self):
        observer.write('Initiating Flight Mission')
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
            self.pos[0],
            self.pos[1],
            config.FLIGHT_ALT,
        )
        wp.add(p)
        # Flight
        point = [self.pos[0] + config.FLIGHT_DISTANCE, self.pos[1]]
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
            config.FLIGHT_ALT,
        )
        wp.add(p)
        point = [self.pos[0] + config.FLIGHT_DISTANCE, self.pos[1] + config.FLIGHT_DISTANCE]
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
            config.FLIGHT_ALT,
        )
        wp.add(p)
        point = [self.pos[0], self.pos[1] + config.FLIGHT_DISTANCE]
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
            config.FLIGHT_ALT,
        )
        wp.add(p)
        point = [self.pos[0], self.pos[1]]
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
            config.FLIGHT_ALT,
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
            0, 
            0, # Precision land mode 
            0, 
            math.nan, # Angle
            self.pos[0], # Lat 
            self.pos[1], # Lon
            0, # Alt
        )
        wp.add(p)

        self.listening = False

        # Send waypoints
        self.mavconn.waypoint_clear_all_send()
        self.mavconn.waypoint_count_send(wp.count())

        for i in range(wp.count()):
            msg = self.mavconn.recv_match(type=['MISSION_REQUEST'], blocking=True)
            observer.write(msg)
            self.mavconn.mav.send(wp.wp(msg.seq))
            observer.write(f'Sending waypoint {msg.seq}')

        # Start Mission
        self.listening = True
        time.sleep(1)
        self.mavconn.set_mode_auto()
        observer.write('Started Mission')
