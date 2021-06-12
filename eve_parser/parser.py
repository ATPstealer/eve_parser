from config import Config
from eve_parser.models import Regions


class Parser:

    def __init__(self):
        self.config = Config()

    def make_something(self):
        self.config.server
        regions = Regions.objects.create(region_id="1000000")
        Regions.objects.all().delete()
