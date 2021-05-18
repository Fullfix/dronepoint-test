from mavlink.Mavlink import Mavlink
from mavlink.DronepointController import DronepointController
import socket
from pymavlink import mavutil, mavwp

def main():
    # mavlink = Mavlink()
    # mavlink.test_command()
    dp = DronepointController()
    dp.main()


if __name__ == '__main__':
    main()