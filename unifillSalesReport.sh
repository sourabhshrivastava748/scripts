#!/bin/bash

if [ "$#" -eq 0 ]; then
    echo "Cron run"
    python3 unifillSalesReport.py
	python3 unifillSalesReport-DailyUsage.py

	ls -1 /tmp/unifill-mtd-sales-report* 
	reportFilename=`ls -1t /tmp/unifill-mtd-sales-report* | head -1`
	echo "Report file: ${reportFilename}"

	ls -1 /tmp/unifill-sales-report-daily-usage* 
	reportFilename2=`ls -1t /tmp/unifill-sales-report-daily-usage* | head -1`
	echo "Report file 2: ${reportFilename2}"

	yesterday_date=$(date -d "yesterday 13:00" +'%d-%b-%Y')

	MAIL_RECIPIENTS="turbo@unicommerce.com,anurag.mittal@unicommerce.com,accounts@unicommerce.com,financeteam@unicommerce.com,kapil@unicommerce.com,pramod@unicommerce.com"

	# MAIL_RECIPIENTS="sourabh.shrivastava@unicommerce.com"

	MAIL_SUBJECT="Unifill Sales Report MTD and Daily Usage | ${yesterday_date}"
	MAIL_CONTENT="Please find the attachment. Report prepared by alpha team."

	echo ${MAIL_CONTENT} | mutt -s "${MAIL_SUBJECT}" -a "${reportFilename}" -a "${reportFilename2}" -- "${MAIL_RECIPIENTS}"

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




