#!/usr/bin/python
import sys, datetime, pytz, re
from pymongo import MongoClient


###
# piiAuditor
# 	- tenantCode
# 	- userName
# 	- actualUsername
# 	- ipAddress
# 	- exportId
# 	- exportJobTypeName
# 	- url
# 	- completionTime
###

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


def getDetails(piiAuditorData):

	details=""
	
	if (len(piiAuditorData)>0):
		for theDetail in piiAuditorData:
			details = details + (theDetail["tenantCode"] + "," 
				+ theDetail["userName"] +"," 
				+ theDetail["actualUsername"] + "," 
				# + theDetail["ipAddress"] +","
				+ theDetail["exportId"] + ","
				+ theDetail["exportJobTypeName"] + ","
				+ theDetail["url"] + ","
				+ str(theDetail["completionTime"]) + "\n")

	return details;


def getPrimaryClient(uri1):
	try:
	    c = MongoClient(uri1, 27017);
	    db= c['uniwareConfig'];
	    db.test.insert_one({});
	    print(str(uri1))
	except:
	    c = None

	return c


#			--- Main ----

colName = "piiAuditor"
tenantSpecificMongoHosts = [
	'mongo2.ril-in.unicommerce.infra',
	'mongo1.ril-in.unicommerce.infra',
	'mongo1.myntra-in.unicommerce.infra',
	'mongo2.hvc-in.unicommerce.infra',
	'mongo1.c6-in.unicommerce.infra',
	'mongo2.e1-in.unicommerce.infra',
	'mongo2.int-c1.unicommerce.infra',
	'mongo1.hvc-in.unicommerce.infra',
	'mongo1.e1-in.unicommerce.infra',
	'mongo1.e2-in.unicommerce.infra',
	'mongo4.c2-in.unicommerce.infra',
	'mongo2.e1-in.unicommerce.infra',
	'mongo3.c2-in.unicommerce.infra',
	'mongo6.c1-in.unicommerce.infra',
	'mongo1.ecloud1-in.unicommerce.infra',
	'mongo2.e2-in.unicommerce.infra',
	'mongo5.c1-in.unicommerce.infra',
	'mongo2.c6-in.unicommerce.infra',
	'mongo1.int-c1.unicommerce.infra',
	'mongo2.c3-in.unicommerce.infra',
	'mongo1.c4-in.unicommerce.infra',
	'mongo1.int-c2.unicommerce.infra',
	'mongo2.c4-in.unicommerce.infra',
	'mongo2.c5-in.unicommerce.infra',
	'mongo1.c3-in.unicommerce.infra',
	'mongo1.c5-in.unicommerce.infra',
	'mongo2.ecloud1-in.unicommerce.infra'
 ]


try:
	queryDate = datetime.datetime(2024, 9, 1, 0, 0, 0)

	current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
	outputFileName = f"/tmp/pii-auditor-details-{current_time}.csv"
	print("outputFileName" + outputFileName)

	outputFile = open(outputFileName, "w")
	outputFile.write("tenantCode, userName, actualUsername, exportId, exportJobTypeName, url, completionTime\n")

	# mongoUri = ["mongo1.e1-in.unicommerce.infra", "mongo2.e1-in.unicommerce.infra"]
	# myclient = getClient(mongoUri[0], mongoUri[1])


	for mongoHost in tenantSpecificMongoHosts:
		print("\nmongoHost: " + str(mongoHost))
		myclient = getPrimaryClient(mongoHost)

		if (myclient is not None):
			database_names = myclient.list_database_names()
			for db_name in database_names:
				print("db_name: " + str(db_name))

				if (db_name == "unistage"):
					continue

				mydb = myclient[db_name]
				mycol = mydb[colName]

				query = {
					"completionTime" : { 
						"$gte" : queryDate
					},
					"userName": { 
				        "$regex" : "unicommerce.com$", 
				        "$options" : "i"  
				    }
				}

				projection = {
					"tenantCode":1,
					"userName":1,
					"actualUsername":1,
					"exportId":1,
					"exportJobTypeName":1,
					"url":1,	
					"completionTime":1
				}

				piiAuditorData = list(mycol.find(query, projection))
				print("Total data: " + str(len(piiAuditorData)))

				if (len(piiAuditorData) > 0):
					details = getDetails(piiAuditorData)
					# print("------------")
					# print(details)
					# print("------------")

					outputFile.write(details + "\n")
		print("------------")

except Exception as e:
		print("Exception while getting piiAuditor data: ")
		print(e)
		print(traceback.format_exc())

finally:
	outputFile.close()










