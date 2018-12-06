import datetime

def to_date(value):
    return datetime.datetime.fromtimestamp(value / 1000)