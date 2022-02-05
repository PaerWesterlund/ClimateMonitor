# ClimateMonitor
# Filename: climateMon.py
# Original: https://github.com/Mjrovai/RPi-NodeMCU-Weather-Station/blob/master/IoT%20Weather%20Station/localDataToTS_v1_EXT.py
# Author: Marcelo Rovai
# Modified by: Paer Westerlund 
# Date: 2022-02-05
# Description: Reads 3 different climate sensors and sends indoor
# temperature, humidity and atmospheric pressure to ThingSpeak
# IoT platform with defined intervals
# DS18B20 library: https://github.com/sunfounder/Sunfounder_SensorKit_Python_code_for_RaspberryPi/blob/master/17_ds18b20.py
# DHT11 library: https://github.com/sunfounder/SunFounder_DHT11
# BMP280 library: https://github.com/pimoroni/bmp280-python
# Note: Slight modifications has been made to the sensor libraries
# to fit this program.
# To execute automatically at bootup use for example crontab, see:
# https://www.dexterindustries.com/howto/auto-run-python-programs-on-the-raspberry-pi/
# Send Twitter messages to your phone by creating a TimeControl and tweet:
# Temp: %%channel_1637741_field_1%%
# Humidity: %%channel_1637741_field_2%%
# Pressure: %%channel_1637741_field_3%%
