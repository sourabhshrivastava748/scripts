#!/bin/bash

# Exit script on failure of any command
set -e

if [ "$#" -eq 0 ]; then
    echo "Cron run"
    python3 unifillSalesReport.py
	python3 unifillSalesReport-DailyUsage.py
	python3 unifillSalesReport-countApiMtd.py
	python3 unifillSalesReport-countApiDailyUsage.py


	ls -1 /tmp/unifill-mtd-sales-report* 
	reportFilename=`ls -1t /tmp/unifill-mtd-sales-report* | head -1`
	echo "Report file: ${reportFilename}"
	cp ${reportFilename} ./

	ls -1 /tmp/unifill-sales-report-daily-usage* 
	reportFilename2=`ls -1t /tmp/unifill-sales-report-daily-usage* | head -1`
	echo "Report file 2: ${reportFilename2}"
	cp ${reportFilename2} ./

	ls -1 /tmp/unifill-count-api-mtd* 
	reportFilename3=`ls -1t /tmp/unifill-count-api-mtd* | head -1`
	echo "Report file: ${reportFilename3}"
	cp ${reportFilename3} ./

	ls -1 /tmp/unifill-count-api-daily-usage* 
	reportFilename4=`ls -1t /tmp/unifill-count-api-daily-usage* | head -1`
	echo "Report file 2: ${reportFilename4}"
	cp ${reportFilename4} ./

	ls -al
	python3 convertCsvToHtml.py > mail-content.html

	yesterday_date=$(date -d "yesterday 13:00" +'%d-%b-%Y')

	MAIL_RECIPIENTS="turbo@unicommerce.com,anurag.mittal@unicommerce.com,accounts@unicommerce.com,financeteam@unicommerce.com,pramod@unicommerce.com,prince.singhla@unicommerce.com,dharamveer.rathore@unicommerce.com,hariom.jaiswal@unicommerce.com,lalit.sharma@unicommerce.com,arpit.saxena@unicommerce.com,gunjan.marwaha@unicommerce.com"

	# MAIL_RECIPIENTS="sourabh.shrivastava@unicommerce.com"

	MAIL_SUBJECT="Unifill Sales Report MTD and Daily Usage | ${yesterday_date}"
	MAIL_CONTENT="Please find the attachment. Report prepared by alpha team."

	mutt -e "set content_type=text/html" -s "${MAIL_SUBJECT}" -a "${reportFilename}" -a "${reportFilename2}" -a "${reportFilename3}" -a "${reportFilename4}" -- "${MAIL_RECIPIENTS}" < mail-content.html

elif [ "$#" -eq 3 ]; then
    echo "Manual parameterized run with arguments: $#"
    python3 unifillSalesReport-Parameterized.py "$1" "$2" 

    reportFileString="unifill-sales-report_${1}_to_${2}.csv"
    ls -1 /tmp/${reportFileString}
    reportFilename=`ls -1t /tmp/${reportFileString} | head -1`
    echo "Report file: ${reportFilename}"

    MAIL_RECIPIENTS="$3"
    echo "MAIL_RECIPIENTS: ${MAIL_RECIPIENTS}"
    MAIL_SUBJECT="Unifill Sales Report | ${1} to ${2}"
	MAIL_CONTENT="Please find the attachment. Report prepared by alpha team."

	echo ${MAIL_CONTENT} | mutt -s "${MAIL_SUBJECT}" -a "${reportFilename}" -- "${MAIL_RECIPIENTS}"
else
    echo "Illegal number of arguments: $#"
fi 




