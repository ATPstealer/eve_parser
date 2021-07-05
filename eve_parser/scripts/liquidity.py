import operator
from eve_parser.models import MarketHistory, TopTypes, Regions, Liquidity
from datetime import datetime, timedelta, date
from eve_parser.include.parser import Parser


def run():
    start = datetime.now()
    for region in Regions.objects.values_list("region_id"):
        for item_type in TopTypes.objects.values_list("type_id"):
            month_ago = datetime.utcnow() - timedelta(days=30)
            market_history = MarketHistory.objects.filter(region_id=region[0], type_id=item_type[0],
                                                          date__gte=month_ago.strftime("%Y-%m-%d"))
            market_history = sorted(market_history, key=operator.attrgetter('date'))
            liquidity_calc(region[0], item_type[0], month_ago, market_history)
    print("start at: %s\nend at: %s" % (start, datetime.now()))
    parser = Parser()
    parser.parser_status("Liquidity calculation", "Done <br>Start at: %s\n<br>end at: %s" % (start, datetime.now()), 0, 0)


def liquidity_calc(region_id, type_id, month_ago, market_history):
    days = 0
    volume = 0
    day_range = timedelta(0)
    for market_history_day in market_history:
        days += 1
        volume += market_history_day.volume
        last_average_price = market_history_day.average
        last_date = market_history_day.date
        day_range = last_date - month_ago.date()
    if day_range.days != 0:
        day_avg_volume = volume / day_range.days
        insert_in_base(region_id, type_id, day_avg_volume, last_average_price,
                       day_avg_volume * last_average_price/1000000000)
        parser = Parser()
        parser.parser_status("Liquidity calculation", "item_type", region_id, type_id)


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
