#!/usr/bin/python
import sys, datetime, pytz, re
from pymongo import MongoClient
from collections import Counter
import mysql.connector


tenantList = [
				 {
				   "code": "bataindialtd",
				   "category": "Focus 30"
				 },
				 {
				   "code": "bestseller",
				   "category": "Focus 30"
				 },
				 {
				   "code": "boatlifestyle",
				   "category": "Focus 30"
				 },
				 {
				   "code": "bodycupid",
				   "category": "Focus 30"
				 },
				 {
				   "code": "brandstudio",
				   "category": "Focus 30"
				 },
				 {
				   "code": "brightlifecareindia",
				   "category": "Focus 30"
				 },
				 {
				   "code": "capl",
				   "category": "Focus 30"
				 },
				 {
				   "code": "curefit",
				   "category": "Focus 30"
				 },
				 {
				   "code": "edamama",
				   "category": "Focus 30"
				 },
				 {
				   "code": "fabbag",
				   "category": "Focus 30"
				 },
				 {
				   "code": "fabindialimited",
				   "category": "Focus 30"
				 },
				 {
				   "code": "forevernew98",
				   "category": "Focus 30"
				 },
				 {
				   "code": "gocolors",
				   "category": "Focus 30"
				 },
				 {
				   "code": "helioslifestyle",
				   "category": "Focus 30"
				 },
				 {
				   "code": "imfirefly",
				   "category": "Focus 30"
				 },
				 {
				   "code": "jnelogistic",
				   "category": "Focus 30"
				 },
				 {
				   "code": "juscorp",
				   "category": "Focus 30"
				 },
				 {
				   "code": "kehpl",
				   "category": "Focus 30"
				 },
				 {
				   "code": "kottylifestyle",
				   "category": "Focus 30"
				 },
				 {
				   "code": "maisondauraine",
				   "category": "Focus 30"
				 },
				 {
				   "code": "mamaearth",
				   "category": "Focus 30"
				 },
				 {
				   "code": "mosaicwellnesspvtlmt",
				   "category": "Focus 30"
				 },
				 {
				   "code": "pep",
				   "category": "Focus 30"
				 },
				 {
				   "code": "rarerabbit",
				   "category": "Focus 30"
				 },
				 {
				   "code": "tcns",
				   "category": "Focus 30"
				 },
				 {
				   "code": "tmrw",
				   "category": "Focus 30"
				 },
				 {
				   "code": "twt",
				   "category": "Focus 30"
				 },
				 {
				   "code": "urbanclap",
				   "category": "Focus 30"
				 },
				 {
				   "code": "4mclothingllp",
				   "category": "UF Tracked Client"
				 },
				 {
				   "code": "enamorecom",
				   "category": "UF Tracked Client"
				 },
				 {
				   "code": "fashorlifestyle",
				   "category": "UF Tracked Client"
				 },
				 {
				   "code": "hopscotch",
				   "category": "UF Tracked Client"
				 },
				 {
				   "code": "leayanglobal",
				   "category": "UF Tracked Client"
				 },
				 {
				   "code": "nuawoman",
				   "category": "UF Tracked Client"
				 },
				 {
				   "code": "plumgoodness",
				   "category": "UF Tracked Client"
				 },
				 {
				   "code": "portronics",
				   "category": "UF Tracked Client"
				 },
				 {
				   "code": "quickshift",
				   "category": "UF Tracked Client"
				 },
				 {
				   "code": "upscalio",
				   "category": "UF Tracked Client"
				 },
				 {
				   "code": "vivaantafashion",
				   "category": "UF Tracked Client"
				 }
			]


print("Tenant list: " + str(tenantList))




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


def getTenantCategory(tenantCode):
	for tenant in tenantList:
		if (tenantCode == tenant['code']):
			return tenant['category']

	return ""

