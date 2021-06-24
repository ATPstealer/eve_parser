from eve_parser.include.parser import Parser
from eve_parser.models import Types
import json


def run():
    parser = Parser()
    for page in range(1, 10000):
        dict_get_args = {"page": page}
        types_json = parser.evetech_req("/universe/types/", dict_get_args)
        if 'error' in types_json:
            print(types_json)
            break

        types_data = json.loads(types_json)
        for item_type in types_data:
            print(item_type)
            t = list(Types.objects.filter(type_id=item_type))
            if len(t) < 1:
                types = Types.objects.create(type_id=item_type)
                types.save()


def clear_types():
    Types.objects.all().delete()
