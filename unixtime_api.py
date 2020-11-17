import requests
url = "http://worldtimeapi.org/api/timezone/asia/manila"


def getnow():
    json_response = requests.get(url=url)
    data = json_response.json()
    return(data["unixtime"])
