from config import Config
import requests


class Parser:

    def __init__(self):
        self.config = Config()

    def evetech_req(self, section, dict_get_args):
        get_args = ""
        for key in dict_get_args:
            get_args += "&" + key + "=" + str(dict_get_args[key])
        try:
            r = requests.get(self.config.esi + section + self.config.server + get_args)
        except requests.exceptions.RequestException as e:
            print("request can't receive data: %s" % e)
        else:
            return r.text
