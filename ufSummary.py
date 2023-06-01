#!/usr/bin/python
import sys, datetime, pytz, re
from pymongo import MongoClient

def getClient(uri1, uri2):
	try:
	    c = MongoClient(uri1, 27017);
	    db= c['uniwareConfig'];
	    db.test.insert_one({});
	    print(str(uri1))
	except:
	    c = MongoClient(uri2, 27017);
	    print(str(uri2) + " - common changed")

	return c

# Input
tenantCodeList = ["tcns"]
colName = "unfulfillableItemsSnapshot"
print("Tenant list: " + str(tenantCodeList))

# Create output file
outputFileName = "/tmp/uf-summary-" + datetime.date.today().strftime("%d-%m-%Y") + ".csv"
outputFile = open(outputFileName, "w")
outputFile.write("Tenant,TotalUFCount,ChannelIssue,SyncTimingIssue,OperationalIssue,FacilityMappingIssue,InventoryFormulaIssue,SummaryUnavailable,Date\n")

utcMidnightDateTime = datetime.datetime.today().replace(hour = 0, minute = 0, second = 0, microsecond = 0).astimezone(pytz.UTC)
print("utcMidnightDateTime: " + str(utcMidnightDateTime))

# For all tenants
for tenantCode in tenantCodeList:
	# Get mongodbUri of tenant 			# TODO
	uri1 = "mongo1.e1-in.unicommerce.infra:27017"
	uri2 = "mongo2.e1-in.unicommerce.infra:27017"

	# Create mongo client
	myclient = getClient(uri1, uri2)
	mydb = myclient[tenantCode]
	mycol = mydb[colName]

	# Get ufData
	query = {
		"tenantCode" : tenantCode,
		"currentStatus" : "UNFULFILLABLE",
		"created" : { "$gte" : utcMidnightDateTime }
	}
	projection = {
		'saleOrderItemCode' : 1,
		'summary': 1
	}

	ufData = mycol.find(query, projection).limit(1) 			# TODO: use projection 
	
	for data in ufData:
		print(data)
		# print(str(tenantCode) + "SOI code: "+ str(data['summary']) + ", Summary: " + str(data['summary']))
		# outputFile.write(str(tenantCode) + "SOI code: "+ str(data['summary']) + ", Summary: " + str(data['summary']) + "\n")
	
	print("")

	# Write to file

outputFile.close()


