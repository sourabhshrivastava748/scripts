#!/usr/bin/python
import sys, datetime, pytz, re
import UniwareDbUtility 
import traceback 


def getSummary(inventorySyncData, tenantCode, date):
	summary = ""
	for data in inventorySyncData:
		summary += (
			tenantCode + "," +
			str(data["requestIdentifier"]) + "," +
			str(data["totalMarkDirtyTimeInSeconds"]) + "," +
			str(data["totalChannelSyncTimeInSeconds"]) + "," +
			str(data["totalTimeInSeconds"]) + "," +
			str(data["totalCit"]) + "," +
			str(data["markDirtyTimePerCit"]) + "," +
			str(data["channelSyncTimePerCit"]) + "," +
			date + "\n")

	return summary


# 										-- Main --
try:
	colName = "channelInventoryUpdate_O2"

	midnightDateTime_today = datetime.datetime.today().replace(hour = 0, minute = 0, second = 0, microsecond = 0)
	midnightDateTime_yesterday = midnightDateTime_today - datetime.timedelta(days = 1)

	utcMidnightDateTime_today = midnightDateTime_today.astimezone(pytz.UTC)
	utcMidnightDateTime_yesterday = midnightDateTime_yesterday.astimezone(pytz.UTC)

	reportDate = datetime.date.today() - datetime.timedelta(days = 1)
	reportDateStr = reportDate.strftime("%d-%m-%Y")

	print("utcMidnightDateTime_today: " + str(utcMidnightDateTime_today))
	print("utcMidnightDateTime_yesterday: " + str(utcMidnightDateTime_yesterday))
	print("reportDate: " + str(reportDate))

	# Create output file
	outputFileName = "/tmp/inventory-sync-timeline-" + reportDateStr + ".csv"
	outputFile = open(outputFileName, "w")
	outputFile.write("Tenant,RequestIdentifier,TotalMarkDirtyTimeInSeconds,TotalChannelSyncTimeInSeconds,TotalTimeInSeconds,TotalCit,MarkDirtyTimePerCit,ChannelSyncTimePerCit,Date\n")

	tenantList = ["helioslifestyle"]

	# For all tenants
	for tenant in tenantList:
		try:
			# Get mongodbUri of tenant 			
			mongoUri = []
			mongoUri = UniwareDbUtility.getTenantSpecificMongoUri(tenant)

			if (len(mongoUri) == 2):
				# Create mongo client
				myclient = UniwareDbUtility.getClient(mongoUri[0], mongoUri[1])
				mydb = myclient[tenant]
				mycol = mydb[colName]

				# Get inventory sync data
				aggregationSteps = [
				  {
				    "$match": {
				      "created": {
				        "$gte": utcMidnightDateTime_yesterday,
				        "$lte": utcMidnightDateTime_today
				      },
				      "itisUnacknowledgedTime": { "$exists": "true" },
				      "calculatedInventory": {
				        "$lt": 5
				      }
				    }
				  },
				  {
				    "$group": {
				      "_id": "$requestIdentifier",
				      "totalMarkDirtyTimeInSeconds": {
				        "$sum": {
				          "$divide": [
				            { "$subtract": ["$citMarkDirtyTime", "$itisUnacknowledgedTime"] },
				            1000
				          ]
				        }
				      },
				      "totalChannelSyncTimeInSeconds": {
				        "$sum": {
				          "$divide": [
				            { "$subtract": ["$created", "$citMarkDirtyTime"] },
				            1000
				          ]
				        }
				      },
				      "totalTimeInSeconds": {
				        "$sum": {
				          "$divide": [
				            { "$subtract": ["$created", "$itisUnacknowledgedTime"] },
				            1000
				          ]
				        }
				      },
				      "totalCit": { "$sum": 1 }
				    }
				  },
				  {
				    "$project": {
				      "requestIdentifier": "$_id",
				      "totalMarkDirtyTimeInSeconds": "$totalMarkDirtyTimeInSeconds",
				      "totalChannelSyncTimeInSeconds": "$totalChannelSyncTimeInSeconds",
				      "totalTimeInSeconds": "$totalTimeInSeconds",
				      "totalCit": "$totalCit",
				      "markDirtyTimePerCit": {
				        "$divide": ["$totalMarkDirtyTimeInSeconds", "$totalCit"]
				      },
				      "channelSyncTimePerCit": {
				        "$divide": ["$totalChannelSyncTimeInSeconds", "$totalCit"]
				      }
				    }
				  }
				]

				inventorySyncData = list(mycol.aggregate(aggregationSteps))

				# print("Inventory sync data: ")
				# print(inventorySyncData)		

				# Get Summary
				summary = getSummary(inventorySyncData, tenant, str(reportDateStr))
				# print(summary)
				outputFile.write(summary + "\n")

		except Exception as e:
			print("Exception while calculating uf data for tenant: " + tenant['code'])
			print(e)

except Exception as e:
	print(e)
	print(sys.exc_info()[0]);
	traceback.print_exc()
	print("FAILED");

finally:
	outputFile.close()


