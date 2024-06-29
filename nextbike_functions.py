import datetime


def two_hours_forward(timestamp_string: str):
    date, time = timestamp_string.split(' ')
    year, month, day = date.split('-')
    hour, minute, second = time.split(':')
    date = datetime.datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))
    date += datetime.timedelta(hours=2)
    return date
