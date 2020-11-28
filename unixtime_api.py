import requests
import time


def getnow(url, unix_name):
    if (json_response := requests.get(url=url)).status_code == 200:
        data = json_response.json()
        return(data[unix_name])
    else:
        return int(time.time())
