from eve_parser.models import Liquidity, TopTypes, Types
from django.db.models import Q


def run():
    TopTypes.objects.all().delete()
    liquidity = Liquidity.objects.filter(region_id=10000002, day_volume__gte=0.001)
    types = Types.objects.filter(~Q(market_group_id=0), ~Q(name__contains="blueprint"), ~Q(name__contains="SKIN"),
                                 ~Q(name__contains="Men's"), ~Q(name__contains="Women's"))
    for typ in types:
        print(typ.type_id)
        for liq in liquidity:
            if liq.type_id == typ.type_id:
                types = TopTypes.objects.create(type_id=typ.type_id, name=typ.name)
                types.save()
