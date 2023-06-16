python3 ufSummary.py

ls -1 /tmp/uf-summary-* 
reportFilename=`ls -1t /tmp/uf-summary-* | head -1`
echo "Report file: ${reportFilename}"

yesterday_date=$(date -d "yesterday 13:00" +'%d-%m-%Y')

MAIL_RECIPIENTS="sourabh.shrivastava@unicommerce.com,dixit.garg@unicommerce.com,ankur.pratik@unicommerce.com,ankit.jain03@unicommerce.com,bhupi@unicommerce.com,kapil@unicommerce.com,prateek.mahajan@unicommerce.com,adarsh.bajpai@unicommerce.com,rakshit.jain@unicommerce.com,oncall@unicommerce.com"

# MAIL_RECIPIENTS="sourabh.shrivastava@unicommerce.com"

MAIL_SUBJECT="Unfulfillable Sale Order Summary | ${yesterday_date}"
MAIL_CONTENT="Please find the attachment. Report prepared by alpha team"

echo ${MAIL_CONTENT} | mutt -s "${MAIL_SUBJECT}" -a "${reportFilename}" -- "${MAIL_RECIPIENTS}"
