#!/usr/bin/python
import xml.etree.ElementTree
import MySQLdb
import pymongo
import sys
import os
import re

from pymongo import MongoClient
from datetime import datetime

result = 'SUCCESS';

print ("In Script");

global db
global dbMysql
master = 1;
common = 1;
isTenant = 1
global client
global c
global tenantMongo



tenantMongo = MongoClient('mongo1.e1-in.unicommerce.infra:27017', 27017);
c = MongoClient('common1.mongo.unicommerce.infra:27017', 27017);

serverName = "HealthKart"
sampleTenantCode = "hktouchstoneteleservices1"
sampleTenantDb = tenantMongo[sampleTenantCode];

queryFilter = {"code": "INVOICE_CUSTOM_TEMPLATE"}
doc = sampleTenantDb.samplePrintTemplate.find_one(queryFilter)
values = { "$set" : { "template": doc["template"] }}


db= c['uniwareConfig'];
serverDetails = db["serverDetails"];
print("Getting details for " + serverName);
server = serverDetails.find_one({"name": serverName});
dbMysql = MySQLdb.connect(server["db"], "developer", "DevelopeR@4#", "uniware");
cur = dbMysql.cursor();
cur.execute("SELECT t.code FROM tenant t where status_code = 'ACTIVE'");

totalCount = 0

for row in cur.fetchall():
    tenantCode = row[0];
    print("#####~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#####");
    print("Starting update for tenant: " + tenantCode);
    tenantDb = tenantMongo[tenantCode]
    tenantDb.samplePrintTemplate.update_one(queryFilter, values)
    print("Done for tenant: " + tenantCode);
    print("#####~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#####");
    print("")
    print("")
    totalCount = totalCount + 1

dbMysql.close();
print("Total count of tenant: " + str(totalCount))
print(result);



