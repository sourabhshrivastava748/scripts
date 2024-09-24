echo "Unifill API Address Export"


echo "input.csv"
cat input.csv

python3 getUnifillAddresses.py

# Send mail
ls -1 /tmp/unifill-mobile-with-addresses* 
reportFilename=`ls -1t /tmp/unifill-mobile-with-addresses* | head -1`
echo "Report file: ${reportFilename}"

if [ -z "$reportFilename" ];
then
    echo "Report file is empty."
else
    current_date=$(date +'%Y%m%d%H%M%S')

	MAIL_RECIPIENTS=${EmailRecipientList}
	# MAIL_RECIPIENTS_CC="sourabh.shrivastava@unicommerce.com,ankur.pratik@unicommerce.com,ankit.jain03@unicommerce.com,bhupi@unicommerce.com"
	MAIL_RECIPIENTS_CC="sourabh.shrivastava@unicommerce.com"

	BUILD_TRIGGER_BY=$(curl -k --silent ${BUILD_URL}/api/xml | tr '<' '\n' | egrep '^userId>|^userName>' | sed 's/.*>//g' | sed -e '1s/$/ \//g' | tr '\n' ' ')

	MAIL_SUBJECT="Unifill API Address Export | ${current_date}"
	MAIL_CONTENT="Please find the attachment. Build triggered by ${BUILD_TRIGGER_BY}"

	echo ${MAIL_CONTENT} | mutt -s "${MAIL_SUBJECT}" -a "${reportFilename}" -c "${MAIL_RECIPIENTS_CC}" -- "${MAIL_RECIPIENTS}"
fi


