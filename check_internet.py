
import os
import time

def check(url):
    is_printed = False
    while os.system("sudo ping -c 1 " + url) != 0:
        if is_printed is False:
            print("cant reach the cloud server. retrying.....")
            is_printed = True
        time.sleep(3)

    print("cloud server has been reached")
