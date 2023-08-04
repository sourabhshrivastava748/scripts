#!/usr/bin/python
import sys, datetime, pytz, re
from pymongo import MongoClient
from collections import Counter
import mysql.connector
import json



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






# 										-- Main --


try:
	ufColName = "unfulfillableItemsSnapshot"

	# Get parameters 
	tenantCode = sys.argv[1]
	summary = sys.argv[2]
	created = sys.argv[3]
	toDate = datetime.strptime(created, "%d-%m-%Y")
	fromDate = toDate - datetime.timedelta(days = 1)

	toDate = toDate.astimezone(pytz.UTC)
	fromDate = fromDate.astimezone(pytz.UTC)



	print("tenantCode: " + str(tenantCode))
	print("summary: " + str(summary))
	print("fromDate: " + str(fromDate))
	print("toDate: " + str(toDate))

	# Create output file
	outputFileName = "/tmp/uf-soi-details-" + tenantCode + ".txt"
	outputFile = open(outputFileName, "w")
	# outputFile.write("Tenant,SaleOrderCode,SaleOrderItemCode,Facility,Created\n")

	# For all tenants
	try:
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
				"summary": summary,
				"unfulfillableTimeStamp" : { 
					"$gte" : fromDate, 
					"$lte" : toDate 
				}
			}
			projection = {
				"tenantCode": 1,
				'saleOrderCode' : 1,
				'saleOrderItemCode' : 1,
				"facilityAllocatorData.facilityCode": 1,
				'summary': 1,
				"created": 1
			}

			ufDetails = list(mycol.find(query, projection))
			print(ufDetails)

			json_object = json.loads(ufDetails)
			ufDetailsPretty = json.dumps(json_object, indent = 1)

			outputFile.write(ufDetailsPretty + "\n")

	except Exception as e:
		print("Exception while calculating uf data for tenant: " + tenant['code'])
		print(e)

except Exception as e:
	print(e)
	print(sys.exc_info()[0]);
	print("FAILED");

finally:
	outputFile.close()

