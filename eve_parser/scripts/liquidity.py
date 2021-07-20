import operator
from eve_parser.models import MarketHistory, TopTypes, Regions, Liquidity, Types, ParserDateStatus
from datetime import datetime, timedelta
from eve_parser.include.parser import Parser


def run(*args):
    Parser.parser_date_status("START liquidity calculation", 0, 0)
    region_array = Regions.objects.values_list("region_id")
    types_array = TopTypes.objects.values_list("type_id")
    if len(args) > 0:
        if "jita_all" in args[0]:
            region_array = [["10000002"]]
            types_array = Types.objects.values_list("type_id")
    for region in region_array:
        parser_date_status = ParserDateStatus.objects.filter(parser_name="Market history", region_id=region[0])
        month_ago = datetime.utcnow() - timedelta(days=30)
        day_range = parser_date_status[0].parse_time.date() - month_ago.date()
        for item_type in types_array:
            market_history = MarketHistory.objects.filter(region_id=region[0], type_id=item_type[0],
                                                          date__gte=month_ago.strftime("%Y-%m-%d"))
            market_history = sorted(market_history, key=operator.attrgetter('date'))
            liquidity_calc(region[0], item_type[0], day_range, market_history)
        Parser.parser_date_status("Liquidity calculation", region[0], 0)
    Parser.parser_date_status("END liquidity calculation", 0, 0)


def liquidity_calc(region_id, type_id, day_range, market_history):
    print(region_id, type_id)
    days = 0
    volume = 0
    average_price_3_days = 0
    for market_history_day in market_history:
        days += 1
        volume += market_history_day.volume
        if days > len(market_history) - 3:
            average_price_3_days += market_history_day.average
    if day_range.days != 0:
        if days >= 3:
            average_price_3_days /= 3
        elif days == 2:
            average_price_3_days /= 2
        day_avg_volume = volume / day_range.days
        insert_in_base(region_id, type_id, day_avg_volume, average_price_3_days,
                       day_avg_volume * average_price_3_days/1000000)


def insert_in_base(region_id, type_id, day_avg_volume, last_average_price, day_turnover):
    liq = list(Liquidity.objects.filter(region_id=region_id, type_id=type_id))
    if len(liq) < 1:
        liquidity = Liquidity.objects.create(
            region_id=region_id, type_id=type_id, day_volume=day_avg_volume,
            price=last_average_price, day_turnover=day_turnover)
        liquidity.save()
    else:
        liquidity = Liquidity.objects.filter(region_id=region_id, type_id=type_id).update(
            region_id=region_id, type_id=type_id, day_volume=day_avg_volume,
            price=last_average_price, day_turnover=day_turnover)
