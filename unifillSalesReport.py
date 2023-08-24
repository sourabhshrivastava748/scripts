#!/usr/bin/python
import sys, datetime, pytz, re
from pymongo import MongoClient
from collections import Counter
import mysql.connector



# FromDate : First day of the month
fromDate = datetime.date.today().replace(day=1)
fromDateString = fromDate.strftime("%Y-%m-%d")
# ToDate : Yesterday
toDate = datetime.date.today() - datetime.timedelta(days = 1)
toDateString = toDate.strftime("%Y-%m-%d")

# fromDateString = "2023-07-01"
# toDateString = "2023-07-31"

print("-- Unifill Sales Report MTD --")
print("fromDate: " + fromDateString)
print("toDate: " + toDateString)

# Create report file
outputFileName = "/tmp/unifill-mtd-sales-report_" + toDateString  + ".csv"
outputFile = open(outputFileName, "w")


mysqlDbUri = "db.address.unicommerce.infra"
dbName = "turbo"

mysqlDbClient = mysql.connector.connect(
  host = mysqlDbUri,
  user ="developer",
  passwd ="DevelopeR@4#",
  database = dbName
)
mysqlDbCursor = mysqlDbClient.cursor();

tenantLookupQuery = "SELECT tenant_code, count(*) AS total_lookups, SUM(CASE WHEN lookup_status = 'FOUND' THEN 1 ELSE 0 END) AS lookups_found, SUM(CASE WHEN lookup_status = 'NOT_FOUND' THEN 1 ELSE 0 END) AS lookups_not_found, COUNT(DISTINCT CASE WHEN lookup_status = 'FOUND' THEN mobile END) AS lookups_found_unique_mobiles FROM address_lookup_trace WHERE     tenant_code IN (SELECT DISTINCT(tenant_code) FROM tenant_details) AND created_at BETWEEN '" + fromDateString + "' AND '" + toDateString + "' GROUP BY tenant_code;"


print("tenantLookupQuery : " + tenantLookupQuery)

try:
	mysqlDbCursor.execute(tenantLookupQuery)

	outputFile.write("Tenant,TotalLookups,LookupsFound,LookupsNotFound,UniqueMobileForLookupsFound,Date\n")
	print("Tenant,TotalLookups,LookupsFound,LookupsNotFound,UniqueMobileForLookupsFound,Date")
	
	for row in mysqlDbCursor.fetchall():
		tenant = row[0]
		totalLookups = row[1]
		lookupsFound = row[2]
		lookupsNotFound = row[3]
		uniqueMobileForLookupsFound = row[4]
		summary = str(tenant) + "," + str(totalLookups) + "," + str(lookupsFound) + "," + str(lookupsNotFound) + "," + str(uniqueMobileForLookupsFound) + "," + toDateString
		print(summary)
		outputFile.write(summary + "\n")

	print("-- FINISHED --")

except Exception as e:
	print(e)
	print(sys.exc_info()[0]);
	print("FAILED");

finally:
	mysqlDbClient.close()
	outputFile.close()

