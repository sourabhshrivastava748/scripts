#!/bin/bash

function initialize_global_variables() {
	TENANT_CODE=${inputData[Tenant_Code]}
	SYSTEM_CONFIGURATION_NAME=${inputData[System_Configuration_Name]}
	SYSTEM_CONFIGURATION_VALUE=${inputData[System_Configuration_Value]}
	CONDITION_EXPRESSION=${inputData[Condition_Expression]}

	# Get build triggered by
	BUILD_TRIGGER_BY=$(curl -k --silent ${BUILD_URL}/api/xml | tr '<' '\n' | egrep '^userId>|^userName>' | sed 's/.*>//g' | sed -e '1s/$/ \//g' | tr '\n' ' ')
	echo BUILD_TRIGGER_BY: $BUILD_TRIGGER_BY

	# Get mongo host
	declare -A ASSOCIATIVE_ARRAY
	ASSOCIATIVE_ARRAY["ACTION"]=MONGO_HOST
	source /var/lib/jenkins/scripts/helper.sh "$(declare -p ASSOCIATIVE_ARRAY)"
	MONGO_HOST=${ASSOCIATIVE_ARRAY[MONGO_HOST]}
	echo MONGO_HOST: $MONGO_HOST

	# Get server name
	ASSOCIATIVE_ARRAY["ACTION"]=SERVER_DETAILS
	ASSOCIATIVE_ARRAY["TENANT_CODE"]="$TENANT_CODE"
	source /var/lib/jenkins/scripts/helper.sh "$(declare -p ASSOCIATIVE_ARRAY)"
	if [ $? -ne 0 ]
	then
	        echo "error: invalid tenant code"
	        exit 1
	fi
	SERVER_NAME=${ASSOCIATIVE_ARRAY[SERVER_NAME]}
	echo SERVER_NAME : $SERVER_NAME

	# Get tenant mongo host
	TENANT_MONGO_HOST=${ASSOCIATIVE_ARRAY[TENANT_MONGO_HOST]}
	echo TENANT_MONGO_HOST: $TENANT_MONGO_HOST

	# DB Credentials
	DB_USER="backupuser"
	DB_PASSWORD="backupUser@5#"
	DB_NAME="uniware"
	DB_HOST=`mongo --host $MONGO_HOST uniwareConfig --eval  "db.getMongo().setSecondaryOk();db.serverDetails.find({serverName:'$SERVER_NAME'}).forEach(function(doc){print(doc.db);})" | grep -v -e "MongoDB shell" | tail -1`
	echo DB_HOST : $DB_HOST

	echo
}

function findColumnValueByIndex() {
	l=0
	RES=-1
	for it in $1
	do
		if [[ $l -eq $2 ]]
		then
			let RES=$it
			break;
		fi
		let l++
	done
	echo "$RES"
}

# Check if config exists for the tenant
function system_config_exists() {
	local tenantCode=$1
	local systemConfigName=$2

	local query="select * from system_configuration where name = '$systemConfigName' and tenant_id = (select id from tenant where code = '$tenantCode');"
	local query_result=`mysql -N -u$DB_USER -p$DB_PASSWORD -h$DB_HOST uniware -e "$query" | tr '\t' ','`
	echo "query_result: ${query_result}"

	IFS=',' read -r -a query_result_array <<< "$query_result"
	echo "Elements after splitting: "
	for element in "${query_result_array[@]}"
	do
	    echo "$element"
	done

	local sys_config_id="${array[0]}"
	echo  "sys_config_id: ${sys_config_id}"

	if [[ $sys_config_id == "-1" ]]; then
		echo "No"
	else
		echo "Yes"
	fi
}

# Find out product_code of tenant

# Based on product code and server name, get base tenant code

# Get system config from base tenant

# If config exist 
	# build system config query
	# insert system config 
# Else
	# exit with message "Config doesn't exists for base tenant: "

# Success message

# Mail trigger







# ====================== Main Script ============================

eval $1
initialize_global_variables

if [[ $(system_config_exists "$TENANT_CODE" "$SYSTEM_CONFIGURATION_NAME") == "Yes" ]]; then
	echo "System config ${SYSTEM_CONFIGURATION_NAME} already exists for the tenant ${TENANT_CODE}"
	exit
fi 

echo "Adding system configuration.. "











