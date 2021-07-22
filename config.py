from dotenv import dotenv_values

config = dotenv_values('.env')
PASSWORD = config['SECRET_CODE']
DRONEPOINT_CONNECTION = config['DRONEPOINT_CONNECTION']
DRONE_CONNECTION = config['DRONE_CONNECTION']