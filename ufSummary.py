#!/usr/bin/python
import sys, datetime, pytz, re
from pymongo import MongoClient
from collections import Counter


tenantCodeList = ["mamaearth","brandstudio","capl","tcns","bestseller","urbanclap","boatlifestyle","helioslifestyle","mosaicwellnesspvtlmt","brightlifecareindia","twt","curefit","imfirefly","edamama","pep","rarerabbit","bodycupid","kehpl","kottylifestyle","bataindialtd","juscorp","fabindialimited","fabbag","forevernew98","maisondauraine","gocolors"]
print("Tenant list: " + str(tenantCodeList))



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


def ifSummaryExists(ufData):
	for data in ufData:
		if ("summary" not in data):
			return False

	return True


def getSummary(ufData, date):
	if ((len(ufData) > 0) and (ifSummaryExists(ufData))):
		tenantCode = ufData[0]['tenantCode']
		channelIssue = Counter(tok['summary'] for tok in ufData)['CHANNEL_ISSUE']
		syncTimingIssue = Counter(tok['summary'] for tok in ufData)['SYNC_TIMING_ISSUE']
		operationalIssue = Counter(tok['summary'] for tok in ufData)['OPERATIONAL_ISSUE']
		facilityMappingIssue = Counter(tok['summary'] for tok in ufData)['FACILITY_MAPPING_ISSUE']
		inventoryFormulaIssue = Counter(tok['summary'] for tok in ufData)['INVENTORY_FORMULA_ISSUE']
		summaryUnavailable = Counter(tok['summary'] for tok in ufData)['SUMMARY_UNAVAILABLE']

		summary = tenantCode + "," + str(len(ufData)) + "," + str(channelIssue) + "," + str(syncTimingIssue) + "," + str(operationalIssue) + "," + str(facilityMappingIssue) + "," + str(inventoryFormulaIssue) + "," + str(summaryUnavailable) + "," + str(date)

	else:
		print("ufData length: " + str(len(ufData)))
		summary = tenantCode + ",,,,,,,," 

	return summary


def getServerNameFromTenant(tenantCode):
	commonMongoUri1 = "common1.mongo.unicommerce.infra:27017"
	commonMongoUri2 = "common2.mongo.unicommerce.infra:27017"
	commonMongoClient = getClient(commonMongoUri1, commonMongoUri2)
	db = commonMongoClient['uniware']
	col = db['tenantProfile']

	return col.find_one({"tenantCode" : tenantCode})['serverName']


def getTenantSpecificMongoFromServerName(serverName):
	commonMongoUri1 = "common1.mongo.unicommerce.infra:27017"
	commonMongoUri2 = "common2.mongo.unicommerce.infra:27017"
	commonMongoClient = getClient(commonMongoUri1, commonMongoUri2)
	db = commonMongoClient['uniwareConfig']
	col = db['serverDetails']

	return col.find_one({"name" : serverName})['tenantSpecificMongoHosts']


def getTenantSpecificMongoUri(tenantCode):
	serverName = getServerNameFromTenant(tenantCode)
	print(tenantCode + ", Server Name: " + serverName)
	mongoUri = []
	if (serverName):
		mongoUri = getTenantSpecificMongoFromServerName(serverName)
		print("Server Name: " + serverName + ", mongoUri: " + str(mongoUri))
	else :
		print("Cannot find serverName for " + str(tenantCode))

	return mongoUri


# Input
ufColName = "unfulfillableItemsSnapshot"

# Create output file
outputFileName = "/tmp/uf-summary-" + datetime.date.today().strftime("%d-%m-%Y") + ".csv"
outputFile = open(outputFileName, "w")
outputFile.write("Tenant,TotalUFCount,ChannelIssue,SyncTimingIssue,OperationalIssue,FacilityMappingIssue,InventoryFormulaIssue,SummaryUnavailable,Date\n")

utcMidnightDateTime = datetime.datetime.today().replace(hour = 0, minute = 0, second = 0, microsecond = 0).astimezone(pytz.UTC)
print("utcMidnightDateTime: " + str(utcMidnightDateTime))

# For all tenants
for tenantCode in tenantCodeList:
	# Get mongodbUri of tenant 			
	mongoUri = []
	mongoUri = getTenantSpecificMongoUri(tenantCode)

	if (len(mongoUri) == 2):
		# Create mongo client
		myclient = getClient(mongoUri[0], mongoUri[1])
		mydb = myclient[tenantCode]
		mycol = mydb[ufColName]

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

		ufData = list(mycol.find(query, projection)) 			# TODO: use projection 

		# Get Summary
		summary = getSummary(ufData, datetime.datetime.today())
		print(summary)
		outputFile.write(summary + "\n")



outputFile.close()


