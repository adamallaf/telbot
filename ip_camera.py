import requests
from logging import getLogger
from datetime import datetime


class IpCameraConfig:
    name = ""
    address = ""
    username = ""
    password = ""


class IpCamera:
    __site_url = "http://{}:{}@{}/"
    __shot = "photo.jpg"
    __set_night_vision_gain = "settings/night_vision_gain?set={:.2f}"
    __set_night_vision_on = "settings/night_vision?set=on"
    __set_night_vision_off = "settings/night_vision?set=off"

    def __init__(self, cam_config):
        self.__config = cam_config
        self.__cam_name = cam_config.name
        self.__address = cam_config.address
        self.__username = cam_config.username
        self.__password = cam_config.password
        self.__url = self.__site_url.format(self.__username, self.__password, self.__address)
        self.__logger = getLogger(self.__class__.__name__ + "_{}".format(self.__cam_name))

    def take_shot(self):
        self.__logger.debug("taking shot...")
        response = requests.get(self.__url + self.__shot)
        if response.status_code == 200:
            file_name = "photo_cam0.jpg"
            with open(file_name, "wb") as f:
                f.write(response.content)
                self.__logger.debug("Shot taken!")
                return True
        self.__logger.error("shot - could not connect to camera!")
        return False

    def enableNightVision(self):
        response = requests.get(self.__url + self.__set_night_vision_on)
        if response.status_code == 200:
            self.__logger.debug("Night vision enabled!")
            return True
        self.__logger.error("enable night vision - could not connect to camera!")
        return False

    def disableNightVision(self):
        response = requests.get(self.__url + self.__set_night_vision_off)
        if response.status_code == 200:
            self.__logger.debug("Night vision disabled!")
            return True
        self.__logger.error("disable night vision - could not connect to camera!")
        return False

    def setNightVisionGain(self, gain):
        if gain not in range(1, 61):
            self.__logger.error("set night vision gain - wrong gain! (x{:.2f})".format(gain))
            return False
        response = requests.get(self.__url + self.__set_night_vision_gain.format(gain))
        if response.status_code == 200:
            self.__logger.debug("Night vision gain set to: x{:.2f}".format(gain))
            return True
        self.__logger.error("set night vision gain - could not connect to camera!")
        return False


if __name__ == "__main__":
    config = IpCameraConfig()
    config.name = "Cam0"
    config.address = ""
    config.username = ""
    config.password = ""
    IpCamera(config).take_shot()
