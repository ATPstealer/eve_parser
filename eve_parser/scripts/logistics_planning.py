from eve_parser.models import TopTypes, Regions, Types, Liquidity, LogisticsPlanning, ParserDateStatus, Market
from eve_parser.models import models
from eve_parser.include.parser import Parser


def run(*args):
    region_from = [[args[0]]]
    region_to = [[args[1]]]
    Parser.parser_date_status("START log plan from %s to %s" % (args[0], args[1]), 0, 0)
    day_turnover_threshold = float(args[2])
    if region_from[0][0] == "*":
        region_from = Regions.objects.values_list("region_id")
    if region_to[0][0] == "*":
        region_to = Regions.objects.values_list("region_id")
    for reg_from in region_from:
        for reg_to in region_to:
            if int(reg_from[0]) < int(reg_to[0]):
                calculate_logistics(reg_from[0], reg_to[0], day_turnover_threshold)
    Parser.parser_date_status("END log plan from %s to %s" % (args[0], args[1]), 0, 0)


def calculate_logistics(region_from, region_to, day_turnover_threshold):
    print("Calculate logistics from %s to %s" % (region_from, region_to))
    if not check_need(region_from, region_to):
        return
    for item_type in TopTypes.objects.values_list("type_id"):
        # get data from database
        item_describe = Types.objects.get(type_id=item_type[0])
        try:
            liquidity_from = Liquidity.objects.get(type_id=item_type[0], region_id=region_from)
        except models.ObjectDoesNotExist:
            continue
        try:
            liquidity_to = Liquidity.objects.get(type_id=item_type[0], region_id=region_to)
        except models.ObjectDoesNotExist:
            continue

        if liquidity_to.day_turnover >= day_turnover_threshold and liquidity_from.day_turnover >= day_turnover_threshold:
            log = list(LogisticsPlanning.objects.filter(type_id=item_type[0], region_id_from=region_from,
                                                        region_id_to=region_to))
            price_bay_from = check_price(region_from, item_type[0], 1)
            price_sell_from = check_price(region_from, item_type[0], 0)
            price_bay_to = check_price(region_to, item_type[0], 1)
            price_sell_to = check_price(region_to, item_type[0], 0)

            if len(log) < 1:
                logistics_planning = LogisticsPlanning.objects.create(
                    type_id=item_type[0], packaged_volume=item_describe.packaged_volume, region_id_from=region_from, region_id_to=region_to,
                    price_from=liquidity_from.price, price_to=liquidity_to.price, price_diff=liquidity_to.price - liquidity_from.price,
                    liquidity_from=liquidity_from.day_turnover, liquidity_to=liquidity_to.day_turnover,
                    day_volume_from=liquidity_from.day_volume, day_volume_to=liquidity_to.day_volume,
                    profit_from=float((liquidity_from.price - liquidity_to.price) * (-1) * liquidity_to.day_volume) / 1000000,
                    profit_to=float((liquidity_from.price - liquidity_to.price) * liquidity_from.day_volume) / 1000000,
                    price_bay_from=price_bay_from, price_sell_from=price_sell_from, price_bay_to=price_bay_to, price_sell_to=price_sell_to)
                logistics_planning.save()
            else:
                logistics_planning = LogisticsPlanning.objects.filter(type_id=item_type[0], region_id_from=region_from,
                                                                      region_id_to=region_to).update(
                    price_from=liquidity_from.price, price_to=liquidity_to.price,
                    price_diff=liquidity_to.price - liquidity_from.price,
                    liquidity_from=liquidity_from.day_turnover, liquidity_to=liquidity_to.day_turnover,
                    day_volume_from=liquidity_from.day_volume, day_volume_to=liquidity_to.day_volume,
                    profit_from=float((liquidity_from.price - liquidity_to.price) * (-1) * liquidity_to.day_volume) / 1000000,
                    profit_to=float((liquidity_from.price - liquidity_to.price) * liquidity_from.day_volume) / 1000000,
                    price_bay_from=price_bay_from, price_sell_from=price_sell_from, price_bay_to=price_bay_to, price_sell_to=price_sell_to)
        else:
            LogisticsPlanning.objects.filter(type_id=item_type[0], region_id_from=region_from,
                                             region_id_to=region_to).delete()
    Parser.parser_date_status("Calculate logistic", region_from, region_to)


def check_need(region_from, region_to):
    try:
        liq_to_time = ParserDateStatus.objects.get(parser_name="Liquidity calculation",
                                                   region_id=region_to).parse_time
    except models.ObjectDoesNotExist:
        return False
    try:
        liq_from_time = ParserDateStatus.objects.get(parser_name="Liquidity calculation",
                                                     region_id=region_from).parse_time
    except models.ObjectDoesNotExist:
        return False
    try:
        log_time = ParserDateStatus.objects.get(parser_name="Calculate logistic", region_id=region_from,
                                                region_id_log=region_to).parse_time
    except models.ObjectDoesNotExist:
        return True
    if log_time > liq_to_time or log_time > liq_from_time:
        return False
    else:
        return True


def check_price(region_id, type_id, is_buy_order):
    order = "-price" if is_buy_order else "price"
    price_array = Market.objects.values_list("price").filter(region_id=region_id, type_id=type_id,
                                                             is_buy_order=is_buy_order).order_by(order)
    return price_array[0][0] if len(price_array) > 0 else 0
