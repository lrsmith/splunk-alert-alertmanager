import json
import sys
import requests

OK = 0
ERROR_CODE_UNKNOWN = 1
ERROR_CODE_VALIDATION_FAILED = 2

ALERT_MANAGER_MSG = {
  'status' : 'firing',
  'labels' : {
      'alertname' : 'alertname',
      'service'   : 'splunk',
      'severity'  : 'warning',
      'instance'  : 'instance',
  },
  'annotations'   : {
      'summary'   : 'Annotation Summary'
  },
  'generatorURL'  : 'http://prometheus.int.example.net/<generating_expression>'
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
    ALERT_MANAGER_MSG['labels']['alertname'] = payload['search_name'] 
    return ALERT_MANAGER_MSG

if __name__ == '__main__':
    payload = json.loads(sys.stdin.read())

    if not valdidate_payload(payload):
        sys.exit(ERROR_CODE_VALIDATION_FAILED)
    alert_payload=build_alertmanager_message(payload)

    config = payload.get('configuration')
    log("INFO Sending alert payload")
    res = requests.post(config.get('alertmanager_url'), json=[alert_payload])
    

