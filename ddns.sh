#!/bin/bash

# Configuration
source ./config.sh

# Get the current public IPv4 (without using proxy)
IP=$(curl --noproxy '*' -s http://ipv4.icanhazip.com)

python3 nddns.py "$IP" "$ACCESSTOKEN" "$ZONE" "$RECORD"

# Log the update
echo "$(date): Updated $RECORD.$ZONE to IP $IP"
