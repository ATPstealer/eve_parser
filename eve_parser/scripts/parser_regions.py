from eve_parser.include.parser import Parser
from eve_parser.models import Regions
import json


def run():
    clear_regions()
    parse_region()
    parse_region_description()


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
            regions = Regions.objects.create(region_id=region, constellations="")
            regions.save()


def parse_region_description():
    parser = Parser()
    dict_get_args = {"language": "en"}
    for region in Regions.objects.values_list("region_id"):
        print("Region description parse: " + srt(region))
        region_description_json = parser.evetech_req("/universe/regions/" + str(region[0]), dict_get_args)
        region_description_json = json.loads(region_description_json)
        if "description" not in region_description_json:
            region_description_json["description"] = ""
        Regions.objects.filter(region_id=region[0]).update(
            name=region_description_json["name"], description=region_description_json["description"],
            constellations=region_description_json["constellations"])


def clear_regions():
    Regions.objects.all().delete()
