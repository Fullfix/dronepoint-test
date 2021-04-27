class DronepointConfig:
    # Modes
    CUSTOM_MODE_LOADING_DRONE = 14
    CUSTOM_MODE_UNLOADING_DRONE = 13
    CUSTOM_MODE_GETTING_FROM_USER = 10
    CUSTOM_MODE_UNLOADING_TO_USER = 11
    CUSTOM_MODE_CHANGING_BATTERY = 9
    CUSTOM_MODE_OPEN_BOTTOM_HATCH = 21
    CUSTOM_MODE_OPEN_TOP_HATCH = 3
    CUSTOM_MODE_GOTO_CELL = 5

    # Connection
    DRONE_CONNECTION = 'udpin:0.0.0.0:14540'
    DRONEPOINT_CONNECTION = 'udpin:192.168.194.34:14590'
    # DRONEPOINT_CONNECTION = 'udpin:192.168.194.198:14590'

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

    # DP State
    STATE_UNKNOWN = 0
    STATE_OPEN = 1
    STATE_OPENING = 2
    STATE_CLOSED = 3
    STATE_CLOSING = 4
    STATE_LOADING_DRONE = 5
    STATE_UNLOADING_DRONE = 6
    STATE_GETTING_FROM_USER = 7
    STATE_UNLOADING_TO_USER = 8
    STATE_CHANGING_BATTERY = 9
    STATE_SERVICE = 10
    STATE_RESET = 11
    STATE_STANDBY = 12
    STATE_ERROR = 13