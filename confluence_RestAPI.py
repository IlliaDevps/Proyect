# This code sample uses the 'requests' library:
# http://docs.python-requests.org

import requests
from requests.auth import HTTPBasicAuth
import json

url = "https://kb.sprc.samsung.pl/rest/api/content/"
auth = HTTPBasicAuth("i.duverkher", "4i8c66j5q2o344ercc7kmlrq0u9mofq")


def get_page_json(page_id, expand=False):
    if expand:
        suffix = "?expand=" + expand
        # body.storage or body.view
    else:
        suffix = ""

    url = f"https://kb.sprc.samsung.pl/rest/api/content/{page_id}" + suffix

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
    response.encoding = "utf8"
    json_data = json.loads(response.text)
    # json_data = json.dumps(json.loads(response.text),sort_keys=True, indent=4, separators=(",", ": "))
    # print(json_data['body']['storage']['value'])

    return json_data  # ['body']['storage']['value']


print(get_page_json("563617140", 'body.storage'))  # Iza page 560881462


def get_and_set(page_id):
    json_data = get_page_json(page_id)

    new_json_data = dict()
    new_json_data['id'] = json_data['id']
    new_json_data['type'] = json_data['type']
    new_json_data['title'] = json_data['title']
    new_json_data['type'] = json_data['type']
    new_json_data['version'] = {"number": json_data['version']['number'] + 1}
    if not 'key' in json_data:
        new_json_data['key'] = json_data['space']['key']
    else:
        new_json_data['key'] = json_data['key']

    new_json_data['body'] = {'storage': {
        'value': '<p>the info you see here was created with Python using confluence Rest-API</p>' +
        '<p><table><tr><th>head1</th><th>head2</th></tr><tr><td>value1</td><td>value2</td></tr><tr><td>value3</td><td>value4</td></tr></table></p>', 'representation': 'storage'}}
    print(set_page_json(page_id, new_json_data))


def set_page_json(page_id, json_content):
    url = f"https://kb.sprc.samsung.pl/rest/api/content/{page_id}"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    response = requests.request(
        "PUT",
        url,
        data=json.dumps(json_content),
        headers=headers,
        auth=auth,
        verify=False
    )

    return (response.text)


print(get_and_set('563617140'))  # 563617140 confluence testing page
