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
        self.dp_url = config.DRONEPOINT_CONNECTION
        self.dp_state = config.STATE_STANDBY
        try:
            self.mavdp = mavutil.mavlink_connection(self.dp_url, source_system=255)
            print('Dronepoint initialized. Waiting for connection')
            self.mavdp.wait_heartbeat()
            print('here')
            print(self.mavdp.recv_match().to_dict())
            print('Connected to Dronepoint')
            thread_listen = threading.Thread(target=self.listen_messages)
            thread_listen.start()
            time.sleep(3)
            self.test_com()
        except BaseException as e:
            self.mavdp = None
            print('Failed to connect to Dronepoint')
            raise e
    
    def handle_message(self, msg):
        if msg['msgid'] == 0:
            state = msg['custom_mode']
            if self.dp_state != state:
                print(f'Changed DP State to {state}')
            self.dp_state = state
    
    def listen_messages(self):
        print('Start Watching Messages')
        while True:
            msg = self.mavdp.recv_match(blocking=True)
            msg_dict = msg.to_dict()
            msg_dict['msgid'] = msg.get_msgId()
            msg_dict['sysid'] = msg.get_srcSystem()
            msg_dict['compid'] = msg.get_srcComponent()
            del msg_dict['mavpackettype']
            # Convert NaN to None
            for key in msg_dict:
                if isinstance(msg_dict[key], float) and math.isnan(msg_dict[key]):
                    msg_dict[key] = None
            self.handle_message(msg_dict)

    def test_com(self):
        self.mavdp.mav.command_long_send(
            self.mavdp.target_system, 
            self.mavdp.target_component,
            mavlink.MAV_CMD_DO_SET_MODE,
            1,
            mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
            config.STATE_GETTING_FROM_USER,
            0,
            0,
            0,
            0,
            0,
        )
        print('SENT COMMAND')
        time.sleep(4)
        while True:
            if self.dp_state == config.STATE_STANDBY:
                break
            print('Executing Command')
            time.sleep(2)
        print('Command finished')

    def execute_command(self, mode, *args):
        self.mavdp.set_mode(
            mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
            mode,
            *args,
        )
        while True:
            # Wait for ACK command
            ack_msg = master.recv_match(type='COMMAND_ACK', blocking=True)
            ack_msg = ack_msg.to_dict()

            # Check if command in the same in `set_mode`
            if ack_msg['command'] != mavutil.mavlink.MAVLINK_MSG_ID_SET_MODE:
                continue

            # Print the ACK result !
            print(mavutil.mavlink.enums['MAV_RESULT'][ack_msg['result']].description)
            break

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
    