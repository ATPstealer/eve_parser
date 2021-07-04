from config import Config
import requests
import time
from eve_parser.models import ParserStatus


class Parser:

    def __init__(self):
        self.config = Config()

    def evetech_req(self, section, dict_get_args):
        get_args = ""
        for key in dict_get_args:
            get_args += "&" + key + "=" + str(dict_get_args[key])
        for k in range(1, 360):
            try:
                r = requests.get(self.config.esi + section + self.config.server + get_args)
            except requests.exceptions.RequestException as e:
                print("request can't receive data: %s" % e)
            else:
                if r.status_code == 200 or r.status_code == 404 or \
                        r.status_code == 500 and "Undefined 404 response" in r.text:
                    return r.text
                elif r.status_code == 420:
                    print("Response code: " + str(r.status_code) + " Wait: " + str(k*10))
                    time.sleep(k*10)
                else:
                    print("Response code: " + str(r.status_code) + " Wait: " + str(k*2))
                    time.sleep(k*2)

        return r.text

    def parser_status(self, name, describe, region_id, now_parse):
        p = ParserStatus.objects.filter(name=name)
        if len(p) == 0:
            ParserStatus.objects.create(name=name, describe=describe, region_id=region_id, now_parse=now_parse)
        else:
            ParserStatus.objects.filter(name=name).update(name=name, describe=describe,
                                                          region_id=region_id, now_parse=now_parse)
