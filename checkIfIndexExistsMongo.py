import pymongo, collections

mongodbUri = "mongodb://localhost:27017/"
dbName = "stgenterprise1"

colName = "channelInventoryUpdate_O2"
indexColumns = ['tenantCode', 'channelCode', 'channelProductId']
indexExists = False

myclient = pymongo.MongoClient(mongodbUri)
mydb = myclient[dbName]
mycol = mydb[colName]

indexes = mycol.index_information()

for name in indexes:
	index_keys = indexes[name]["key"]
	index_keys = [i[0] for i in index_keys]
	# print(index_keys)

	if (set(indexColumns) == set(index_keys)):
		indexExists = True
		print("Index exists for " + str(indexColumns) + " in collection " + str(colName) + " with name: " + str(name))
		break

if (not indexExists):
	print("Index does not exists for " + str(indexColumns) + " in collection " + str(colName))


