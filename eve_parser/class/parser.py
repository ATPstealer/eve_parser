from config import Config
from eve_parser.models import Regions
import requests


class Parser:

    def __init__(self):
        self.config = Config()

    def make_something(self):
        self.config.server
        regions = Regions.objects.create(region_id="1000000")
        Regions.objects.all().delete()

    def evetech_req(self, section):
        try:
            r = requests.get(self.config.esi + section + self.config.server)
        except requests.exceptions.RequestException as e:
            print("request can't receive data: %s" % e)
        else:
            return r.text
