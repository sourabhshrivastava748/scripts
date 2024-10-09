#!/usr/bin/python
import sys, datetime, pytz, re
from pymongo import MongoClient
from collections import defaultdict
import pandas as pd


###
# piiAuditor
# - ipAddress
# - actualUsername
# - tenantCode
# - exportJobTypeName
# - exportFilterList


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
		        theDetail.get("ipAddress", "") + "," 
		        + theDetail.get("actualUsername", "") + "," 
		        + theDetail.get("tenantCode", "") + "," 
		        + theDetail.get("exportJobTypeName", "") + "," 
		        + "\"" + theDetail.get("exportFilterList", "").replace("\\", "").replace("\"", "") + "\"" + "\n"
		    )

			details += row

	return details;



def find_multiple_tenants_combined(csv_file_path, output_csv_path):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file_path)

    # Clean df: Drop rows where ipAddress or actualUsername is NaN or empty
    df = df.dropna(subset=['ipAddress', 'actualUsername'])
    df = df[(df['ipAddress'].astype(bool)) & (df['actualUsername'].astype(bool))]

    # Group by ipAddress and aggregate unique tenantCodes and the list of tenantCodes
    ip_df = df.groupby('ipAddress').agg(
        tenantCode_count=('tenantCode', 'nunique'),
        tenantCodes_list=('tenantCode', lambda x: ', '.join(x.unique()))
    ).reset_index()

    # Filter for ipAddresses with more than one tenantCode
    ip_df = ip_df[ip_df['tenantCode_count'] > 1]

    # Group by actualUsername and aggregate unique tenantCodes and the list of tenantCodes
    user_df = df.groupby('actualUsername').agg(
        tenantCode_count=('tenantCode', 'nunique'),
        tenantCodes_list=('tenantCode', lambda x: ', '.join(x.unique()))
    ).reset_index()

    # Filter for actualUsernames with more than one tenantCode
    user_df = user_df[user_df['tenantCode_count'] > 1]

    # Combine the two DataFrames
    combined_df = pd.concat([ip_df.rename(columns={'ipAddress': 'identifier'}),
                             user_df.rename(columns={'actualUsername': 'identifier'})])

    print("Combined df")
    print(combined_df)

    # Save the combined DataFrame to a CSV file
    combined_df.to_csv(output_csv_path, index=False)

    print(f"CSV file with IP addresses and usernames having multiple tenant codes saved to {output_csv_path}")





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
outputFile.write("ipAddress,actualUsername,tenantCode,exportJobTypeName,exportFilterList\n")

# suspiciousUserOutputFile = open(suspiciousUserOfn, "w")
# suspiciousUserOutputFile.write("ip_username_with_multiple_tenants\n")



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
					"ipAddress":1,
					"actualUsername":1,
					"tenantCode":1,
					"exportJobTypeName": 1,
					"exportFilterList":1
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
	find_multiple_tenants_combined(outputFileName, suspiciousUserOfn)
	

except Exception as e:
	print("Exception while getting piiAuditor data: ")
	print(e)
	print(traceback.format_exc())






