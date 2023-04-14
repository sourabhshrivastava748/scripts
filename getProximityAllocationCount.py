import pymongo, sys
from datetime import date

# serverName = sys.argv[1]
# commonPrimary = getClient()
# mongodbUri = getTenantSpecificMongo(commonPrimary)

myclient = getClient()
# dbsList = myclient.list_database_names()
dbsList = ['tcns', 'curefit', 'pep', 'mamaearth', 'leayanglobal', 'bestseller']
print("Database(tenant) list: " + str(dbsList))

fileName = "/tmp/proximity-based-allocation-" + date.today().strftime("%d-%m-%Y") + ".csv"
f = open(fileName, "w")
f.write("Tenant,Allocation Count,Date\n")

colName = "methodActivityMeta"

for tenantCode in dbsList:
	if (tenantCode != "uniware"):
		mydb = myclient[tenantCode]
		mycol = mydb[colName]
		query = {
			"tenantCode" : tenantCode,
			"entityName" : "SALE_ORDER",
			"created" : { "$gte" : "new Date((new Date()).getFullYear(), (new Date()).getMonth(), (new Date()).getDate(), 0, 0, 0)" },
			"log": "/via Proximity/"
		}

		allocationCount = mycol.count_documents(query)
		print(str(tenantCode) + "," + str(allocationCount) + "," + str(date.today().strftime("%d-%m-%Y")))
		f.write(str(tenantCode) + "," + str(allocationCount) + "," + str(date.today().strftime("%d-%m-%Y")) + "\n")

f.close()

def getClient():
	try:
	    c = MongoClient('mongo1.e1-in.unicommerce.infra', 27017);
	    db= c['uniwareConfig'];
	    db.test.insert_one({});
	except:
	    print("Server not available common1.mongo.unicommerce.infra");
	    common = 0;

	if common == 0:
	    print("common changed")
	    c = MongoClient('mongo2.e1-in.unicommerce.infra', 27017);
    return c


# def getTenantSpecificMongo(commonPrimary):
# 	db = commonPrimary['uniwareConfig'];
# 	mycol = db["serverDetails"]
# 	print ("Getting details for " + sys.argv[1]);

# 	serverDetail = mycol.find_one({"name": sys.argv[1]});
# 	print ("Tenant specific mongo hosts " + serverDetail["tenantSpecificMongoHosts"][0]);



