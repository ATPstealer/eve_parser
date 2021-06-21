from django.db import models


class Regions(models.Model):
    region_id = models.IntegerField()


class Market(models.Model):
    parse_time = models.DateTimeField(
        auto_now=True
    )
    region_id = models.IntegerField()

    duration = models.IntegerField()
    is_buy_order = models.BooleanField()
    issued = models.DateTimeField()
    location_id = models.IntegerField()
    min_volume = models.IntegerField()
    order_id = models.IntegerField(
        unique=True
    )
    price = models.FloatField()
    range = models.CharField(
        max_length=20
    )
    system_id = models.IntegerField()
    type_id = models.IntegerField()
    volume_remain = models.IntegerField()
    volume_total = models.IntegerField()


class Types(models.Model):
    type_id = models.IntegerField(
        unique=True
    )
