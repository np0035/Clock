import datetime

settings = {
    "locations": {"HUNTSVILLE_AL": [34.732611, -86.586232], "MERRIMACK_NH": [42.867057, -71.495412]},
    "time_zones": {"HUNTSVILLE_AL": -5.0, "MERRIMACK_NH": -4.0},
    "current_loc": "HUNTSVILLE_AL",
    "time_zone": -4.0,
    "date": "today",
}

dynamic_vals = {
    "local_time": datetime.time(),
    "sunrise_time": datetime.time(),
    "sunset_time": datetime.time(),
    "sunrise_angle": 0,
    "day_extent": 0,
    "hand_angle": 0
}


def get_locations():
    return settings["locations"]


def get_angle_vals():
    return dynamic_vals["sunrise_angle"], dynamic_vals["day_extent"], dynamic_vals["hand_angle"]
