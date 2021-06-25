from eve_parser.models import Liquidity, TopTypes


def run():
    TopTypes.objects.all().delete()
    liq = Liquidity.objects.filter(region_id=10000002, month_volume__gte=0.001)
    for t in liq:
        types = TopTypes.objects.create(type_id=t.type_id)
        types.save()
