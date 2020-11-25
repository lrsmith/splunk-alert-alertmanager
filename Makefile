
build_app:
	tar zcpf ./build/alertmanager.tgz ./app

## Docker Targets 

# Alertmanager

alertmanager_start:
	docker run -d -p 9093:9093 -v `pwd`/alertmanager:/etc/alertmanager --network bridge --name alertmanager prom/alertmanager
	sleep 10

alertmanager_stop:
	docker stop alertmanager

alertmanager_rm:
	docker rm alertmanager


# Splunk

splunk_start:
	docker stop splunk
	docker rm splunk
	docker run -d -p 8000:8000 -e "SPLUNK_START_ARGS=--accept-license" -e "SPLUNK_PASSWORD=password" -v /tmp/log.log:/tmp/log.log --network bridge --name splunk splunk/splunk:latest


## Local testing Targets
# Only requires Alertmanager to be running.

group_by_none:
	cat ./example/splunk_payload_1.json | python ./app/bin/alertmanager.py

group_by_one:
	cat ./example/splunk_payload_2.json | python ./app/bin/alertmanager.py

group_by_two:
	cat ./example/splunk_payload_3.json | python ./app/bin/alertmanager.py


test: start_alertmanager group_by_none group_by_one group_by_two

