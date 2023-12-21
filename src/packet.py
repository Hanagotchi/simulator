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