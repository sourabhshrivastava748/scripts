
python3 unifillSalesReport.py
python3 unifillSalesReport-DailyUsage.py

ls -1 /tmp/unifill-mtd-sales-report* 
reportFilename=`ls -1t /tmp/unifill-mtd-sales-report* | head -1`
echo "Report file: ${reportFilename}"

ls -1 /tmp/unifill-sales-report-daily-usage* 
reportFilename2=`ls -1t /tmp/unifill-sales-report-daily-usage* | head -1`
echo "Report file 2: ${reportFilename2}"

yesterday_date=$(date -d "yesterday 13:00" +'%d-%b-%Y')

MAIL_RECIPIENTS="sourabh.shrivastava@unicommerce.com,ankur.pratik@unicommerce.com,ankit.jain03@unicommerce.com,bhupi@unicommerce.com,anurag.mittal@unicommerce.com,accounts@unicommerce.com,financeteam@unicommerce.com,abhinav.gupta@unicommerce.com,kapil@unicommerce.com,lalit.sharma@unicommerce.com,pramod@unicommerce.com"

# MAIL_RECIPIENTS="sourabh.shrivastava@unicommerce.com"

MAIL_SUBJECT="Unifill Sales Report MTD and Daily Usage | ${yesterday_date}"
MAIL_CONTENT="Please find the attachment. Report prepared by alpha team."

echo ${MAIL_CONTENT} | mutt -s "${MAIL_SUBJECT}" -a "${reportFilename}" -a "${reportFilename2}" -- "${MAIL_RECIPIENTS}"
