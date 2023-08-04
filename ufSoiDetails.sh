python3 ufSoiDetails.py

ls -1 /tmp/soi-details-* 
reportFilename=`ls -1t /tmp/soi-details-* | head -1`
echo "Report file: ${reportFilename}"


MAIL_RECIPIENTS="sourabh.shrivastava@unicommerce.com"

MAIL_SUBJECT="Unfulfillable Sale Order Items Details"
MAIL_CONTENT="Please find the attachment."

echo ${MAIL_CONTENT} | mutt -s "${MAIL_SUBJECT}" -a "${reportFilename}" -- "${MAIL_RECIPIENTS}"

# python3 checkIfIndexExistsMysql.py 
