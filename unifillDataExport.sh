echo "Unifill data export"

MobileList=$1

python3 unifillDataExport.py $MobileList

# Send mail
ls -1 /tmp/unifill-data-export* 
reportFilename=`ls -1t /tmp/unifill-data-export* | head -1`
echo "Report file: ${reportFilename}"

if [ -z "$reportFilename" ];
then
    echo "Report file is empty."
else
    current_date=$(date +'%d-%b-%Y %H:%M')

	MAIL_RECIPIENTS="sourabh.shrivastava@unicommerce.com"

	MAIL_SUBJECT="Unifill Data Export | ${current_date}"
	MAIL_CONTENT="Please find the attachment."

	echo ${MAIL_CONTENT} | mutt -s "${MAIL_SUBJECT}" -a "${reportFilename}" -- "${MAIL_RECIPIENTS}"
fi


