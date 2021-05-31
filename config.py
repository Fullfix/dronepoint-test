from dotenv import dotenv_values

config = dotenv_values('.env')
password = config['SECRET_CODE']
stream_video = bool(int(config['STREAM_VIDEO']))