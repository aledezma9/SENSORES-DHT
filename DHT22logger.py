# Copyright (c) 2019
# Author: Arturo Ledezma



#!/usr/bin/python2
#coding=utf-8

import sys
import logging, logging.handlers

from Debugger.Logger import Logger
from Utility.MailSender import MailSender
from Utility.WeeklyAverages import WeeklyAverages
from Database.DbActionController import DbController
from Configurations.ConfigHandler import ConfigHandler
from Sensors.SensorDataHandler import SensorDataHandler

def main():

	
	try:
		Logger()
		logger = logging.getLogger()
	
	except Exception as e: 
		print('Logger initialization failed. Error:\n{0}\nTry adding write permission directly to root (DHT22-TemperatureLogger) folder with "sudo chmod -R 777"'.format(e))
		sys.exit(0)

	
	logger.info("DHT22logger execution started")

	
	try:
		configurationHandler = ConfigHandler()
		configurations = configurationHandler.getFullConfiguration()
	except Exception as e:
		logger.error('Failed to get configurations:\n',exc_info=True)
		sys.exit(0)

	
	try:
		dbControl = DbController(configurations)
	except Exception as e:
		logger.error("dbController instantiation failed:\n",exc_info=True)
		sys.exit(0)

	
	try:
		mailSender = MailSender(configurations, dbControl)
		mailSenderAvailable = True
	except Exception as e:
		mailSenderAvailable = False
		logger.error('MailSender instantiation failed:\n',exc_info=True)

	
	try:
		SensorDataHandler(configurations,dbControl,mailSender).readAndStoreSensorReadings()
	except Exception as e:
		logger.error('Sensor data handling failed:\n',exc_info=True)
		if mailSenderAvailable:
			try:
				mailSender.sendWarningEmail("Error with sensor data handling.\nError message: {0}".format(e.message))
			except:
				logger.error('Sending warning mail failed\n',exc_info=True)

	
	if mailSenderAvailable:
		logger.info("Check if weekly averages need to be sended")

		
		if configurationHandler.isWeeklyAveragesConfigEnabled():
			
			averagesSender = WeeklyAverages(configurations,dbControl,mailSender)

			
			try:			
				
				averagesSender.performWeeklyAverageMailSending()
			
			except Exception as e:
				logger.error('Failed to check weekly averages\n',exc_info=True)
				try:
					mailSender.sendWarningEmail("Failed to send weekly averages.\nError message: {0}\nCheck debug log from Raspberry for more information".format(e.message))
				except Exception as e:
					logger.error('Failed to send email\n',exc_info=True)

	
	if configurationHandler.isBackupDumpConfigEnabled():
		
		logger.info("Starting sql backup dump")
		try:
			
			dbControl.createSqlBackupDump()
		except Exception as e:
			logger.error('Failed to create SQL backup dump')
			if mailSenderAvailable:
				logger.error('Exception in DbBackupControl\n',exc_info=True)
				try:
					mailSender.sendWarningEmail('SQL Backup dump failed. Check debug log from raspberrypi for information')
				except Exception as e:
					logger.error('Failed to send email:\n',exc_info=True)
		logger.info("Sql backup dump finished")

	logger.info("DHT22logger execution finished\n")

if __name__ == "__main__":
	main()
