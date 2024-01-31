import requests as req
from requests import Response
from dotenv import load_dotenv
from os import environ
from typing import Tuple
from datetime import datetime
import logging
import math
import uuid

load_dotenv()
logging.getLogger("urllib3").setLevel(logging.WARNING)
UUID = str(uuid.uuid4()).replace("-", "")


def fetch_temperature_and_humidity(location: str) -> Tuple[int, int]:

    base_params = {
        "q": location,
        "APPID": environ['WEATHER_API_KEY']
    }
    res: Response = req.get(environ["WEATHER_API_URL"], params=base_params)

    if not res.ok:
        raise Exception(
            "Could not fetch temperature and humidity from weather API"
            )

    result = res.json()
    temperature = int(result["main"]["temp"] - 273.15)
    humidity = result["main"]["humidity"]

    return temperature, humidity


def get_decimal_hour():
    current_hour = datetime.now()
    return current_hour.hour + (
        60 * current_hour.minute + current_hour.second
        ) / 3600


def solar_irradiation_simulator(x):
    if x < 7 or x > 19:
        return 0

    x += 14
    x *= (math.pi / 6)
    x = math.sin(x)
    x += 1
    x *= 500
    return x


def fetch_solar_irradiation():
    x = get_decimal_hour()
    return round(solar_irradiation_simulator(x))


def watering_simulator(x):
    x %= 6
    x /= 6
    x *= 100
    x = 100 - x
    return x


def fetch_watering():
    x = get_decimal_hour()
    return round(watering_simulator(x))


def create_packet(temperature: float = None, humidity: float = None,
                  light: float = None, watering: float = None):
    '''
    Creates a data packet with simulated data, validating the data before that.

    If all the parameters are empty, returns None. Else, return a dictionary
    with the data.


    Constraints:
    - Humidity and Watering should be between 0 and 100, since they are
    percentages.
    - Light has to be positive or 0.
    '''
    if not (temperature or humidity or light or watering):
        return None

    if humidity < 0 or humidity > 100:
        raise Exception(f"Humidity has to be between 0 and 100."
                        f"Current value: {humidity}")

    if watering < 0 or watering > 100:
        raise Exception(f"Watering has to be between 0 and 100. "
                        f"Current value: {watering}")

    if light < 0:
        raise Exception(f"Light has to be positive or 0. "
                        f"Current value: {light}")

    return {
        "temperature": temperature,
        "humidity": humidity,
        "light": light,
        "watering": watering,
        "time_stamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "id_device": UUID
    }


def generate_data(location="Pilar, AR") -> Tuple[int, int, int, int]:
    '''
    Generates the parameters data: temperature, humidity, light and watering.

    [Describe the criteria of every parameter here]
    -
    -
    -
    '''

    temperature, humidity = fetch_temperature_and_humidity(location)
    # esto no va a producir cambios instantaneamente, pero es para probar
    light = fetch_solar_irradiation()
    watering = fetch_watering()

    return temperature, humidity, light, watering


def data_has_changed(current, last_sent, deviations):
    '''
    Compares the current packet and the last sent packet,
    based in the deviations.

    If any parameter differs enough from the last sent packet, then the packet
    must be sent.

    In other words:
    if (|current[parameter] - last_sent[parameter]| > deviations[parameter]),
    return True.
    Else, return False

    If there is no last_sent, then the current must be sent.

    Types:
    - current: {temperature: float, humidity: float, light: float,
    watering: float}
    - last_sent: {temperature: float, humidity: float, light: float,
    watering: float}
    - deviations: {temperature: float, humidity: float, light: float,
    watering: float}
    '''

    if not last_sent:
        return True

    if parameter_has_changed(current["temperature"], last_sent["temperature"],
                             deviations["temperature"])\
            or parameter_has_changed(current["humidity"], last_sent["humidity"],
                                     deviations["humidity"])\
            or parameter_has_changed(current["light"], last_sent["light"],
                                     deviations["light"])\
            or parameter_has_changed(current["watering"], last_sent["watering"],
                                     deviations["watering"]):
        return True

    return False


def parameter_has_changed(current, last, deviation):
    return abs(current - last) > deviation
