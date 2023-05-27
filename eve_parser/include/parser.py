from config import Config
import requests
import time
from datetime import datetime, timezone
from eve_parser.models import ParserStatus, ParserDateStatus


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
                if r.status_code == 200 or r.status_code == 404 or r.status_code == 400 or\
                        r.status_code == 500 and "Undefined 404 response" in r.text:
                    return r.text
                elif r.status_code == 420:
                    print("Response code: " + str(r.status_code) + " Wait: " + str(k*10))
                    time.sleep(k*10)
                else:
                    print("Response code: " + str(r.status_code) + " Wait: " + str(k*2))
                    time.sleep(k*2)
        return r.text

    @staticmethod
    def parser_date_status(parser_name, region_id, region_id_log):
        par = ParserDateStatus.objects.filter(parser_name=parser_name, region_id=region_id, region_id_log=region_id_log)
        if len(par) == 0:
            ParserDateStatus.objects.create(parser_name=parser_name, region_id=region_id, region_id_log=region_id_log)
        else:
            ParserDateStatus.objects.filter(parser_name=parser_name, region_id=region_id, region_id_log=region_id_log)\
                .update(parse_time=datetime.now(timezone.utc))
