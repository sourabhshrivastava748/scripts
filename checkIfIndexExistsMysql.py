import mysql.connector
  
dataBase = mysql.connector.connect(
  host ="localhost",
  user ="root",
  passwd ="uniware",
  database = "uniware"
)

tableName = "sale_order"
indexColumns = ['tenant_id', 'channel_id', 'created']
query = "show index from " + str(tableName)
indexExists = False

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
    # print(str(key) + " : " + str(indexDict[key]))
    if (set(indexColumns) == set(indexDict[key])):
        indexExists = True
        print("Index exists for " + str(indexColumns) + " in table " + str(tableName) + " with name " + str(key))
        break

if (not indexExists):
    print("Index does not exists for " + str(indexColumns) + " in table " + str(tableName))

  
# Disconnecting from the server
dataBase.close()