def getSummary(ufData, tenantCode, date):
	totalUFCount = len(ufData)
	totalSoiCount = int(getTotalSOICount(tenantCode))

	if ((len(ufData) > 0) and (ifSummaryExists(ufData))):
		tenantCode = ufData[0]['tenantCode']
		channelIssue = Counter(tok['summary'] for tok in ufData)['CHANNEL_ISSUE']
		syncTimingIssue = Counter(tok['summary'] for tok in ufData)['SYNC_TIMING_ISSUE']
		operationalIssue = Counter(tok['summary'] for tok in ufData)['OPERATIONAL_ISSUE']
		facilityMappingIssue = Counter(tok['summary'] for tok in ufData)['FACILITY_MAPPING_ISSUE']
		inventoryFormulaIssue = Counter(tok['summary'] for tok in ufData)['INVENTORY_FORMULA_ISSUE']
		summaryUnavailable = Counter(tok['summary'] for tok in ufData)['SUMMARY_UNAVAILABLE']

		if (totalSoiCount != 0):
			ufPercentage = round(((float(totalUFCount) / totalSoiCount) * 100), 3);
			nonOpsUf = channelIssue + syncTimingIssue + summaryUnavailable
			nonOpsUfPercentage = round(((float(nonOpsUf) / totalSoiCount) * 100), 3);

		summary = (tenantCode + "," 
			+ getTenantCategory(tenantCode) + "," 
			+ str(totalSoiCount) + "," 
			+ str(totalUFCount) + "," 
			+ str(ufPercentage) + "," 
			+ str(nonOpsUfPercentage) + "," 
			+ str(channelIssue) + "," 
			+ str(syncTimingIssue) + "," 
			+ str(operationalIssue) + "," 
			+ str(facilityMappingIssue) + "," 
			+ str(inventoryFormulaIssue) + "," 
			+ str(summaryUnavailable) + "," 
			+ str(date))

	elif (len(ufData) == 0): 
		summary = (tenantCode + "," 
			+ getTenantCategory(tenantCode) + "," 
			+ str(totalSoiCount) + "," 
			+ str(totalUFCount) + "," 
			+ "0,0,,,,,,," 
			+ str(date))

	else:
		print("ufData length: " + str(len(ufData)))
		summary = (tenantCode + "," 
			+ getTenantCategory(tenantCode) + "," 
			+ str(totalSoiCount) + "," 
			+ str(totalUFCount) + "," 
			+ ",,,,,,,," 
			+ str(date))

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


def getMysqlDBFromServerName(serverName):
	# Get Mysql DB replica 
	commonMongoUri1 = "common1.mongo.unicommerce.infra:27017"
	commonMongoUri2 = "common2.mongo.unicommerce.infra:27017"
	commonMongoClient = getClient(commonMongoUri1, commonMongoUri2)
	db = commonMongoClient['uniwareConfig']
	col = db['serverDetails']

	return col.find_one({"name" : serverName})['replicatedTo']



def getDbNameFromServerName(serverName):
	dedicatedReplica = ["Myntra", "Lenskart", "BrandStudio", "MamaEarth", "Ril", "ECloud3" , "ECloud2" , "ECloud1", "ECloud4", "Dhani", "ECloud5", "ECloud6", "Cloud37", "UniStage"]

	if (serverName in dedicatedReplica):
		return "uniware"
	else:
		return serverName



