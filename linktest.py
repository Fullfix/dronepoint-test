# import os
# import logging
# import time
# import threading

# from pymavlink import mavutil, mavwp
# from pymavlink.mavutil import mavlink
# import math

# dp_url = 'udpin:192.168.194.103:14550'

# mavconn = mavutil.mavlink_connection(dp_url, source_system=255)
# print('Connected')

# print(mavconn.recv_match().to_dict())
import socket
def test_host():
    server = socket.socket()
    print(socket.gethostname())
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('192.168.194.103', 14590))
    server.listen(4)
    client_socket, client_address = server.accept()
    print(client_address, "has connected")
    while 1==1:
        recvieved_data = client_socket.recv(1024)
        print(recvieved_data)

test_host()