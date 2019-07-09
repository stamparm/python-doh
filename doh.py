#!/usr/bin/env python

from __future__ import print_function

import json
import os
import re
import socket
import ssl
import subprocess
import sys

PY3 = sys.version_info >= (3, 0)

if hasattr(ssl, "_create_unverified_context"):
    ssl._create_default_https_context = ssl._create_unverified_context
    DOH_SERVER = "1.1.1.1"
else:
    DOH_SERVER = "cloudflare-dns.com"

if PY3:
    import urllib.request
    _urlopen = urllib.request.urlopen
    _Request = urllib.request.Request
else:
    import urllib2
    _urlopen = urllib2.urlopen
    _Request = urllib2.Request

def doh(query, type='A', server=DOH_SERVER, fallback=True, verbose=False):
    """
    Returns domain name query results retrieved by using DNS over HTTPS
    # Reference: https://developers.cloudflare.com/1.1.1.1/dns-over-https/json-format/
    """

    retval = None

    try:
        req = _Request("https://%s/dns-query?name=%s&type=%s" % (server, query, type), headers={"Accept": "application/dns-json"})
        content = _urlopen(req).read().decode()
        reply = json.loads(content)

        if "Answer" in reply:
            answer = json.loads(content)["Answer"]
            retval = [_["data"] for _ in answer]
        else:
            retval = []
    except Exception as ex:
        if verbose:
            print("Exception occurred: '%s'" % ex)

    if retval is None and fallback:
        if type == 'A':
            try:
                retval = socket.gethostbyname_ex(query)[2]
            except (socket.error, IndexError):
                pass

        if retval is None:
            process = subprocess.Popen(("nslookup", "-q=%s" % type, query), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            content = (process.communicate()[0] or "").decode().replace("\r", "")

            if "\n\n" in content and "can't" not in content.lower():
                answer = content.split("\n\n", 1)[-1]
                retval = re.findall(r"(?m)^%s.+= ([^=,\n]+)$" % re.escape(query), answer) or re.findall(r"Address: (.+)", answer)

                if not retval:
                    match = re.search(r"Addresses: ([\s\d.]+)", answer)
                    if match:
                        retval = re.split(r"\s+", match.group(1).strip())

    return retval
