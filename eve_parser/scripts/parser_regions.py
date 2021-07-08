from eve_parser.include.parser import Parser
from eve_parser.models import Regions
import json


def run():
    clear_regions()
    parse_region()


def parse_region():
    parser = Parser()
    regions_json = parser.evetech_req("/universe/regions/", {})
    regions_data = json.loads(regions_json)

    for region in regions_data:
        exist = 0
        exist_regions = Regions.objects.values_list('region_id')
        for exist_region in exist_regions:
            if region == exist_region[0]:
                exist = 1
                break
        if exist == 0:
            regions = Regions.objects.create(region_id=region)
            regions.save()


def clear_regions():
    Regions.objects.all().delete()
