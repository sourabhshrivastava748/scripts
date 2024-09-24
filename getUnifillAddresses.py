"""
    Input : input.csv - contains mobile numbers line separated
    Output : unifill-mobile-with-addresses.csv
        - contains csv of mobile along with top 5 address (max)
"""

import requests, datetime
import csv
import io
from time import sleep

inputFilename = "input.csv"

reportDate = datetime.date.today()
reportDateString = reportDate.strftime("%Y%m%d%H%M%S")
outputFileName = "/tmp/unifill-mobile-with-addresses_" + reportDateString  + ".csv"


outputFile = open(outputFileName, "w")
totalCount = 0;
totalMobileCount = 0;

try:
    outputFile.write("mobile,name,address_line1,address_line2,city,district,state,country,pin_code\n")
    
    with open(inputFilename) as file:
        for line in file:
            totalCount+=1
            unifillMobile = line.rstrip()
            # lineSplit = line.rstrip().split(",")
            # unifillMobile = lineSplit[0]
            # unifillHash = lineSplit[1]
            # print("unifillMobile: " + unifillMobile + ", unifillHash: " + unifillHash)
            print(str(totalCount) + ". unifillMobile: " + unifillMobile)

            url = "http://apiaddress.unicommerce.co.in/v1/addresses?mobile=" + unifillMobile
            headers = { "x-api-key" : "uc_dev-5tywMX2vfwltwWCfq9cb"}

            response = requests.get(url = url, headers = headers)
            response_json = response.json()

            sleep(0.05)

            if len(response_json["address_list"]) > 0:
                totalMobileCount+=1
                for address in response_json["address_list"][:5]:
                    # ostr = (
                    #     "\"" + unifillMobile + "\",\"" + unifillHash + "\"," + 
                    #     ','.join(f"\"{item}\"" for item in address.values())
                    # )

                    ostr = (
                        "\"" + unifillMobile + "\"," + ','.join(f"\"{item}\"" for item in address.values())
                    )

                    # print(ostr)
                    outputFile.write(ostr + "\n")

finally:
    outputFile.close()

        
print("\nTotal count : " + str(totalCount))
print("Total mobile where atleast one address is found : " + str(totalMobileCount))
print("Output file: " + outputFileName)


