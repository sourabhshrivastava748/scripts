#!/usr/bin/python
import sys, datetime, pytz, re
from pymongo import MongoClient
from collections import Counter
import mysql.connector

#---
mobileListString = sys.argv[1]
mobileList = mobileListString.split(",")
for i in range(0, len(mobileList)):
	mobileList[i] = "\"" + mobileList[i] + "\""

separator = ","
mobileListString = separator.join(mobileList)	
print("Mobile list: " + mobileListString)


#---
reportDate = datetime.date.today()
reportDateString = reportDate.strftime("%Y-%m-%d")

outputFileName = "/tmp/unifill-data-export_" + reportDateString  + ".csv"
mysqlDbUri = "db-slave.address.unicommerce.infra"
dbName = "turbo"


#---
try: 
	outputFile = open(outputFileName, "w")

	if (len(mobileList) > 1000) :
		outputFile.write("At max 1000 mobiles are allowed for data export")

	else:
		mysqlDbClient = mysql.connector.connect(
		  host = mysqlDbUri,
		  user ="developer",
		  passwd ="DevelopeR@4#",
		  database = dbName
		)
		mysqlDbCursor = mysqlDbClient.cursor();

		unifillDataExportQuery = "select turbo_mobile, address_line1, address_line2, city, district, state_code, country_code, pincode, shipping_package_uc_status, uniware_sp_created, uniware_sp_updated from shipping_package_address where turbo_mobile in (" + mobileListString + ")";

		print("unifillDataExportQuery : " + unifillDataExportQuery)

		mysqlDbCursor.execute(unifillReportQuery)

		columnHeadings = "turbo_mobile, address_line1, address_line2, city, district, state_code, country_code, pincode, shipping_package_uc_status, uniware_sp_created, uniware_sp_updated"
		print(columnHeadings)

		outputFile.write(columnHeadings + "\n")
		
		for row in mysqlDbCursor.fetchall():
			address_details = (
				"\"" + str(row[0]) + "\"" + 
				"\"" + str(row[1]) + "\"" + 
				"\"" + str(row[2]) + "\"" + 
				"\"" + str(row[3]) + "\"" + 
				"\"" + str(row[4]) + "\"" + 
				"\"" + str(row[5]) + "\"" + 
				"\"" + str(row[6]) + "\"" + 
				"\"" + str(row[7]) + "\"" + 
				"\"" + str(row[8]) + "\"" + 
				"\"" + str(row[9]) + "\"" + 
				"\"" + str(row[10]) + "\"" + 
				"\"" + str(row[11]) + "\""
			)
			outputFile.write(summary + "\n")

	print("-- FINISHED --")

except Exception as e:
	print(e)
	print(sys.exc_info()[0]);
	print("FAILED");

finally:
	mysqlDbClient.close()
	outputFile.close()

