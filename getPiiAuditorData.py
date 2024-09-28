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
				+ theDetail["ipAddress"] +","
				+ theDetail["exportId"] + ","
				+ theDetail["exportJobTypeName"] + ","
				+ theDetail["url"] + ","
				+ str(theDetail["completionTime"]) + "\n")

	return details;


#			--- Main ----

try:
	colName = "piiAuditor"
	tenantCode = "pep"
	queryDate = datetime.datetime(2024, 9, 27, 0, 0, 0)

	outputFileName = "/tmp/pii-auditor-details-27-Sep.csv"
	outputFile = open(outputFileName, "w")
	outputFile.write("tenantCode, userName, actualUsername, ipAddress, exportId, exportJobTypeName, url, completionTime\n")

	mongoUri = ["mongo1.e1-in.unicommerce.infra", "mongo2.e1-in.unicommerce.infra"]
	myclient = getClient(mongoUri[0], mongoUri[1])
	mydb = myclient[tenantCode]
	mycol = mydb[colName]

	query = {
		"completionTime" : { 
			"$gte" : queryDate
		}
	}

	projection = {
		"tenantCode":1,
		"userName":1,
		"actualUsername":1,
		"ipAddress":1,
		"exportId":1,
		"exportJobTypeName":1,
		"url":1,
		"completionTime":1
	}

	piiAuditorData = list(mycol.find(query, projection))
	details = getDetails(piiAuditorData)
	print("------------")
	print(details)
	print("------------")

	outputFile.write(details + "\n")

except Exception as e:
		print("Exception while getting piiAuditor data: ")
		print(e)
		print(traceback.format_exc())

finally:
	outputFile.close()










