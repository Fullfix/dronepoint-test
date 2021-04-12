class DronepointConfig:
    # Modes
    CUSTOM_MODE_LOADING_DRONE = 5
    CUSTOM_MODE_UNLOADING_DRONE = 6
    CUSTOM_MODE_GETTING_FROM_USER = 7
    CUSTOM_MODE_UNLOADING_TO_USER = 8
    CUSTOM_MODE_CHANGING_BATTERY = 9

    # Connection
    DRONE_CONNECTION = 'udpin:0.0.0.0:14540'
    DRONEPOINT_CONNECTION = ''

    # Flight
    FLIGHT_DISTANCE = 0.00027
    FLIGHT_ALT = 50

    # State
    IDLE = 'idle'
    GETTING_FROM_USER = 'getting_from_user'
    TAKING_BATTERY = 'taking_battery'
    LOADING_DRONE = 'loading_drone'
    FLYING = 'flying'
    UNLOADING_DRONE = 'unloading_drone'
    GIVING_BATTERY = 'giving_battery'
    UNLOADING_TO_USER = 'unloading_to_user'  