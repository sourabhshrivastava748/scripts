python3 unifillSalesReport.py

ls -1 /tmp/unifill-sales-report* 
reportFilename=`ls -1t /tmp/unifill-sales-report* | head -1`
echo "Report file: ${reportFilename}"

MAIL_RECIPIENTS="sourabh.shrivastava@unicommerce.com"

MAIL_SUBJECT="Unifill Sales Report | Last 60 days"
MAIL_CONTENT="Please find the attachment"

echo ${MAIL_CONTENT} | mutt -s "${MAIL_SUBJECT}" -a "${reportFilename}" -- "${MAIL_RECIPIENTS}"
