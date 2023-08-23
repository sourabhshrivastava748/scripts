#!/usr/bin/python
import sys, datetime, pytz, re
from pymongo import MongoClient
from collections import Counter
import mysql.connector


# Create report file
# fromDate = datetime.date.today() - datetime.timedelta(days = 60)
# fromDateString = fromDate.strftime("%Y-%m-%d")
# toDateString = datetime.date.today().strftime("%Y-%m-%d")

fromDateString = "2023-07-01"
toDateString = "2023-07-31"

print("fromDate: " + fromDateString)
print("toDate: " + toDateString)

outputFileName = "/tmp/unifill-sales-report_" + fromDateString  + "_to_" + toDateString  + ".csv"
outputFile = open(outputFileName, "w")
outputFile.write("Tenant,LookupsFound,FromDate,ToDate\n")


mysqlDbUri = "db.address.unicommerce.infra"
dbName = "turbo"

mysqlDbClient = mysql.connector.connect(
  host = mysqlDbUri,
  user ="developer",
  passwd ="DevelopeR@4#",
  database = dbName
)
mysqlDbCursor = mysqlDbClient.cursor();

tenantLookupQuery = "select tenant_code, count(lookup_status) from address_lookup_trace where tenant_code in (select distinct(tenant_code) from tenant_details) and lookup_status = 'FOUND' and created_at between '" + fromDateString + "' and '" + toDateString + "' group by tenant_code;"


tenantLookupQuery = "SELECT tenant_code, count(*) AS total_lookups, SUM(CASE WHEN lookup_status = 'FOUND' THEN 1 ELSE 0 END) AS lookups_found, SUM(CASE WHEN lookup_status = 'NOT_FOUND' THEN 1 ELSE 0 END) AS lookups_not_found, COUNT(DISTINCT CASE WHEN lookup_status = 'FOUND' THEN mobile END) AS lookups_found_unique_mobiles FROM address_lookup_trace WHERE     tenant_code IN (SELECT DISTINCT(tenant_code) FROM tenant_details) AND created_at BETWEEN '" + fromDateString + "' AND '" + toDateString + "' GROUP BY tenant_code;"


print("tenantLookupQuery : " + tenantLookupQuery)

try:
	mysqlDbCursor.execute(tenantLookupQuery)

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

except Exception as e:
	print(e)
	print(sys.exc_info()[0]);
	print("FAILED");

finally:
	mysqlDbClient.close()
	outputFile.close()

