"""Script for updating the IP address on Cloudflare if it has changed."""

import json
import time
from pathlib import Path

import requests


CONFIG = "config.json"
IP_FILE = "public_ip"
IP_URL = "http://ip.42.pl/raw"


def get_ip():
    """Get public IP adrdess in raw format from IP_URL."""
    response = requests.get(IP_URL)
    return str(response.text)


def get_old_ip():
    """Get IP address from file."""
    if not Path(IP_FILE).is_file():
        return ""
    with open(IP_FILE, "r") as f:
        ip = f.read().strip()
    return ip


def save_new_ip(ip):
    """Save IP address to file."""
    with open(IP_FILE, "w") as f:
        f.write(ip)


def read_config():
    """Retrieve config."""
    with open(CONFIG) as f:
        config = json.load(f)
        return config


def set_ip(current_ip, myconfig):
    """Set new IP address in Cloudflare for all zones and records specified in config.json."""
    api_token = myconfig.get("API_TOKEN")

    for zoneobj in myconfig.get("ZONES"):
        zone_id = zoneobj.get("ZONE_ID")

        headers = {
                "Authorization": "Bearer %s" % api_token,
                "Content-Type": "application/json"
                }

        for record in zoneobj.get("RECORDS"):
            record_name = record["name"]
            record_id = record["id"]
            url = "https://api.cloudflare.com/client/v4/zones/%(zone_id)s/dns_records/%(record_id)s" % {"zone_id": zone_id, "record_id": record_id}

            payload = {
                    "type": "A",
                    "name": record_name,
                    "content": current_ip
                    }
            response = requests.put(url, headers=headers, data=json.dumps(payload))
            if response.status_code == 200:
                print("Successfully updated IP in Cloudflare for record %s" % record_name)
            else:
                print("IP could not be updated in Cloudflare.")
                print("Status code: %s" % response.status_code)
                print("Message: %s" % response.text)


def do_ddns():
    """Get current IP, compare it to the IP saved in IP_FILE, update Cloudflare records if necessary."""
    # Try to get IP multiple times if request fails
    for _x in range(5):
        try:
            current_ip = get_ip()
            if current_ip != get_old_ip():
                print("The IP address has changed! New IP: %s\n" % current_ip)
                save_new_ip(current_ip)
                myconfig = read_config()
                set_ip(current_ip, myconfig)
            break
        except requests.exceptions.ConnectionError:
            time.sleep(10)
    else:
        raise Exception("Failed to retrieve IP address from '%s'. Tried 5 times and gave up." % IP_URL)


if __name__ == "__main__":
    do_ddns()
