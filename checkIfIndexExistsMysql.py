import mysql.connector
  
dataBase = mysql.connector.connect(
  host ="db-slave.ecloud1-in.unicommerce.infra",
  user ="developer",
  passwd ="DevelopeR@4#",
  database = "uniware"
)

tableName = "shipping_package"
indexColumns = ['tenant_id', 'channel_id', 'created']
query = "show index from " + str(tableName)
indexExists = False

cursorObject = dataBase.cursor()
cursorObject.execute(query)
   
indexList = cursorObject.fetchall()
indexDict = dict()

   
# for index in indexList:
#     # print("Key_name: " + str(index[2]) + " Column_name : " + str(index[4]))
#     if index[2] not in indexDict.keys():
#         indexDict[index[2]] = set()

#     indexDict[index[2]].add(index[4])


# for key in indexDict:
#     print(str(key) + " : " + str(indexDict[key]))
#     if (set(indexColumns) == set(indexDict[key])):
#         indexExists = True
#         print("Index exists for " + str(indexColumns) + " in table " + str(tableName) + " with name " + str(key))
#         break

# if (not indexExists):
#     print("Index does not exists for " + str(indexColumns) + " in table " + str(tableName))

# -------------- test --------------

tableNameList = ["shipping_package", "shipping_manifest_item", "shipping_manifest", "inflow_receipt_item", "item_type", "picklist_item", "picklist", "invoice"]

for tableName in tableNameList:
    print("------ " + str(tableName) + "--------")
    query = "show index from " + str(tableName)

    cursorObject = dataBase.cursor()
    cursorObject.execute(query)
       
    indexList = cursorObject.fetchall()
    indexDict = dict()

    for index in indexList:
        # print("Key_name: " + str(index[2]) + " Column_name : " + str(index[4]))
        if index[2] not in indexDict.keys():
            indexDict[index[2]] = set()

        indexDict[index[2]].add(index[4])

    for key in indexDict:
        print(str(key) + " : " + str(indexDict[key]))

    print("")

# -------------- --------------

  
# Disconnecting from the server
dataBase.close()

