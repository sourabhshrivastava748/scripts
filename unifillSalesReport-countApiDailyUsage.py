#!/usr/bin/python
import sys, datetime, re
from pymongo import MongoClient
from collections import Counter
import mysql.connector


# FromDate : First day of the month (based on yesterday's date) 
fromDate = datetime.date.today() - datetime.timedelta(days = 1)
fromDateString = fromDate.strftime("%Y-%m-%d")

# ToDate for the report
toDate = datetime.date.today() - datetime.timedelta(days = 1)
toDateString = toDate.strftime("%Y-%m-%d")

# ToDate for the query : Today's date (less than query)
todayDate = datetime.date.today()
todayDateString = todayDate.strftime("%Y-%m-%d")

# fromDateString = "2023-07-18"
# toDateString = "2023-08-17"

print("-- Unifill Sales Report Count API Daily Usage --")
print("fromDate: " + fromDateString)
print("toDate (inclusive): " + toDateString)

# Create report file
outputFileName = "/tmp/unifill-count-api-daily-usage_" + toDateString  + ".csv"
# outputFileName = "/tmp/unifill-sales-report_" + fromDateString + "_to_" + toDateString  + ".csv"

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

# unifillReportQuery = "SELECT tenant_code, count(*) AS total_lookups, SUM(CASE WHEN lookup_status = 'FOUND' THEN 1 ELSE 0 END) AS lookups_found, SUM(CASE WHEN lookup_status = 'NOT_FOUND' THEN 1 ELSE 0 END) AS lookups_not_found, COUNT(DISTINCT CASE WHEN lookup_status = 'FOUND' THEN mobile END) AS lookups_found_unique_mobiles FROM address_lookup_trace WHERE     tenant_code IN (SELECT DISTINCT(tenant_code) FROM tenant_details) AND created_at >= '" + fromDateString + "' AND created_at < '" + todayDateString + "' GROUP BY tenant_code;"


unifillReportQuery = """select tenant_code, 
		count(*) as total_api_hits, 
		count(distinct(mobile)) as unique_mobile,
		SUM(CASE WHEN address_count > 0 THEN 1 ELSE 0 END) AS address_found, 
		SUM(CASE WHEN address_count = 0 THEN 1 ELSE 0 END) AS address_not_found 
	from 
		address_count_trace 
	where 
		created_at >= '""" + fromDateString + """' AND 
		created_at < '""" + todayDateString + """' 
	group by 
		tenant_code"""

print("unifillReportQuery : " + unifillReportQuery)

try:
	mysqlDbCursor.execute(unifillReportQuery)

	columnHeadings = "Tenant,TotalApiHits,UniqueMobile,AddressFound,AddressNotFound,Date"
	print(columnHeadings)

	outputFile.write(columnHeadings + "\n")
	
	for row in mysqlDbCursor.fetchall():
		tenant = row[0]
		totalApiHits = row[1]
		uniqueMobile = row[2]
		addressFound = row[3]
		addressNotFound = row[4]

		summary = (str(tenant) + "," 
						+ str(totalApiHits) + "," 
						+ str(uniqueMobile) + "," 
						+ str(addressFound) + ","
						+ str(addressNotFound) + ","
						+ toDateString)
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

