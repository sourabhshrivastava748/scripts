#!/bin/bash
# Analyse UC Logs

set -eo pipefail

# Input
# tenantCode="earthrhythm"
# logDate="06-04-2023"
# key="EART473648"

# ==================================================================================

function show_help() {
	echo -e "\t\033[0;36m Usage: \033[0m"
	echo -e "\t\t \033[0;33m analyseLogs --tenantCode <Tenant-Code> --logDate <Date in DD-MM-YYYY> --saleOrderCode <Sale-Order-Code> \033[0m"
	echo -e "\t\t \033[0;33m analyseLogs --tenantCode <Tenant-Code> --logDate <Date in DD-MM-YYYY> --shipmentCode <Shipment-Code> \033[0m"
	echo
   	exit
}

# ==================================================================================

function set_args() {
  while [ "$1" != "" ]; do
    case $1 in
		"--tenantCode")
	        shift
	        tenantCode=$1
        ;;
      	"--logDate")
			shift
	        logDate=$1
        ;;
      	"--saleOrderCode")
	        shift
	        saleOrderCode=$1
        ;;
      	"--shipmentCode")
			shift
	        shipmentCode=$1
        ;;
        "--help")
			show_help
        ;;
    esac
    shift
  done
}


function get_logs() {
	getServerLogs -t "${tenantCode}" -d "${logDate}" "app,task,app3"
	
	appLogFileName="/applogs/${tenantCode}.${logDate:6}-${logDate:3:2}-${logDate::2}"
	taskLogFileName="/applogs/tasklog/${tenantCode}.${logDate:6}-${logDate:3:2}-${logDate::2}"
	app3LogFileName="/applogs/app3log/${tenantCode}.${logDate:6}-${logDate:3:2}-${logDate::2}"
	logFileName=""
}


function get_request_identifier() {
	if [[ -n ${appLogFileName} ]]; then
		logFileName=${appLogFileName}
		requestIdentifier=$(zgrep "${key}" ${logFileName}* | grep "${flowString}" | grep -oP '(?<=\[).*?(?=\])' | head -1)
		if [[ -n ${requestIdentifier} ]]; then
			return
		fi
	fi

	if [[ -n ${taskLogFileName} ]]; then
		logFileName=${taskLogFileName}
		requestIdentifier=$(zgrep "${key}" ${logFileName}* | grep "${flowString}" | grep -oP '(?<=\[).*?(?=\])' | head -1)
		if [[ -n ${requestIdentifier} ]]; then
			return
		fi
	fi

	if [[ -n ${app3LogFileName} ]]; then
		logFileName=${app3LogFileName}
		requestIdentifier=$(zgrep "${key}" ${logFileName}* | grep "${flowString}" | grep -oP '(?<=\[).*?(?=\])' | head -1)
		if [[ -n ${requestIdentifier} ]]; then
			return
		fi
	fi

}


function print_logs() {
	echo ""; echo "";
	echo -e "\t\033[0;33m ============ \033[0m"
	echo -e "\t\033[0;33m Tenant: $tenantCode \033[0m"
	echo -e "\t\033[0;33m Flow: $flow \033[0m"
	echo -e "\t\033[0;33m Key: $key \033[0m"
	echo -e "\t\033[0;33m Date: $logDate \033[0m"
	echo -e "\t\033[0;33m Log file: ${logFileName} \033[0m"

	get_request_identifier

	echo -e "\t\033[0;33m Request Identifier: $requestIdentifier \033[0m"
	echo -e "\t\033[0;33m ============ \033[0m"
	echo ""; echo "";

	if [[ -n ${requestIdentifier} ]]; then
		# match after colon (:) and remove everything between brackets []
		zgrep "${requestIdentifier}" ${logFileName}* | grep -oP '(?<=\:).*' | sed 's/\[[^P]* - /- /g' | grep --color -E "${key}|$"
	fi

	echo "";	
}



# ==================================== Input validation ====================================

function validate_input() {
		if [ -z "$tenantCode" ] || [ -z "$logDate" ]; then
			echo -e "\t \033[5;31m Invalid Input \033[0m"
			echo -e "\t \033[0;36m tenantCode or logDate cannot be empty \033[0m"
	    echo -e "\t \033[0;36m Use 'analyseLogs --help' for help \033[0m"
	    echo
	    exit
    fi
}


# ========================================= main ==========================================

# Set arguments
set_args $*

# Validate input
validate_input

# Get server logs
get_logs

# Analyse logs
clear
echo -e "\t \033[0;32m ================================================== \033[0m"
echo -e "\t \033[0;32m                   Analyse Logs                     \033[0m"
echo -e "\t \033[0;32m ================================================== \033[0m"

if [[ -n ${saleOrderCode} ]]; then
	key=${saleOrderCode}

	# Sale order import flow 
	flow="saleOrderImport"
	flowString="Creating sale order for request"
	print_logs

	# Facility allocation flow 
	flow="facilityAllocation"
	flowString="applying facility allocation rules, pending items for allocation :"
	print_logs

	# Sale order processing flow 
	flow="saleOrderProcessing"
	flowString="Processing sale order:"
	print_logs
fi

if [[ -n ${shipmentCode} ]]; then
	key=${shipmentCode}

	# Create invoice flow 
	flow="createInvoice"
	flowString="Creating Invoice for shipping package"
	print_logs

	# Allocate shipping provider and generate label
	flow="allocateShippingProvider"
	flowString="Allocating shipping provider and tracking number for shipping code"
	print_logs

	# Create manifest flow
	# flow="createManifest"
	# flowString=""
	# print_logs
fi

#====================================================================================

