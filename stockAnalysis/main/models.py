from django.db import models
import uuid

# Create your models here.


class Indicators (models.Model):
    INTERVALS = (
        ('1m', '1 minute'),
        ('2m', '2 minute'),
        ('5m', '5 minute'),
        ('15m', '15 minute'),
        ('30m', '30 minute'),
        ('60m', '60 minute'),
        ('90m', '90 minute'),
        ('1h', '1 hour'),
        ('1d', '1 day'),
        ('5d', '5 day'),
        ('1wk', '1 week'),
        ('1mo', '1 month'),
        ('3mo', '3 month'),
    )
    PERIODS = (
        ('1d', '1 day'),
        ('5d', '5 day'),
        ('1mo', '1 month'),
        ('3mo', '3 month'),
        ('6mo', '6 month'),
        ('1y', '1 year'),
        ('2y', '2 year'),
        ('5y', '5 year'),
        ('10y', '10 year'),
        ('ytd', 'year-to-date'),
        ('max', 'Max'),
    )
    CHARTS = (
        ('candlestick', 'Candlestick'),
        ('ohlc', 'OHLC'),
    )
    id = models.UUIDField(default=uuid.uuid4,
                          primary_key=True, unique=True, editable=True)
    interval = models.CharField(max_length=200, choices=INTERVALS)
    period = models.CharField(max_length=200, choices=PERIODS)
    type = models.CharField(max_length=200, choices=CHARTS)
    rsi = models.BooleanField(default=False)
    macd = models.BooleanField(default=False)
