from django.db import models


class Regions(models.Model):
    region_id = models.BigIntegerField()
    name = models.CharField(
        max_length=50
    )
    description = models.TextField(
        max_length=256
    )
    constellations = models.JSONField()


class Types(models.Model):
    type_id = models.IntegerField(
        unique=True
    )
    parse_time = models.DateTimeField(
        auto_now=True
    )
    name = models.CharField(
        max_length=128
    )
    packaged_volume = models.FloatField()
    volume = models.FloatField()
    group_id = models.IntegerField()
    market_group_id = models.IntegerField()
    icon_id = models.IntegerField()
    description = models.TextField()


class TopTypes(models.Model):
    type_id = models.IntegerField(
        unique=True
    )
    name = models.CharField(
        max_length=128
    )


class Market(models.Model):
    parse_time = models.DateTimeField(
        auto_now=True
    )
    region_id = models.IntegerField(
        db_index=True
    )

    duration = models.IntegerField()
    is_buy_order = models.BigIntegerField()
    issued = models.DateTimeField()
    location_id = models.BigIntegerField()
    min_volume = models.BigIntegerField()
    order_id = models.BigIntegerField(
        unique=True,
        db_index=True
    )
    price = models.FloatField(
        db_index=True
    )
    range = models.CharField(
        max_length=20
    )
    system_id = models.BigIntegerField()
    type_id = models.IntegerField(
        db_index=True
    )
    volume_remain = models.BigIntegerField()
    volume_total = models.BigIntegerField()


class MarketHistory(models.Model):
    region_id = models.IntegerField(
        db_index=True
    )
    type_id = models.IntegerField(
        db_index=True
    )
    date = models.DateField(
        db_index=True
    )
    average = models.FloatField()
    highest = models.FloatField()
    lowest = models.FloatField()
    order_count = models.IntegerField()
    volume = models.BigIntegerField()


class ParserStatus(models.Model):
    name = models.CharField(
        max_length=50
    )
    describe = models.CharField(
        max_length=100
    )
    region_id = models.IntegerField()
    now_parse = models.IntegerField()


class Liquidity(models.Model):
    region_id = models.IntegerField(
        db_index=True
    )
    type_id = models.IntegerField(
        db_index=True
    )
    day_volume = models.FloatField()
    price = models.FloatField()
    day_turnover = models.FloatField()
    price_bay = models.FloatField()
    price_sell = models.FloatField()


class LogisticsPlanning(models.Model):
    type_id = models.IntegerField(
        db_index=True
    )
    packaged_volume = models.FloatField()
    region_id_from = models.IntegerField(
        db_index=True
    )
    region_id_to = models.IntegerField(
        db_index=True
    )
    price_from = models.FloatField()
    price_to = models.FloatField()
    price_diff = models.FloatField()
    liquidity_from = models.FloatField()
    liquidity_to = models.FloatField()
    day_volume_from = models.FloatField()
    day_volume_to = models.FloatField()
    profit_from = models.FloatField()
    profit_to = models.FloatField()
    price_bay_from = models.FloatField()
    price_sell_from = models.FloatField()
    price_bay_to = models.FloatField()
    price_sell_to = models.FloatField()


class ParserDateStatus(models.Model):
    parser_name = models.CharField(
        max_length=50,
        db_index=True
    )
    region_id = models.IntegerField(
        db_index=True
    )
    region_id_log = models.IntegerField(
        db_index=True
    )
    parse_time = models.DateTimeField(
        auto_now=True
    )
