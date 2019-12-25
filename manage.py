import subprocess
import requests
import sys
from urllib.parse import urlsplit
import json

error_codes = [400, 404, 403, 408, 409, 501, 502, 503]

url = sys.argv[1]

response = requests.get(url).text

with open('example.html', 'w') as f:
    f.write(response)

links = subprocess.run(['oust', 'example.html', 'links'], stdout=subprocess.PIPE).stdout.decode('utf-8')
links = links.splitlines()

urls = []
for link in links:
    try:
        status_code = requests.get(link).status_code
    except Exception:
        continue
    domain = urlsplit(url).netloc
    broken = 'Yes' if status_code in error_codes else 'No'
    expiration = subprocess.run(['python', 'domain_exp.py', domain], stdout=subprocess.PIPE).stdout.decode('utf-8')
    if 'ConnectionResetError' in expiration:
        expiration = 'Unable to get data from whois.'
    urls.append({
        'url': link,
        'domain': domain,
        'broken': broken,
        'expiration': expiration,
        'status_code': status_code,
    })

with open('result.json', 'w') as f:
    json.dump(urls, f)

