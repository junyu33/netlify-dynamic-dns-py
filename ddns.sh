#!/bin/bash

# Configuration
ACCESSTOKEN="<your_access_token>"  # Netlify API access token
ZONE="<your_root_domain>"          # Domain name (Netlify DNS zone)
RECORD="<your_subdomain>"          # Subdomain (rdp.junyu33.me)

# Get the current public IPv4 (without using proxy)
IP=$(curl --noproxy '*' -s http://ipv4.icanhazip.com)

python3 nddns.py "$IP" "$ACCESSTOKEN" "$ZONE" "$RECORD"

# Log the update
echo "$(date): Updated $RECORD.$ZONE to IP $IP"
