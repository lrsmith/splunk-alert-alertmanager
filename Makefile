

## Docker Targets

start:
	docker run -d -p 9093:9093 -v `pwd`/alertmanager:/etc/alertmanager --network bridge --name alertmanager prom/alertmanager


## Testing Targets

group_by_none:
	cat ./example/splunk_payload_1.json | python ./app/bin/alertmanager.py

group_by_one:
	cat ./example/splunk_payload_2.json | python ./app/bin/alertmanager.py

group_by_two:
	cat ./example/splunk_payload_3.json | python ./app/bin/alertmanager.py


test: group_by_none group_by_one group_by_two



