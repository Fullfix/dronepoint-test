import os
import logging
import time
import threading

from pymavlink import mavutil, mavwp
from pymavlink.mavutil import mavlink
import math

class MavlinkListener:
    POS = [0, 0]
    ALT = 0
    ARMED = False
    LANDING_STATE = 0

    def receive_drone_messages(self):
        print('Start Watching Messages')
        while True:
            msg = self.mavconn.recv_match(blocking=True)
            msg_dict = msg.to_dict()
            msg_dict['msgid'] = msg.get_msgId()
            msg_dict['sysid'] = msg.get_srcSystem()
            msg_dict['compid'] = msg.get_srcComponent()
            del msg_dict['mavpackettype']
            # Convert NaN to None
            for key in msg_dict:
                if isinstance(msg_dict[key], float) and math.isnan(msg_dict[key]):
                    msg_dict[key] = None
            self.handle_drone_message(msg_dict)
    
    def handle_drone_message(self, msg_dict):
        if msg_dict['msgid'] == mavlink.MAVLINK_MSG_ID_GLOBAL_POSITION_INT:
            self.GLOBAL_POSITION_INT_HANDLER(msg_dict)
        elif msg_dict['msgid'] == mavlink.MAVLINK_MSG_ID_EXTENDED_SYS_STATE:
            self.EXTENDED_SYS_STATE_HANDLER(msg_dict)
        elif msg_dict['msgid'] == mavlink.MAVLINK_MSG_ID_HEARTBEAT:
            self.HEARTBEAT_HANDLER(msg_dict)

    def GLOBAL_POSITION_INT_HANDLER(self, msg_dict):
        # Get GPS Position
        pos = [msg_dict['lat'] / 10000000, msg_dict['lon'] / 10000000]

        # Check if Difference is big enough
        pos_difference = [abs(pos[i] - self.POS[i]) * 10000000 for i in range(len(pos))]
        alt = msg_dict['alt'] / 1000
        alt_difference = abs(self.ALT - alt)
        if pos_difference[0] > 5 or pos_difference[1] > 5 or alt_difference >= 1:
            self.POS = pos[:]
            self.ALT = alt
            print(f'Update pos to {self.POS[0]} {self.POS[1]} {self.ALT}')
    
    def HEARTBEAT_HANDLER(self, msg_dict):
        self.ARMED = msg_dict["system_status"] == 4
    
    def EXTENDED_SYS_STATE_HANDLER(self, msg_dict):
        # Get landed state
        landed_state = msg_dict['landed_state']
        # Check if different from previous
        if landed_state != self.LANDING_STATE:
            self.LANDING_STATE = landed_state
            print(f"Updated Landed State to {landed_state}")