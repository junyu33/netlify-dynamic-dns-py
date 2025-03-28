#!/bin/bash

# Configuration
source ./config.sh

# Get the current public IPv4 (without using proxy)
IP=$(ip -4 addr show ppp0 | grep inet | awk '{print $2}' | cut -d'/' -f1)

python3 nddns.py "$IP" "$ACCESSTOKEN" "$ZONE" "$RECORD"

# Log the update
echo "$(date): Updated $RECORD.$ZONE to IP $IP"
