import hmac
import hashlib
import time
import requests
import base64
from datetime import datetime, timezone

# Method for the request
method = "GET"
# Path of you DNS record. The format is always: /v1/user/self/zone/{domain}/record/{record-id}
path = "/v1/user/self/zone/contoso.com/record/123456789"
# API url for Websupport / Webonic
api = "https://rest.websupport.sk"
# The Query part is optional, you almost never use it.
query = ""
# This is for creating 
timestamp = int(time.time())

# Here should be your API key and secret which you generated on the site
apiKey = "xxxx-xxxx-xxxxx-xxxxxx"
secret = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# Creates a formated request
canonicalRequest = "%s %s %s" % (method, path, timestamp)
# Creates a hmac hash from the request
signature = hmac.new(bytes(secret, 'UTF-8'), bytes(canonicalRequest, 'UTF-8'), hashlib.sha1).hexdigest()

# Headers for the request. Note that, the date should be in UTC all times!
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Date": datetime.fromtimestamp(timestamp, timezone.utc).isoformat()
}

# Getting the stored DNS record from Websupport / Webonic
stored_ip = requests.get("%s%s%s" % (api, path, query), headers=headers, auth=(apiKey, signature)).json();
# Getting your current public IP address from a third-party system
current_ip = requests.get("https://api.ipify.org/?format=json").json();

# This is just for debugging
# print(stored_ip)

if stored_ip["content"] != current_ip["ip"] :
    # This part is the same from above, only the method changed.
    method = "PUT"
    timestamp = int(time.time())
    canonicalRequest = "%s %s %s" % (method, path, timestamp)
    signature = hmac.new(bytes(secret, 'UTF-8'), bytes(canonicalRequest, 'UTF-8'), hashlib.sha1).hexdigest()

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Date": datetime.fromtimestamp(timestamp, timezone.utc).isoformat()
    }

    # This is the JSON body which we will send to the API. Note that, in the "Name" property, you should only put the last part of your domain.
    # For example: if your DNS record is server01.contoso.com, you will only put the "server01" part in there.
    body = {
        "name": "server01",
        "content": current_ip["ip"],
        "ttl": 600
    }

    # Sends the request
    response = requests.put("%s%s%s" % (api, path, query), headers=headers, auth=(apiKey, signature), json=body).json()

    # Used for debugging response
    # print(response)
    
    dc_data = {
        "content": "__[INFO] IP Cím változás!__" 
        + "\nDNS frissítés történt ekkor: " + datetime.today().isoformat()  
        + "\nDNS név: *server01.contoso.com*" 
        + "\nRégi IP cím: " + stored_ip["content"]
        + "\nÚj IP cím: **" + current_ip["ip"] + "**"
        + "\n\nWebsupport API válasz"
        + "\n||```json\n" + str(response) + "```||"
    }

    # Sends the Discord message through webhook
    requests.post("https://discord.com/api/webhooks/xxxx/xxxxx", data=dc_data )