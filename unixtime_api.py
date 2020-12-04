import requests
import time


def get_time(url, unix_name, url2, unix_name2):
    def getnow():
        json_response = requests.get(url=url)
        if json_response.status_code == 200:
            data = json_response.json()
            del json_response
            return data[unix_name]
        else:
            json_response = requests.get(url=url2)
            if json_response.status_code == 200:
                data = json_response.json()
                del json_response
                return data[unix_name2]
            else:
                print("API call failed. Substituting system time")
                return int(time.time())
    return getnow
