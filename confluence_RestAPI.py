# This code sample uses the 'requests' library:
# http://docs.python-requests.org
import certifi
import requests
from requests.auth import HTTPBasicAuth
import json

page_id = "560881462"
url = f"https://kb.sprc.samsung.pl/rest/api/content/{page_id}"

auth = HTTPBasicAuth("i.duverkher",
                     "4i8c66j5q2o344ercc7kmlrq0u9mofq")

headers = {
    "Accept": "application/json"
}

response = requests.request(
    "GET",
    url,
    headers=headers,
    auth=auth,
    verify=False
)

print(json.dumps(json.loads(response.text),
      sort_keys=True, indent=4, separators=(",", ": ")))
