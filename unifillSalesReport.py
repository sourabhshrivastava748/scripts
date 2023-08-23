#!/usr/bin/python
import sys, datetime, pytz, re
from pymongo import MongoClient
from collections import Counter
import mysql.connector


# Create report file
fromDate = datetime.date.today() - datetime.timedelta(days = 60)
fromDateString = fromDate.strftime("%Y-%m-%d")
toDateString = datetime.date.today().strftime("%Y-%m-%d")

print("fromDate: " + fromDateString)
print("toDate: " + toDateString)

outputFileName = "/tmp/unifill-sales-report_" + fromDateString  + "_to_" + toDateString  + ".csv"
outputFile = open(outputFileName, "w")
outputFile.write("Tenant,LookupsFound,FromDate,ToDate\n")


mysqlDbUri = "db.address.unicommerce.infra"
dbName = "turbo"

mysqlDbClient = mysql.connector.connect(
  host = mysqlDbReplicaUri,
  user ="developer",
  passwd ="DevelopeR@4#",
  database = dbName
)
mysqlDbCursor = mysqlDbClient.cursor();

tenantLookupQuery = "select tenant_code, count(lookup_status) from address_lookup_trace where tenant_code in (select distinct(tenant_code) from tenant_details) and lookup_status = 'FOUND' and created_at between " + fromDateString + " and " + toDateString + " group by tenant_code;"
print("tenantLookupQuery : " + tenantLookupQuery)

try:
	mysqlDbCursor.execute(soiCountQuery)

	print("Tenant,LookupsFound,FromDate,ToDate")
	for row in mysqlDbCursor.fetchall():
		tenant = row[0]
		lookupsFound = row[1]
		summary = str(tenant) + "," + str(lookupsFound) + "," + fromDateString + "," + toDateString
		print(summary)
		outputFile.write(summary + "\n")

except Exception as e:
	print(e)
	print(sys.exc_info()[0]);
	print("FAILED");

finally:
	mysqlDbClient.close()
	outputFile.close()

