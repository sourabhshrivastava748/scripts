#!/usr/bin/python
import sys, datetime, pytz, re
from pymongo import MongoClient
from collections import Counter

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


def calculateCount(name, ufData):
	counter = 0
	for data in ufData:
		if (data['summary'] == name):
			counter = counter + 1

	return counter

def getSummary(ufData):
	if (ufData.count() > 0):
		tenantCode = ufData[0]['tenantCode']
		# channelIssue = Counter(tok['summary'] for tok in ufData)['CHANNEL_ISSUE']
		# syncTimingIssue = Counter(tok['summary'] for tok in ufData)['SYNC_TIMING_ISSUE']
		# operationalIssue = Counter(tok['summary'] for tok in ufData)['OPERATIONAL_ISSUE']
		# facilityMappingIssue = Counter(tok['summary'] for tok in ufData)['FACILITY_MAPPING_ISSUE']
		# inventoryFormulaIssue = Counter(tok['summary'] for tok in ufData)['INVENTORY_FORMULA_ISSUE']
		# summaryUnavailable = Counter(tok['summary'] for tok in ufData)['SUMMARY_UNAVAILABLE']

		channelIssue = calculateCount('CHANNEL_ISSUE', ufData)
		syncTimingIssue = calculateCount('SYNC_TIMING_ISSUE', ufData)
		operationalIssue = calculateCount('OPERATIONAL_ISSUE', ufData)
		facilityMappingIssue = calculateCount('FACILITY_MAPPING_ISSUE', ufData)
		inventoryFormulaIssue = calculateCount('INVENTORY_FORMULA_ISSUE', ufData)
		summaryUnavailable = calculateCount('SUMMARY_UNAVAILABLE', ufData)

		summary = tenantCode + "," + str(summaryUnavailable) + str(ufData.count()) + "," + str(channelIssue) + "," + str(syncTimingIssue) + "," + str(operationalIssue) + "," + str(facilityMappingIssue) + "," + str(inventoryFormulaIssue) + "," + str(summaryUnavailable) 

	else:
		summary = ""

	return summary

# Input
tenantCodeList = ["capl"]
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
	uri1 = "mongo1.e2-in.unicommerce.infra:27017"
	uri2 = "mongo2.e2-in.unicommerce.infra:27017"

	# Create mongo client
	myclient = getClient(uri1, uri2)
	mydb = myclient[tenantCode]
	mycol = mydb[colName]

	# Get ufData
	query = {
		"tenantCode" : tenantCode,
		"currentStatus" : "UNFULFILLABLE",
		"unfulfillableTimeStamp" : { "$gte" : utcMidnightDateTime }
	}
	projection = {
		"tenantCode": 1,
		'saleOrderCode' : 1,
		'summary': 1
	}

	ufData = mycol.find(query, projection) 			# TODO: use projection 
	
	# Get Summary
	summary = getSummary(ufData)
	print(summary)
	outputFile.write(summary + "\n")


outputFile.close()


