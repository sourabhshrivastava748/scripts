import pymongo, sys
from datetime import date

mongodbUri = sys.argv[1]
myclient = pymongo.MongoClient(mongodbUri)

dbsList = myclient.list_database_names()
print("Database list: " + str(dbsList))

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
		print(str(tenantCode) + "," + str(date.today()) + "," + str(allocationCount))






