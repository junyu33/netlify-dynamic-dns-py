#!/bin/bash

# Configuration
source ./config.sh

if [ -z "$CERTBOT_DOMAIN" ] || [ -z "$CERTBOT_VALIDATION" ]; then
    echo "error: CERTBOT_DOMAIN or CERTBOT_VALIDATION undefined"
    exit 1
fi

python3 renew.py "$CERTBOT_DOMAIN" "$CERTBOT_VALIDATION" "$ZONE" "$ACCESSTOKEN"

if [ $? -eq 0 ]; then
    echo "success: renew.py executed，domain: $CERTBOT_DOMAIN, verification: $CERTBOT_VALIDATION"
else
    echo "fail: renew.py failed to execute"
    exit 1
fi

