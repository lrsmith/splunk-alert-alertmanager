import json
import sys
import requests

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
      'severity'     : 'critical',
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
    ALERT_MANAGER_MSG['labels']['alertname']         = payload['search_name'] 
    ALERT_MANAGER_MSG['labels']['instance']          = payload['server_host'] 

    # Shows up as 'source' in alert manager and takes you to Splunk Search
    ALERT_MANAGER_MSG['generatorURL']                = payload['server_uri'] + payload['search_uri'] 

    return ALERT_MANAGER_MSG

if __name__ == '__main__':
    payload = json.loads(sys.stdin.read())

    if not valdidate_payload(payload):
        sys.exit(ERROR_CODE_VALIDATION_FAILED)
    alert_payload=build_alertmanager_message(payload)

    config = payload.get('configuration')
    #log("INFO Sending alert payload")
    res = requests.post(config.get('alertmanager_url'), json=[alert_payload])
    

