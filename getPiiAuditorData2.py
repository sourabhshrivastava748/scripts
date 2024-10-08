#!/usr/bin/python
import sys, datetime, pytz, re
from pymongo import MongoClient
from collections import defaultdict
import pandas as pd


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
			row = (
		        theDetail.get("tenantCode", "") + "," 
		        + theDetail.get("userName", "") + "," 
		        + theDetail.get("actualUsername", "") + "," 
		        + theDetail.get("ipAddress", "") + "," 
		        + theDetail.get("exportId", "") + "," 
		        + theDetail.get("exportJobTypeName", "") + "," 
		        + theDetail.get("url", "") + "," 
		        + str(theDetail.get("completionTime", "")) + "\n"
		    )

			details += row

	return details;


# def find_ip_with_multiple_tenants(piiAuditorData):
#     # Dictionary to store ipAddress -> set of tenantCodes
#     ip_to_tenant_codes = defaultdict(set)

#     # Populate the dictionary
#     for theDetail in piiAuditorData:
#         ip = theDetail.get("ipAddress", "")
#         tenant_code = theDetail.get("tenantCode", "")
        
#         if ip and tenant_code:  # Ensure both ipAddress and tenantCode are not empty
#             ip_to_tenant_codes[ip].add(tenant_code)

#     # Find ipAddresses with more than one distinct tenantCode
#     ip_addresses = [ip for ip, tenant_codes in ip_to_tenant_codes.items() if len(tenant_codes) > 1]

#     return "\n".join(ip_addresses)


# def find_user_with_multiple_tenants(piiAuditorData):
#     # Dictionary to store actualUsername -> set of tenantCodes
#     user_to_tenant_codes = defaultdict(set)

#     # Populate the dictionary
#     for theDetail in piiAuditorData:
#         user = theDetail.get("actualUsername", "")
#         tenant_code = theDetail.get("tenantCode", "")
        
#         if user and tenant_code:  # Ensure both actualUsername and tenantCode are not empty
#             user_to_tenant_codes[user].add(tenant_code)

#     # Find actualUsernames with more than one distinct tenantCode
#     usernames = [user for user, tenant_codes in user_to_tenant_codes.items() if len(tenant_codes) > 1]

#     # Join the usernames with newlines
#     return "\n".join(usernames)



def find_multiple_tenants_combined(csv_file_path):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file_path)
    print(df)
    
    # Group by ipAddress and aggregate unique tenantCodes
    ip_groups = df.groupby('ipAddress')['tenantCode'].nunique()
    ip_addresses_with_multiple_tenants = ip_groups[ip_groups > 1].index.tolist()
    
    # Group by userName and aggregate unique tenantCodes
    user_groups = df.groupby('userName')['tenantCode'].nunique()
    usernames_with_multiple_tenants = user_groups[user_groups > 1].index.tolist()
    
    # Combine the two lists
    combined_list = ip_addresses_with_multiple_tenants + usernames_with_multiple_tenants

    combined_string = "\n".join(combined_list)
    
    return combined_string




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
# tenantSpecificMongoHosts = [
# 	'mongo2.ril-in.unicommerce.infra',
# 	'mongo1.ril-in.unicommerce.infra',
# 	'mongo1.myntra-in.unicommerce.infra',
# 	'mongo2.hvc-in.unicommerce.infra',
# 	'mongo1.c6-in.unicommerce.infra',
# 	'mongo2.e1-in.unicommerce.infra',
# 	'mongo2.int-c1.unicommerce.infra',
# 	'mongo1.hvc-in.unicommerce.infra',
# 	'mongo1.e1-in.unicommerce.infra',
# 	'mongo1.e2-in.unicommerce.infra',
# 	'mongo4.c2-in.unicommerce.infra',
# 	'mongo2.e1-in.unicommerce.infra',
# 	'mongo3.c2-in.unicommerce.infra',
# 	'mongo6.c1-in.unicommerce.infra',
# 	'mongo1.ecloud1-in.unicommerce.infra',
# 	'mongo2.e2-in.unicommerce.infra',
# 	'mongo5.c1-in.unicommerce.infra',
# 	'mongo2.c6-in.unicommerce.infra',
# 	'mongo1.int-c1.unicommerce.infra',
# 	'mongo2.c3-in.unicommerce.infra',
# 	'mongo1.c4-in.unicommerce.infra',
# 	'mongo1.int-c2.unicommerce.infra',
# 	'mongo2.c4-in.unicommerce.infra',
# 	'mongo2.c5-in.unicommerce.infra',
# 	'mongo1.c3-in.unicommerce.infra',
# 	'mongo1.c5-in.unicommerce.infra',
# 	'mongo2.ecloud1-in.unicommerce.infra'
#  ]

 tenantSpecificMongoHosts = [
	'mongo1.e1-in.unicommerce.infra',
	'mongo1.e2-in.unicommerce.infra'
 ]


fromDate = datetime.date.today() - datetime.timedelta(days = 7)
fromDateString = fromDate.strftime("%d-%m-%Y")
print("fromDateString: " + fromDateString)
fromDateTime = datetime.datetime.combine(fromDate, datetime.datetime.min.time())

toDate = datetime.date.today()
toDateString = toDate.strftime("%d-%m-%Y")
print("toDateString: " + toDateString)


outputFileName = f"/tmp/pii-auditor-details_{fromDateString}_to_{toDateString}.csv"
print("outputFileName" + outputFileName)

suspiciousUserOfn = f"/tmp/suspicious-users_{fromDateString}_to_{toDateString}.csv"
print("suspiciousUserOfn" + suspiciousUserOfn)


outputFile = open(outputFileName, "w")
outputFile.write("tenantCode, userName, actualUsername, ipAddress, exportId, exportJobTypeName, url, completionTime\n")

suspiciousUserOutputFile = open(suspiciousUserOfn, "w")
suspiciousUserOutputFile.write("ip_username_with_multiple_tenants\n")



try:
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
						"$gte" : fromDateTime
					}
				}

				projection = {
					"tenantCode":1,
					"userName":1,
					"actualUsername":1,
					"ipAddress": 1,
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



try:
	suspiciousUsers = find_multiple_tenants_combined(outputFileName)
	print("------------")
	print(suspiciousUsers)
	print("------------")
	if not suspiciousUsers.strip():
		suspiciousUserOutputFile.write(suspiciousUsers+ "\n")

except Exception as e:
	print("Exception while getting piiAuditor data: ")
	print(e)
	print(traceback.format_exc())






