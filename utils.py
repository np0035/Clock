from datetime import timedelta, datetime
import datetime as dt
from config import settings, dynamic_vals
import requests
import json
import re


def offset_time(time_string, utc_offset=-5.0):
    """
    Creates a datetime object containing the local time.

    :param time_string: A string in the form HH:MM:SS containing the UTC value
    :param utc_offset: A floating point value denoting the difference between local time and Greenwich in hours
    :return: A datetime object containing the local time
    """
    time_object = datetime.strptime(time_string, '%H:%M:%S')
    time_local = (time_object + timedelta(hours=utc_offset)).time()
    return time_local


def get_sun_data(coords, date='today'):
    """
    Gets data regarding apparent solar motion from the sunrise-sunset API

    :param coords: 1x2 list denoting the observer's coordinates; i.e. [latitude, longitude]
    :param date: The date of the observation in the form YYYY-MM-DD
    :return: A dictionary containing the data
    """
    request_url = 'https://api.sunrise-sunset.org/json?lat={lat}&lng={lng}&date={date}&formatted=0' \
        .format(lat=coords[0], lng=coords[1], date=date)

    raw_data = requests.get(request_url)
    data_dict = json.loads(raw_data.content)

    return data_dict


def get_sunrise_sunset_times(coords, date='today', utc_offset=0):
    """
    Filters data from get_sun_data() to return only the local sunrise and sunset

    :param coords: The coordinates of the observer
    :param date: The date of the observation
    :param utc_offset: The difference between local time and Greenwich, in hours
    :return: Time objects containing the sunrise time and sunset time
    """

    data_dict = get_sun_data(coords, date)

    sunrise_time_utc = re.split('T|[+]', data_dict['results']['sunrise'])[1]
    sunset_time_utc = re.split('T|[+]', data_dict['results']['sunset'])[1]

    sunrise_time_local = offset_time(sunrise_time_utc, utc_offset)
    sunset_time_local = offset_time(sunset_time_utc, utc_offset)

    return sunrise_time_local, sunset_time_local


def time_to_angle(time_object):
    mins = (time_object.hour * 60) + time_object.minute + (time_object.second / 60)
    degrees_per_min = 4
    angle = mins / degrees_per_min + 180
    return angle


def get_angles(sunrise_time, sunset_time, local_time):
    # Get angles for clock face
    sunrise_angle = time_to_angle(sunrise_time)
    sunset_angle = time_to_angle(sunset_time)
    day_extent = sunset_angle - sunrise_angle

    hand_angle = time_to_angle(local_time)

    return sunrise_angle, day_extent, hand_angle


def get_times(location):
    coords = settings["locations"][str(location)]
    time_zone = settings["time_zones"][str(location)]
    sunrise_time, sunset_time = get_sunrise_sunset_times(coords, settings["date"], time_zone)

    return sunrise_time, sunset_time


def update_angles():
    dynamic_vals["local_time"] = datetime.time(datetime.utcnow() + timedelta(
        hours=settings["time_zones"][settings["current_loc"]]))

    print(settings["time_zones"][settings["current_loc"]])
    print(dynamic_vals["local_time"])
    dynamic_vals["sunrise_time"], dynamic_vals["sunset_time"] = get_times(settings["current_loc"])
    dynamic_vals["sunrise_angle"], dynamic_vals["day_extent"], dynamic_vals["hand_angle"] = get_angles(
        dynamic_vals["sunrise_time"],
        dynamic_vals["sunset_time"],
        dynamic_vals["local_time"])
    print(dynamic_vals["hand_angle"])
