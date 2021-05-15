from mavlink.Mavlink import Mavlink
from mavlink.DronepointController import DronepointController
import socket
from pymavlink import mavutil, mavwp

def main():
    # mavlink = Mavlink()
    # mavlink.test_command()
    # dp = DronepointController()
    # dp.main()
    url = 'udpout:192.168.194.9:14590'
    mavconn = mavutil.mavlink_connection(url, source_system=255)


if __name__ == '__main__':
    main()