def getTotalSOICount(tenantCode):
	try:
		print("Getting SOI count for tenant: " + tenantCode)

		serverName = getServerNameFromTenant(tenantCode)
		print(tenantCode + ", Server Name: " + serverName)
		if (serverName):
			mysqlDbReplicaUri = getMysqlDBFromServerName(serverName)
			print("Server Name: " + serverName + ", : MySQLdb: " + str(mysqlDbReplicaUri))
		else :
			print("Cannot find serverName for " + str(tenantCode))

		dbName = getDbNameFromServerName(serverName)

		mysqlDbClient = mysql.connector.connect(
			  host = mysqlDbReplicaUri,
			  user ="developer",
			  passwd ="DevelopeR@4#",
			  database = dbName
			)
		mysqlDbCursor = mysqlDbClient.cursor();

		soiCountQuery = "select count(*) from sale_order_item soi join sale_order so on soi.sale_order_id = so.id join tenant t on so.tenant_id = t.id where soi.created > '" + totalSoiCountFromDate + "' and soi.created < '" + totalSoiCountToDate + "' and t.code = '" + tenantCode + "';"
		print("soiCountQuery : " + soiCountQuery)

		mysqlDbCursor.execute(soiCountQuery)

		for row in mysqlDbCursor.fetchall():
			soiCount = row[0]

		print("Tenant: " + tenantCode + ", soiCount: " + str(soiCount))
	except Exception as e:
		print(e)
		print(sys.exc_info()[0]);
		print("FAILED");
	finally:
		mysqlDbClient.close()

	return str(soiCount)






# 										-- Main --
try:
	ufColName = "unfulfillableItemsSnapshot"

	midnightDateTime_today = datetime.datetime.today().replace(hour = 0, minute = 0, second = 0, microsecond = 0)
	midnightDateTime_yesterday = midnightDateTime_today - datetime.timedelta(days = 1)

	utcMidnightDateTime_today = midnightDateTime_today.astimezone(pytz.UTC)
	utcMidnightDateTime_yesterday = midnightDateTime_yesterday.astimezone(pytz.UTC)
	ufSummaryDate = datetime.date.today() - datetime.timedelta(days = 1)
	ufSummaryDateStr = ufSummaryDate.strftime("%d-%m-%Y")

	totalSoiCountFromDate = ufSummaryDate.strftime("%Y-%m-%d")
	totalSoiCountToDate = datetime.date.today().strftime("%Y-%m-%d")

	print("utcMidnightDateTime_today: " + str(utcMidnightDateTime_today))
	print("utcMidnightDateTime_yesterday: " + str(utcMidnightDateTime_yesterday))
	print("ufSummaryDate: " + str(ufSummaryDate))

	# Create output file
	outputFileName = "/tmp/uf-summary-" + ufSummaryDateStr + ".csv"
	outputFile = open(outputFileName, "w")
	outputFile.write("Tenant,TenantCategory,TotalSOICount,TotalUFCount,UFPercentage,NonOpsUFPercentage,ChannelIssue,SyncTimingIssue,OperationalIssue,FacilityMappingIssue,InventoryFormulaIssue,SummaryUnavailable,Date\n")

	# For all tenants
	for tenant in tenantList:
		try:
			# Get mongodbUri of tenant 			
			mongoUri = []
			mongoUri = getTenantSpecificMongoUri(tenant['code'])

			if (len(mongoUri) == 2):
				# Create mongo client
				myclient = getClient(mongoUri[0], mongoUri[1])
				mydb = myclient[tenant['code']]
				mycol = mydb[ufColName]

				# Get ufData
				query = {
					"tenantCode" : tenant['code'],
					"currentStatus" : "UNFULFILLABLE",
					"unfulfillableTimeStamp" : { 
						"$gte" : utcMidnightDateTime_yesterday, 
						"$lte" : utcMidnightDateTime_today 
					}
				}
				projection = {
					"tenantCode": 1,
					'saleOrderCode' : 1,
					'summary': 1
				}

				ufData = list(mycol.find(query, projection)) 			

				# Get Summary
				summary = getSummary(ufData, tenant['code'], str(ufSummaryDateStr))
				print(summary)
				outputFile.write(summary + "\n")

		except Exception as e:
			print("Exception while calculating uf data for tenant: " + tenant['code'])
			print(e)

except Exception as e:
	print(e)
	print(sys.exc_info()[0]);
	print("FAILED");

finally:
	outputFile.close()

