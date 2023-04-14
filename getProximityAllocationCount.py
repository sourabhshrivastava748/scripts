#!/usr/bin/python
import sys, datetime, pytz, re
from pymongo import MongoClient

def getClient():
	try:
	    c = MongoClient('mongo1.e1-in.unicommerce.infra', 27017);
	    db= c['uniwareConfig'];
	    db.test.insert_one({});
	except:
	    print("common changed")
	    c = MongoClient('mongo2.e1-in.unicommerce.infra', 27017);

	return c

# serverName = sys.argv[1]
# commonPrimary = getClient()
# mongodbUri = getTenantSpecificMongo(commonPrimary)

myclient = getClient()
# dbsList = myclient.list_database_names()
dbsList = ['tcns', 'curefit', 'pep', 'mamaearth', 'leayanglobal', 'bestseller']
# dbsList = ['tcns']
print("Database list: " + str(dbsList))

fileName = "/tmp/proximity-based-allocation-" + datetime.date.today().strftime("%d-%m-%Y") + ".csv"
f = open(fileName, "w")
f.write("Tenant,Allocation Count,Date\n")

colName = "methodActivityMeta"
utcMidnightDateTime = datetime.datetime.today().replace(hour = 0, minute = 0, second = 0, microsecond = 0).astimezone(pytz.UTC)
print("utcMidnightDateTime: " + str(utcMidnightDateTime))

search = "via Proximity"
search_expr = re.compile(f".*{search}.*", re.I)

for tenantCode in dbsList:
	if (tenantCode != "uniware"):
		mydb = myclient[tenantCode]
		mycol = mydb[colName]

		query = {
			"tenantCode" : tenantCode,
			"entityName" : "SALE_ORDER",
			"created" : { "$gte" : utcMidnightDateTime },
			"log": { "$regex" : search_expr }
		}

		allocationCount = mycol.count_documents(query)
		print(str(tenantCode) + "," + str(allocationCount) + "," + str(datetime.date.today().strftime("%d-%m-%Y")))
		f.write(str(tenantCode) + "," + str(allocationCount) + "," + str(datetime.date.today().strftime("%d-%m-%Y")) + "\n")

f.close()




# def getTenantSpecificMongo(commonPrimary):
# 	db = commonPrimary['uniwareConfig'];
# 	mycol = db["serverDetails"]
# 	print ("Getting details for " + sys.argv[1]);

# 	serverDetail = mycol.find_one({"name": sys.argv[1]});
# 	print ("Tenant specific mongo hosts " + serverDetail["tenantSpecificMongoHosts"][0]);



