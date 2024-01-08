import random as rnd

'''
Creates a data packet with simulated data, validating the data before that.

If all the parameters are empty, returns None. Else, return a dictionary with the data.


Constraints:
- Humidity and Watering should be between 0 and 100, since they are percentages.
- Light has to be positive or 0.
'''


def create_packet(temperature: float = None, humidity: float = None, light: float = None, watering: float = None):
    if not (temperature and humidity and light and watering):
        return None

    if humidity < 0 or humidity > 100:
        raise Exception(f"Humidity has to be between 0 and 100. Current value: {humidity}")

    if watering < 0 or watering > 100:
        raise Exception(f"Watering has to be between 0 and 100. Current value: {watering}")

    if light < 0:
        raise Exception(f"Light has to be positive or 0. Current value: {light}")

    return {
        "temperature": temperature,
        "humidity": humidity,
        "light": light,
        "watering": watering
    }


'''
Generates the parameters data: temperature, humidity, light and watering.

[Describe the criteria of every parameter here]
- 
- 
-
'''


def generate_data():
    # TODO
    temperature = rnd.randint(-5, 30)
    humidity = rnd.randint(0, 100)
    light = rnd.randint(0, 400)
    watering = rnd.randint(0, 100)

    return temperature, humidity, light, watering


'''
Compares the current packet and the last sent packet, based in the deviations.

If any parameter differs enough from the last sent packet, then the packet
must be sent. 

In other words: if (|current[parameter] - last_sent[parameter]| > deviations[parameter]), return True.
Else, return False

If there is no last_sent, then the current must be sent.

Types:
- current: {temperature: float, humidity: float, light: float, watering: float}
- last_sent: {temperature: float, humidity: float, light: float, watering: float}
- deviations: {temperature: float, humidity: float, light: float, watering: float}
'''


def data_has_changed(current, last_sent, deviations):
    if not last_sent:
        return True

    if parameter_has_changed(current["temperature"], last_sent["temperature"], deviations["temperature"])\
            or parameter_has_changed(current["humidity"], last_sent["humidity"], deviations["humidity"])\
            or parameter_has_changed(current["light"], last_sent["light"], deviations["light"])\
            or parameter_has_changed(current["watering"], last_sent["watering"], deviations["watering"]):
        return True

    return False


def parameter_has_changed(current, last, deviation):
    return abs(current - last) > deviation
