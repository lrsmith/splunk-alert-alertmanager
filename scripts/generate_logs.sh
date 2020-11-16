#!/bin/sh

LOG="/tmp/log.log"

while true
do
TIMESTAMP=`date`
echo "{ \"TIMESTAMP\": \"$TIMESTAMP\", \"cell\": \"1\", \"customer\": \"Zaphod\", \"ResponseCode\": \"500\" }" >> $LOG
echo "{ \"TIMESTAMP\": \"$TIMESTAMP\", \"cell\": \"1\", \"customer\": \"Ford\", \"ResponseCode\": \"500\" }" >> $LOG
echo "{ \"TIMESTAMP\": \"$TIMESTAMP\", \"cell\": \"1\", \"customer\": \"Marvin\", \"ResponseCode\": \"200\" }" >> $LOG

echo "{ \"TIMESTAMP\": \"$TIMESTAMP\", \"cell\": \"2\", \"customer\": \"Trillian\", \"ResponseCode\": \"500\" }" >> $LOG

echo "{ \"TIMESTAMP\": \"$TIMESTAMP\", \"cell\": \"3\", \"customer\": \"Slartibartfast\", \"ResponseCode\": \"500\" }" >> $LOG
echo "{ \"TIMESTAMP\": \"$TIMESTAMP\", \"cell\": \"3\", \"customer\": \"Arthur\", \"ResponseCode\": \"200\" }" >> $LOG

sleep 1
done
