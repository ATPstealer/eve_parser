from config import Config
import requests
import time


class Parser:

    def __init__(self):
        self.config = Config()

    def evetech_req(self, section, dict_get_args):
        get_args = ""
        for key in dict_get_args:
            get_args += "&" + key + "=" + str(dict_get_args[key])
        for k in range(1, 4):
            try:
                r = requests.get(self.config.esi + section + self.config.server + get_args)
            except requests.exceptions.RequestException as e:
                print("request can't receive data: %s" % e)
            else:
                if r.status_code == 200 or r.status_code == 404:
                    return r.text
                else:
                    print("Response code: " + str(r.status_code))
                    time.sleep(5)
        return r.text
