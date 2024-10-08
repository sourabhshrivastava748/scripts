set -e

echo "PII Auditor Data Export"

python3 getPiiAuditorData.py

# Send mail
ls -1 /tmp/pii-auditor-details* 
reportFilename=`ls -1t /tmp/pii-auditor-details* | head -1`
echo "Report file: ${reportFilename}"


ls -1 /tmp/suspicious-users* 
reportFilename2=`ls -1t /tmp/suspicious-users* | head -1`
echo "Report file 2: ${reportFilename2}"



if [ -z "$reportFilename" ];
then
    echo "Report file is empty."
else
    current_date=$(date +'%Y%m%d%H%M%S')

	MAIL_RECIPIENTS="sourabh.shrivastava@unicommerce.com"
	# MAIL_RECIPIENTS_CC="turbo@unicommerce.com"
	# MAIL_RECIPIENTS_CC="sourabh.shrivastava@unicommerce.com"

	# BUILD_TRIGGER_BY=$(curl -k --silent ${BUILD_URL}/api/xml | tr '<' '\n' | egrep '^userId>|^userName>' | sed 's/.*>//g' | sed -e '1s/$/ \//g' | tr '\n' ' ')

	MAIL_SUBJECT="PII Auditor Data Export | Last 7 days"
	MAIL_CONTENT="Please find the attachments"

	echo ${MAIL_CONTENT} | mutt -s "${MAIL_SUBJECT}" -a "${reportFilename}" -a "${reportFilename2}" -c "${MAIL_RECIPIENTS_CC}" -- "${MAIL_RECIPIENTS}"
fi


