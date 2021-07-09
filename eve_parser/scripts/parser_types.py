from eve_parser.include.parser import Parser
from eve_parser.models import Liquidity, TopTypes, Types
import json
from datetime import datetime, timezone, timedelta
from django.db.models import Q


def run():
    parse_types()
    parse_types_description()
    clear_types()
    top_types()


def parse_types():
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
                types = Types.objects.create(type_id=item_type,
                                             packaged_volume=0, volume=0, group_id=0, market_group_id=0, icon_id=0)
                types.save()


def parse_types_description():
    parser = Parser()
    for item_type in Types.objects.values_list("type_id"):
        dict_get_args = {"language": "en"}
        types_description_json = parser.evetech_req("/universe/types/" + str(item_type[0]), dict_get_args)
        print(types_description_json)
        if "error" in types_description_json:
            continue
        print("Item: " + str(item_type[0]))
        insert_in_base(json.loads(types_description_json))


def insert_in_base(types_description_json):
    print(types_description_json["type_id"])
    if "icon_id" not in types_description_json:
        types_description_json["icon_id"] = 0
    if "market_group_id" not in types_description_json:
        types_description_json["market_group_id"] = 0
    Types.objects.filter(type_id=types_description_json["type_id"]).update(
        parse_time=datetime.now(timezone.utc), packaged_volume=types_description_json["packaged_volume"],
        volume=types_description_json["volume"], group_id=types_description_json["group_id"],
        description=types_description_json["description"], name=types_description_json["name"],
        market_group_id=types_description_json["market_group_id"], icon_id=types_description_json["icon_id"])


def clear_types():
    orders_for_delete = Types.objects.filter(parse_time__lte=datetime.now(timezone.utc) - timedelta(days=1))
    for order in orders_for_delete:
        print("Delete: " + str(order.order_id))
        order.delete()


def top_types():
    TopTypes.objects.all().delete()
    # liquidity = Liquidity.objects.filter(region_id=10000002, day_volume__gte=0.001)
    types = Types.objects.filter(~Q(market_group_id=0), ~Q(name__contains="blueprint"), ~Q(name__contains="SKIN"),
                                 ~Q(name__contains="Men's"), ~Q(name__contains="Women's"))
    for typ in types:
        print(typ.type_id)
        # for liq in liquidity:
            # if liq.type_id == typ.type_id:
        types_for_save = TopTypes.objects.create(type_id=typ.type_id, name=typ.name)
        types_for_save.save()
