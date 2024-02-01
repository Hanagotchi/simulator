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

## Usage Instructions
The repository includes a **Makefile** that encapsulates various commands used frequently in the project as targets. The targets are executed by invoking:

* **make \<target\>**:
The essential targets to start and stop the system are **docker-compose-up** and **docker-compose-down**, with the remaining targets being useful for debugging and troubleshooting.

Available targets are:
* **docker-compose-up**: Initializes the development environment (builds docker images for the server and client, initializes the network used by docker, etc.) and starts the containers of the applications that make up the project.
* **docker-compose-down**: Performs a `docker-compose stop` to stop the containers associated with the compose and then performs a `docker-compose down` to destroy all resources associated with the initialized project. It is recommended to execute this command at the end of each run to prevent the host machine's disk from filling up.
* **docker-compose-logs**: Allows viewing the current logs of the project. Use with `grep` to filter messages from a specific application within the compose.
* **docker-image**: Builds the images to be used. This target is used by **docker-compose-up**, so it can be used to test new changes in the images before starting the project.

Important Note: This service assumes a running instance of RabbitMQ and connects to it. Therefore, to run this service, it is necessary to first have the **measurements** service running. Please make sure to also check [measurements repository](https://github.com/Hanagotchi/measurements).
