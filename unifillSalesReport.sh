python3 unifillSalesReport.py

ls -1 /tmp/unifill-mtd-sales-report* 
reportFilename=`ls -1t /tmp/unifill-mtd-sales-report* | head -1`
echo "Report file: ${reportFilename}"

yesterday_date=$(date -d "yesterday 13:00" +'%d-%b-%Y')

MAIL_RECIPIENTS="sourabh.shrivastava@unicommerce.com,ankur.pratik@unicommerce.com,ankit.jain03@unicommerce.com"
# MAIL_RECIPIENTS="sourabh.shrivastava@unicommerce.com"

MAIL_SUBJECT="Unifill Sales Report MTD | ${yesterday_date}"
MAIL_CONTENT="Please find the attachment"

echo ${MAIL_CONTENT} | mutt -s "${MAIL_SUBJECT}" -a "${reportFilename}" -- "${MAIL_RECIPIENTS}"
