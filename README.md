# DDNS
Script that checks your IP address and sets it on your Cloudflare records if it has changed.
Inspired by https://github.com/creimers/cloudflare-ddns.

## Initialisation

1. Install the python requirements from `requirements.txt`.
2. Copy `config_default.json` to `config.json` and fill in your Cloudflare details (more info below).
3. Run `python3 update_dns.py` to check if things are working.
4. Setup a cron job that regularly runs this script, e.g. like this (running evey 30 minutes):
   `*/30 * * * * cd /path/to/cloudflare-ddns && python3 update_dns.py`


## Manage API tokens on Cloudflare

You can retrieve your global API key and create API tokens with specific permissions via your Cloudflare profile:
https://dash.cloudflare.com/profile/api-tokens.

The full Cloudflare API documentation can be found here: https://api.cloudflare.com/.


## Getting Zone IDs from Cloudflare

```
curl -X GET "https://api.cloudflare.com/client/v4/zones" \
    -H "X-Auth-Email: user@example.com" \
    -H "X-Auth-Key: 1234567893feefc5f0q5000bfo0c38d90bbeb" \
    -H "Content-Type: application/json"
```

## Getting Record IDs from Cloudflare

Replace `[zoneID]` with the proper Zone ID in the following call:

```
curl -X GET "https://api.cloudflare.com/client/v4/zones/[zoneID]/dns_records" \
    -H "X-Auth-Email: user@example.com" \
    -H "X-Auth-Key: 1234567893feefc5f0q5000bfo0c38d90bbeb" \
    -H "Content-Type: application/json"
```

Look for `"name": "[your URL]"` and get the ID.
