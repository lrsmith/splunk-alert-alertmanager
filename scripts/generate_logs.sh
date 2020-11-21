#!/bin/sh

LOG="/tmp/log.log"

response_codes=(0 200 400 500)
customers=(none zaphod slartibartfast marvin ford arthur trillian )

while true
do
cell=$((1 + $RANDOM % 3))
customer=$((1 + $RANDOM % 6))
resp_code=$((1 + $RANDOM % 3))
TIMESTAMP=`date`


echo "{ \"TIMESTAMP\": \"$TIMESTAMP\", \"cell\": \"$cell\", \"customer\": \"${customers[$customer]}\", \"ResponseCode\": \"${response_codes[$resp_code]}\" }" >> $LOG

sleep 1
done
