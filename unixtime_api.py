import requests
import time


def getnow(url, unix_name, url2, unix_name2):
    if (json_response := requests.get(url=url)).status_code == 200:
        data = json_response.json()
        del json_response
        return data[unix_name]
    elif (json_response := requests.get(url=url2)).status_code == 200:
        data = json_response.json()
        del json_response
        return data[unix_name2]
    else:
        print("API call failed. Substituting system time")
        return int(time.time())
