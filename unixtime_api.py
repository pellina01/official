import requests


def getnow(url, list_name):
    json_response = requests.get(url=url)
    data = json_response.json()
    return(data[list_name])
