import requests
from logging import getLogger
from datetime import datetime


class IpCameraConfig:
    name = ""
    address = ""
    username = ""
    password = ""


class IpCamera:
    __site_url = "http://{}:{}@{}/photo.jpg"

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
        response = requests.get(self.__url)
        if response.status_code == 200:
            file_name = "photo_cam0.jpg"
            with open(file_name, "wb") as f:
                f.write(response.content)
                self.__logger.debug("Shot taken!")
                return True
        self.__logger.error("Could not connect to camera!")
        return False


if __name__ == "__main__":
    config = IpCameraConfig()
    config.name = "Cam0"
    config.address = ""
    config.username = ""
    config.password = ""
    IpCamera(config).take_shot()
