import os
import logging
import time
import threading

from pymavlink import mavutil, mavwp
from pymavlink.mavutil import mavlink
import math
from .config import DronepointConfig as config


class DronepointController:
    def __init__(self):
        # Dronepoint connection url
        url = config.DRONEPOINT_CONNECTION
        # Dronepoint current custom mode
        self.custom_mode = config.STATE_STANDBY
        # Mavlink message handlers
        self.handlers = {
            0: self.handle_heartbeat
        }
        try:
            self.mavconn = mavutil.mavlink_connection(url, source_system=255)
            # Debug
            print('Dronepoint initialized. Waiting for connection')
            # Wait heartbeat
            self.mavconn.wait_heartbeat()
            # Debug 
            print(self.mavconn.recv_match().to_dict())
            print('Connected to Dronepoint')
            # Start listening mavlink messages
            thread_listen = threading.Thread(target=self.listen_messages)
            thread_listen.start()
            # Cooldown
            time.sleep(1)
            self.main()
        except BaseException as e:
            self.mavconn = None
            # Debug
            print('Failed to connect to Dronepoint')
            raise e
    
    # Test code
    def main(self):
        self.execute_command(
            config.STATE_LOADING_DRONE, 0, 
            2, 2, 2
        )
    
    # Listen for mavlink messages and apply message handlers
    def listen_messages(self):
        print('Started watching messages')
        while True:
            msg = self.mavconn.recv_match(blocking=True)
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

    # Execute Dronepoint command via command long
    def execute_command(self, mode, submode=0, param1=0, param2=0, param3=0):
        # Send command
        self.mavconn.mav.command_long_send(
            self.mavconn.target_system,
            self.mavconn.target_component,
            mavlink.MAV_CMD_DO_SET_MODE,
            1,
            mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
            mode,
            submode,
            param1, param2, param3,
            0,
        )
        
        # Wait until dronepoint custom_mode is in STANDBY mode (12)
        time.sleep(1)
        while True:
            i = 1
            if self.custom_mode == config.STATE_STANDBY:
                break
            # Debug
            if i % 10 == 0:
                print('Executing command')
            # Cooldown
            time.sleep(1)
        # Debug
        print('Command finished')
    
    # Heartbeat listener (0): update dronepoint's custom mode
    def handle_heartbeat(self, msg):
        state = msg['custom_mode']
        if self.custom_mode != state:
            self.custom_mode = state
            # Debug
            print(f'Changed to custom mode {state}')