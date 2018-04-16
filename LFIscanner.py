import argparse
import json
import sys
import re
from Engine import Engine
from urllib3.exceptions import NewConnectionError
print("""

+++++++++++++++++++++++++++++++++++++++++++++/++++++++++++++++++++++++++++++++++++++++++++++++++++++
++++++++++++++++++++++++++++++++++++++++++/:. ````````.-:/++++++++++++++++++++++++++++++++++++++++++
++++++++++++++++++++++++++++++++++++++/:.`                `-:+++++++++++++++++++++++++++++++++++++++
++++++++++++++++++++++++++++++++++++/.`                      `-+++++++++++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++++++++-        ``.-----..`        `:+++++++++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++++++/`      `.:///////////:-`       .++++++++++++++++++++++++++++++++++
++++++++++++++++++++++++++++++++/`      ./////////////////:`      `+++++++++++++++++++++++++++++++++
++++++++++++++++++++++++++++++++`     `:////////////////:://.      .++++++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++++-      :///////////////:.:////.      `+++++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++++`     .//////////////:`.://////      .+++++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++++      -////////////-` .////////      .+++++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++++      .//:.-:////-` `-/////////      -+++++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++++       ///:` `.-`  `://///////-      /+++++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++++       `////.     .//////////-      .++++++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++++        `:///-  `://////////.      `+++++++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++++          `-//:.:////////:.`      ./+++++++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++++            ``.-::::::-.`       `-+++++++++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++++                              `-/++++++++++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++++      ./-``                `.:+++++++++++++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++++      .+++/:-.````````  -:/++++++++++++++++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++++      .+++++++++++//++:/+++++++++++++++++++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++++      .++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++++      .++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++++      .++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++++      .++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++++      .++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++++      .++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++++      .++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++++      .++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++++/:::::/++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Made for PentestCloud.io by Luka Sikic @CroCyber
""")

parser = argparse.ArgumentParser()
parser._action_groups.pop()

required = parser.add_argument_group('required arguments')
optional = parser.add_argument_group('optional arguments')

required.add_argument("-u", "--url", help="Target URL to scan, example: http://localhost/index.php?page=about", action="store", type=str, required=True)
optional.add_argument("-w", "--windows", help="(optional) Use if server is windows", action="store_true")
optional.add_argument("-v", "--verbose", help="(optional) display every request", action="store_true")
optional.add_argument("-c", "--cookie", help="(optional) HTTP request cookie", action="store", type=str)

args = parser.parse_args()

def is_valid_url(url):
    regex = re.compile(
        r'^https?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url is not None and regex.search(url)

if not (is_valid_url(args.url)):
    print("[-] Not a valid URL")
    sys.exit()

with open('payloads.json', 'r') as f:
    elements = json.load(f)

if(args.windows):
    print("[*] Using windows server payloads")
    matches = elements["windows"]
    payloads = elements['windows'].keys()
    prefixes = elements['windowsPrefix']

else:
    print("[*] Using linux server payloads")
    matches = elements["linux"]
    payloads = elements['linux'].keys()
    prefixes = elements['linuxPrefix']

urls = []
for prefix in prefixes:
    urls.append(args.url + prefix)

engine = Engine(urls, payloads, matches, args.cookie, args.verbose)
try:
    engine.start()
except Exception:
    print("[-] Something went wrong, make sure provided URL is valid and accessible.")