import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import sys
import time

# Replace with your Netlify token and DNS zone ID
CERTBOT_DOMAIN = '_acme-challenge.' + sys.argv[1]
CERTBOT_VALIDATION = sys.argv[2]
DOMAIN = sys.argv[3]
API_TOKEN = sys.argv[4]
DNS_ZONE_ID = ""

# Headers for authentication
headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

# Max retry configuration
MAX_RETRIES = 5
BACKOFF_FACTOR = 1  # Exponential backoff factor for retries

# Create a session with retries
session = requests.Session()
retries = Retry(
    total=MAX_RETRIES,
    backoff_factor=BACKOFF_FACTOR,
    status_forcelist=[500, 502, 503, 504],
    allowed_methods=["GET", "POST", "DELETE"]
)
adapter = HTTPAdapter(max_retries=retries)
session.mount("https://", adapter)
session.mount("http://", adapter)

# Step 0: Find the DNS zone ID
def get_dns_zone_id():
    response = session.get("https://api.netlify.com/api/v1/dns_zones", headers=headers)
    response.raise_for_status()
    zones = response.json()
    for zone in zones:
        if zone["name"] == DOMAIN:
            return zone["id"]
    return None

# Step 1: Find the record_id for the subdomain
def get_record_id():
    res = []
    response = session.get(f"https://api.netlify.com/api/v1/dns_zones/{DNS_ZONE_ID}/dns_records", headers=headers)
    response.raise_for_status()
    records = response.json()
    for record in records:
        if record["hostname"] == CERTBOT_DOMAIN:
            res.append(record["id"])
    return res, len(res)

# Step 2: Delete the existing DNS record
def delete_dns_record(record_id):
    response = session.delete(f"https://api.netlify.com/api/v1/dns_zones/{DNS_ZONE_ID}/dns_records/{record_id}", headers=headers)
    response.raise_for_status()
    print(f"Deleted DNS record for {CERTBOT_DOMAIN}")

# Step 3: Create a new DNS record with the updated IP
def create_dns_record():
    payload = {
        "hostname": CERTBOT_DOMAIN,
        "type": "TXT",
        "value": CERTBOT_VALIDATION,
        "ttl": 3600
    }
    response = session.post(f"https://api.netlify.com/api/v1/dns_zones/{DNS_ZONE_ID}/dns_records", headers=headers, json=payload)
    response.raise_for_status()
    print(f"Created DNS TXT record for {CERTBOT_DOMAIN} with RECORD {CERTBOT_VALIDATION}")

# Execute the steps
'''
CLEAN_FLAG = 0
if len(sys.argv) > 5:
    if sys.argv[5] == "--cleanup":
        CLEAN_FLAG = 1

DNS_ZONE_ID = get_dns_zone_id()
if CLEAN_FLAG:
    records = get_record_id()
    for record_id in records:
        delete_dns_record(record_id)
else:
    create_dns_record()
'''

DNS_ZONE_ID = get_dns_zone_id()
records, len = get_record_id()
if len >= 1:
    for record_id in records:
        delete_dns_record(record_id)
create_dns_record()
time.sleep(30)
