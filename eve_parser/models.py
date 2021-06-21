from django.db import models


class Regions(models.Model):
    region_id = models.BigIntegerField()


class Types(models.Model):
    type_id = models.IntegerField(
        unique=True
    )


class Market(models.Model):
    parse_time = models.DateTimeField(
        auto_now=True
    )
    region_id = models.IntegerField()

    duration = models.IntegerField()
    is_buy_order = models.BigIntegerField()
    issued = models.DateTimeField()
    location_id = models.BigIntegerField()
    min_volume = models.BigIntegerField()
    order_id = models.BigIntegerField(
        unique=True
    )
    price = models.FloatField()
    range = models.CharField(
        max_length=20
    )
    system_id = models.BigIntegerField()
    type_id = models.IntegerField()
    volume_remain = models.BigIntegerField()
    volume_total = models.BigIntegerField()


class MarketHistory(models.Model):
    region_id = models.IntegerField()
    type_id = models.IntegerField()
    date = models.DateField()
    average = models.FloatField()
    highest = models.FloatField()
    lowest = models.FloatField()
    order_count = models.IntegerField()
    volume = models.BigIntegerField()

