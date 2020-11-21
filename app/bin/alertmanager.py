import json
import sys
import requests
import gzip
import csv
import copy

OK = 0
ERROR_CODE_UNKNOWN = 1
ERROR_CODE_VALIDATION_FAILED = 2

# This is the JSON payload that Alertmanager expects to see. This will
#  be populated by data from the Splunk Alert Payload.
ALERT_MANAGER_MSG = {
  'status' : 'firing',
  'labels' : {
      'alertname'    : '',                  # Populate with Splunk Search Name
      'job'          : 'splunk',            
      'severity'     : '',                  # Populate with Alert param
      'instance'     : '',                  # Populate with Splunk Server Host
  },
  'annotations'      : {
      'summary'      : 'Annotation Summary'
  },
  'generatorURL'  : ''                      # Populate with Splunk server and search URI
}

def log(msg, *args):
    sys.stderr.write(msg + " ".join([str(a) for a in args]) + "\n")

def valdidate_payload(payload):
    if not 'configuration' in payload:
      log("FATAL Invalid payload, missing 'configuration'")
      return False

    config = payload.get('configuration')

    # No default alertmanager URL is set and app setup is required.
    alertmanager_url = config.get('alertmanager_url')
    if alertmanager_url == '':
        log("ERROR Validation error: Alertmanager URL not specified")
        return False
    return True

def build_alertmanager_message(payload):
    # Set 'global'
    ALERT_MANAGER_MSG['labels']['alertname']         = payload['search_name'] 
    ALERT_MANAGER_MSG['labels']['instance']          = payload['server_host'] 
        # Shows up as 'source' in alert manager and takes you to Splunk Search
    ALERT_MANAGER_MSG['generatorURL']                = payload['server_uri'] + payload['search_uri'] 
    ALERT_MANAGER_MSG['labels']['severity']          = payload['configuration']['severity'] 

    alerts = []

    # Split out alert(s) based on fields. i.e. cell or cell,customer
    if payload['configuration'].has_key('group_by'):

        log("INFO : Grouping alerts by %s." % payload['configuration']['group_by'])
        results = set()

        with gzip.open(payload.get('results_file'),'rt') as f:
            csv_dict = csv.DictReader(f)
            for row in csv_dict:
                tmp_hash = {}
                for field in set(payload['configuration']['group_by'].split(",")):
                    tmp_hash[field] = row[field]
                results.add(json.dumps(tmp_hash))

        # For each result generate an alert
        for tup in results:
            tmp_alert = copy.deepcopy(ALERT_MANAGER_MSG) 
            tmp_hash = json.loads(tup)
            for key in tmp_hash:
                tmp_alert['labels'][key] = tmp_hash[key]
            alerts.append(tmp_alert)

    else:
        alerts.append(ALERT_MANAGER_MSG)

    return alerts 

if __name__ == '__main__':

    payload = json.loads(sys.stdin.read())

    if not valdidate_payload(payload):
        sys.exit(ERROR_CODE_VALIDATION_FAILED)

    config = payload.get('configuration')

    alert_payload=build_alertmanager_message(payload)
    res = requests.post(config.get('alertmanager_url'), json=alert_payload)


