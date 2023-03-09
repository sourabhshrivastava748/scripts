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

# ============================== Helper functions ===================================

function get_system_config() {
	local tenantCode=$1
	local systemConfigName=$2
	local query="select * from system_configuration where name = '$systemConfigName' and tenant_id = (select id from tenant where code = '$tenantCode');"
	local query_result=`mysql -N -u$DB_USER -p$DB_PASSWORD -h$DB_HOST uniware -e "$query" | tr '\t' ','`
	
	echo ${query_result}
}

function get_tenant() {
	local tenantCode=$1
	local query="select * from tenant where code = '$tenantCode';"
	local query_result=`mysql -N -u$DB_USER -p$DB_PASSWORD -h$DB_HOST uniware -e "$query" | tr '\t' ','`
	
	echo ${query_result}
}

function get_base_tenant_code() {
	local baseTenantCode=${TENANT_PRODUCT_CODE}
	baseTenantCode="base$(echo "$baseTenantCode" | tr '[:upper:]' '[:lower:]')"

	if [[ "$SERVER_NAME" == "ECloud"* ]]; then
		suffix=${SERVER_NAME#"ECloud"}
	elif [[ "$SERVER_NAME" == "Cloud"* ]]; then
		suffix=${SERVER_NAME#"Cloud"}
	fi
	baseTenantCode+=$suffix

	echo ${baseTenantCode}
}

function validate_config_value() {
	if [[ -n ${SYSTEM_CONFIGURATION_VALUE} ]]; then
		local configType=$1
		if [[ ${configType} == "checkbox" ]]; then
			if [[ ${SYSTEM_CONFIGURATION_VALUE} == "true" || ${SYSTEM_CONFIGURATION_VALUE} == "false" ]]; then
				return
			else
				echo "Invalid config value. The config type is checkbox, hence the value can be either true or false"
				exit
			fi
		fi
	fi
}

function build_insert_query() {
	INSERT_QUERY="insert ignore into system_configuration select null,"

	if [[ ${BASE_TENANT_SYSTEM_CONFIG_ARRAY[2]} == "NULL" ]]; then
		echo "Tenant level config"
		INSERT_QUERY+="${TENANT_ID}-${SYSTEM_CONFIGURATION_NAME},null,"
	else
		echo "Facility level config"
	fi

	# tenant_id
	INSERT_QUERY+="${TENANT_ID},"

	# name
	INSERT_QUERY+="${BASE_TENANT_SYSTEM_CONFIG_ARRAY[4]},"

	# display_name
	INSERT_QUERY+="${BASE_TENANT_SYSTEM_CONFIG_ARRAY[5]},"

	# value
	if [[ -n ${SYSTEM_CONFIGURATION_VALUE} ]]; then
		INSERT_QUERY+="${SYSTEM_CONFIGURATION_VALUE},"
	else
		INSERT_QUERY+="${BASE_TENANT_SYSTEM_CONFIG_ARRAY[6]},"
	fi

	# type
	INSERT_QUERY+="${BASE_TENANT_SYSTEM_CONFIG_ARRAY[7]},"
	validate_config_value ${BASE_TENANT_SYSTEM_CONFIG_ARRAY[7]}

	# hidden
	INSERT_QUERY+="${BASE_TENANT_SYSTEM_CONFIG_ARRAY[8]},"

	# condition_expression
	if [[ -n ${CONDITION_EXPRESSION} ]]; then
		INSERT_QUERY+="${CONDITION_EXPRESSION},"
	else
		INSERT_QUERY+="${BASE_TENANT_SYSTEM_CONFIG_ARRAY[9]},"
	fi

	# access_resource_name
	INSERT_QUERY+="${BASE_TENANT_SYSTEM_CONFIG_ARRAY[10]},"
	# group_name
	INSERT_QUERY+="${BASE_TENANT_SYSTEM_CONFIG_ARRAY[11]},"
	# sequence
	INSERT_QUERY+="${BASE_TENANT_SYSTEM_CONFIG_ARRAY[12]},"
	# created
	INSERT_QUERY+="now(),"
	# updated
	INSERT_QUERY+="now();"
}



# ============================== Runner Script ===================================

eval $1
initialize_global_variables


TENANT=$(get_tenant "$TENANT_CODE")
if [[ -z $TENANT ]]; then
	echo "Invalid tenant code: ${tenantCode}"
	exit
fi
IFS=',' read -r -a tenant_array <<< "$TENANT"
TENANT_ID=${tenant_array[0]}
TENANT_PRODUCT_CODE=${tenant_array[4]}
echo "TENANT_ID: ${TENANT_ID}"
echo "TENANT_PRODUCT_CODE: ${TENANT_PRODUCT_CODE}"

# if [[ -n $(get_system_config "$TENANT_CODE" "$SYSTEM_CONFIGURATION_NAME") ]]; then
# 	echo "System config ${SYSTEM_CONFIGURATION_NAME} already exists for the tenant ${TENANT_CODE}"
# 	exit
# fi

BASE_TENANT_CODE=$(get_base_tenant_code)
echo "BASE_TENANT_CODE : ${BASE_TENANT_CODE}"

tc="aei"
q="select * from tenant where code = '$tc';"
qr=`mysql -N -u$DB_USER -p$DB_PASSWORD -h$DB_HOST uniware -e "$query" | tr '\t' ','`

echo ${qr}

BASE_TENANT_SYSTEM_CONFIG=$(get_system_config "$BASE_TENANT_CODE" "$SYSTEM_CONFIGURATION_NAME")
if [[ -z $BASE_TENANT_SYSTEM_CONFIG ]]; then
	echo "System config ${SYSTEM_CONFIGURATION_NAME} does not exists for the base tenant ${BASE_TENANT_CODE} . Invalid system configuration"
	exit
fi

IFS=',' read -r -a BASE_TENANT_SYSTEM_CONFIG_ARRAY <<< "$BASE_TENANT_SYSTEM_CONFIG"
echo 


build_insert_query


echo "-----------------------"
echo $INSERT_QUERY
echo "-----------------------"

echo "Adding system configuration.. "







