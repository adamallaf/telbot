import requests
from datetime import datetime


site_url = "http://{}:{}@192.168.1.114:8080/photo.jpg"


def cam0_take_shot():
    response = requests.get(site_url.format("admin", "12345A"))
    if response.status_code == 200:
        file_name = "photo_cam0.jpg"
        with open(file_name, "wb") as f:
            f.write(response.content)
            return True
    return False


if __name__ == "__main__":
    cam0_take_shot()
