# Websupport / Webonic DDNS updater

This is a simple Python script made for DNS updating at Websupport and Webonic hosting with a plain notification system through Discord.

## What you need?

You need to acquire a API key and an API secret to do this. After then you should get the ID of your DNS record which you want to update. Optionally, you can create a Discord webhook link if you want to use the Discord notification system.

## How can I get an API key, secret and ID of DNS record

For API, you should head to `https://admin.websupport.hu/hu/auth/security-settings` and create a new API key.

For DNS record, the easiest way to get a DNS record id is if you create the record by hand, and you copy the ID from the URL. For example: `https://admin.websupport.hu/hu/domain/dns/edit/1391605?domain=ruzger.hu&recordId=107646638&type=A`. You want to copy here the `recordId=107646638` part!

## License and other stuff

This script is licensed under MIT-license, so do whatever you want with it. Also, if you find a bug or have an idea, please write in the "Issues" section!
