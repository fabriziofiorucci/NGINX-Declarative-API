"""
GitOps support functions
"""

import base64
import requests

from requests import ReadTimeout, HTTPError, Timeout, ConnectionError, ConnectTimeout


# Fetches a URL content
def __fetchfromsourceoftruth__(url):
    # Policy must be fetched from external repository
    try:
        reply = requests.get(url=url, verify=False)
    except (ConnectTimeout, HTTPError, ReadTimeout, Timeout, ConnectionError):
        return 408, "URL " + url + " unreachable"

    return reply.status_code, reply.text


# If content starts with http(s):// fetches the object and return it b64-encoded
# Returns the status original content otherwise.
# Return is a tuple: status_code, content
def getObjectFromRepo(content: str):
    status_code = 200
    if content.lower().startswith("http://") or content.lower().startswith("https://"):
        # Policy is fetched from external repository
        status_code, content = __fetchfromsourceoftruth__(content)

        if status_code == 200:
            content = base64.b64encode(bytes(content, 'utf-8')).decode('utf-8')

    return status_code, content
