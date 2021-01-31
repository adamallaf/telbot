from bot import BotAppConfig
from ip_camera import IpCameraConfig
from utils import getToken, readToken


config = BotAppConfig()
config.timezone = 'Europe/Warsaw'
if readToken():
    config.token = getToken()

config.alarm = False

config.camera_config = None
