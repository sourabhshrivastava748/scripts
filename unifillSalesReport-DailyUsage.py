#!/usr/bin/python
import sys, datetime, pytz, re
from pymongo import MongoClient
from collections import Counter
import mysql.connector



# FromDate : First day of the month (based on yesterday's date) 
fromDate = datetime.date.today() - datetime.timedelta(days = 2)
fromDateString = fromDate.strftime("%Y-%m-%d")

# ToDate for the report
toDate = datetime.date.today() - datetime.timedelta(days = 1)
toDateString = toDate.strftime("%Y-%m-%d")

# ToDate for the query : Today's date (less than query)
todayDate = datetime.date.today()
todayDateString = todayDate.strftime("%Y-%m-%d")

# fromDateString = "2023-07-18"
# toDateString = "2023-08-17"

print("-- Unifill Sales Report Daily Usage --")
print("fromDate: " + fromDateString)
print("toDate (inclusive): " + toDateString)

# Create report file
outputFileName = "/tmp/unifill-sales-report-daily-usage_" + toDateString  + ".csv"
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

unifillReportQuery = "SELECT tenant_code, count(*) AS total_lookups, SUM(CASE WHEN lookup_status = 'FOUND' THEN 1 ELSE 0 END) AS lookups_found, SUM(CASE WHEN lookup_status = 'NOT_FOUND' THEN 1 ELSE 0 END) AS lookups_not_found, COUNT(DISTINCT CASE WHEN lookup_status = 'FOUND' THEN mobile END) AS lookups_found_unique_mobiles FROM address_lookup_trace WHERE     tenant_code IN (SELECT DISTINCT(tenant_code) FROM tenant_details) AND created_at >= '" + fromDateString + "' AND created_at < '" + todayDateString + "' GROUP BY tenant_code;"


# unifillReportQuery = "SELECT tenant_code, count(*) AS total_lookups, SUM(CASE WHEN lookup_status = 'FOUND' THEN 1 ELSE 0 END) AS lookups_found, SUM(CASE WHEN lookup_status = 'NOT_FOUND' THEN 1 ELSE 0 END) AS lookups_not_found, COUNT(DISTINCT CASE WHEN lookup_status = 'FOUND' THEN mobile END) AS lookups_found_unique_mobiles FROM address_lookup_trace WHERE     tenant_code IN (SELECT DISTINCT(tenant_code) FROM tenant_details) AND created_at BETWEEN '" + fromDateString + "' AND '" + toDateString + "' AND mobile NOT IN ('+919999900000','+919999911111','+919999999999','+919901033800','+919711903969','+919428140479','+919015238030','+919315974807','+919663265675','+919468283901','+918126148700','+918700789547') GROUP BY tenant_code;"

print("unifillReportQuery : " + unifillReportQuery)

try:
	mysqlDbCursor.execute(unifillReportQuery)

	columnHeadings = "Tenant,TotalLookups,LookupsFound,LookupsNotFound,UniqueMobileForLookupsFound,Date"
	print(columnHeadings)

	outputFile.write(columnHeadings + "\n")
	
	for row in mysqlDbCursor.fetchall():
		tenant = row[0]
		totalLookups = row[1]
		lookupsFound = row[2]
		lookupsNotFound = row[3]
		uniqueMobileForLookupsFound = row[4]
		summary = (str(tenant) + "," 
						+ str(totalLookups) + "," 
						+ str(lookupsFound) + "," 
						+ str(lookupsNotFound) + "," 
						+ str(uniqueMobileForLookupsFound) + "," 
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

