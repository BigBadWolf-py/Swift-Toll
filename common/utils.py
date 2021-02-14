from random import randint

from datetime import datetime


def get_location(loc_str):
    """
    This function parses the provided location string into lat lng dict. Sample Str : [28.121312, 77.212121]
    :param loc_str:
    :return: lat lng dictionary
    """
    if not loc_str:
        raise Exception('Unable to parse location : {0}'.format(loc_str))
    loc = [l.strip() for l in loc_str.split(',') if l]
    return {
        'lat': loc[0],
        'lng': loc[1]
    }


def get_str_from_date(date):
    """
    Converts the date into timestamp format string
    :param date: date object
    """
    return date.strftime('%Y-%m-%d %H:%M:%S')


def get_access_code():
    return randint(1000, 9999)


def within_a_same_day(t):
    return True if (datetime.now()-t).seconds < 86400 else False


def under_midnight(t):
    return True if (datetime.now().day-t.day) == 0 else False
