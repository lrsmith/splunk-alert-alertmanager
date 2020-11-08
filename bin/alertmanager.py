import json
import sys
import requests


OK = 0
ERROR_CODE_UNKNOWN = 1
ERROR_CODE_VALIDATION_FAILED = 2

ALERT_MANAGER_URL='http://localhost:9093/api/v1/alerts'

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
    log("DEBUG: %s" % payload)
    return OK

def build_alertmanager_message(payload):
    ALERT_MANAGER_MSG['labels']['alertname'] = payload['search_name'] 
    return ALERT_MANAGER_MSG

if __name__ == '__main__':
    log("INFO Running python %s" % (sys.version_info[0]))
    payload = json.loads(sys.stdin.read())
#    if not valdidate_payload(payload):
#        sys.exit(ERROR_CODE_VALIDATION_FAILED)
    log("INFO: Sending alert payload")
    alert_payload=build_alertmanager_message(payload)
    res = requests.post(ALERT_MANAGER_URL, json=[alert_payload])
    

