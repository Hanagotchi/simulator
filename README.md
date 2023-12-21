# Sensor simulator
Indoor plant sensor simulator for early testing.

## How it works

The simulator creates a data packet every fixed period. This packet contains simulated parameters data like: 
- Temperature
- Humidity
- Light
- Watering 
- Current timestamp
- Device ID

This **fixed period** can be:
- Every N seconds/minutes/hours.
- When a parameter P increases/decreases in a ΔP.

### Temperature and humidity
This parameters are fetched from the [OpenWeatherMap API](https://openweathermap.org/). 

## Commands
It would be nice to accept commands from TUI to simulate deviations fixes. Something like `<parameter> <increase/decrease> <amount>`
