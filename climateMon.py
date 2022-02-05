#----------------------------------------------------------------
# Filename: climateMon.py
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
# to fit this program
#-----------------------------------------------------------------

import time
import datetime

# Client library for the thingspeak.com API 
import thingspeak  

# ThingSpeak channel credentials 
chId = 1637741
tsKey= 'XXXX'
tsUrl='https://api.thingspeak.com/update'
ts = thingspeak.Channel(chId, tsUrl ,tsKey)

# DS18B20 1-Wire library
import ds18b20 as _ds18b20 
ds18b20Sensor = _ds18b20.DS18B20() # By default GPIO 4

# DHT11 Library 
import dht11
dht = dht11.DHT11(7) # GPIO 7

# BMP280 library
import bmp280 as _BMP280
bmp280Sensor = _BMP280.BMP280()

# Global Variables
global altReal # Defined altitude
global ds18b20id
altReal = 90
ds18b20id = '28-021605d51cee'

# Get data (from local sensors)
def getLocalData():
	global timeString
	global humDHT	# Humidity
	global tempDHT
	global tempDS18B20
	global tempIn
	global pSL	# Sea level pressure
	global alt	# Calculated altitude
	global pAbs	# Absolute pressure
	
	# Get time of reading
	now = datetime.datetime.now()
	timeString = now.strftime("%Y-%m-%d %H:%M")
	
	# Read DS18B20 Temperature
	tempDS18B20 = round(ds18b20Sensor.readSensor(ds18b20id), 1)

	# Read BMP280 Data
	tempIn, pAbs, alt, pSL = bmp280GetData(altReal) 
	
	humDHT, tempDHT = dht.read()
	if humDHT is not None and tempDHT is not None:
		hum = round (humDHT)

# Get BMP280 data		
def bmp280GetData(altitude):
	
	temp = bmp280Sensor.get_temperature()
	pres = bmp280Sensor.get_pressure()
	alt =  bmp280Sensor.get_altitude()
	presSeaLevel = pres / pow(1.0 - altitude/44330.0, 5.255) 
	
	temp = round (temp, 1)
	pres = round (pres, 2)	# Absolute pressure in hPa (mbar)
	alt = round (altitude) 	# Absolute altitude
	presSeaLevel = round (presSeaLevel, 2) 	# Sea level pressure in hPa (mbar)

	return temp, pres, alt, presSeaLevel

# Send data to ThingSpeak
def sendDataTs():
	data = {"field1": tempDS18B20,
		"field2": humDHT, 
		"field3": pSL 
		}
	ts.update(data)
	print ("[INFO] Data sent for  fields: ", tempDS18B20, humDHT, pSL)
  
# Main function
def main():	
	print ("[INFO] Initiating")
	while True:
		getLocalData()
		try:
			sendDataTs()
			time.sleep(3600) # Every 60 min
		except (KeyboardInterrupt):
			print ("[INFO] Finishing")
			break

''''--------------------------------------------------------------'''
if __name__ == '__main__':
	main()
