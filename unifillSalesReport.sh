python3 unifillSalesReport.py

ls -1 /tmp/unifill-mtd-sales-report* 
reportFilename=`ls -1t /tmp/unifill-mtd-sales-report* | head -1`
echo "Report file: ${reportFilename}"

today_date=$(date +'%d-%b-%Y')

MAIL_RECIPIENTS="sourabh.shrivastava@unicommerce.com,ankur.pratik@unicommerce.com,ankit.jain03@unicommerce.com"

MAIL_SUBJECT="Unifill Sales Report MTD | ${today_date}"
MAIL_CONTENT="Please find the attachment"

echo ${MAIL_CONTENT} | mutt -s "${MAIL_SUBJECT}" -a "${reportFilename}" -- "${MAIL_RECIPIENTS}"
