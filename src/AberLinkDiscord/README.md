# AberLink

AberLink is a Discord bot that marks attendance in practicals and verifies student's discord accounts.

## Usage

TBD

## Initial setup

1. Check python3, pip and pipenv are installed
2. Navigate to a terminal and `git clone  <repository url>` and cd into its directory
3. `pipenv install` to install dependencies
4. Navigate to the discord developers site, create a new application, go to the bot tab, add a bot and then copy the token from that tab
5. create a .env file with the token from the previous step using the format `DISCORD_TOKEN=<yourtoken-here>`.

6. `pipenv run python3 -m aberlink` to run the server
7. use `which pipenv` to find file path to pipenv location
8. Navigate to the 0Auth2 tab and select bot from the scopes section, then scroll down and select the bot permissions: View channels and Send Messages. Copy the link from the scopes section and paste it into your web browser and select the servers you want to add the bot to
  
## Setting up as a service

1. Complete the steps from above apart from 6 and 7
2. create a file in `/etc/systemd/system/` called `aberlink.service` and add the following to the file:

```bash
[Unit]
Description=AberLink Discord bot
After=network.target
StartLimitIntervalSec=0

[Service]
Type=simple
Restart=always
RestartSec=1
User=<username>
WorkingDirectory=/home/<username>/aberlink/src/AberLinkDiscord
ExecStart=/usr/bin/pipenv run python3 -m aberlink

[Install]
WantedBy=multi-user.target
```

3. Once completed use the command `sudo systemctl daemon-reload` to reload the file

## The following commands are now used to manage the bot

1. `sudo systemctl start aberlink` - start the service
2. `sudo systemctl status aberlink` - get the status of the service
3. `sudo systemctl stop aberlink` - stop the service
4. `systemctl restart aberlink` - restart the service
5. `sudo systemctl enable aberlink/sudo systemctl disable aberlink` - enable/disable the service on boot of server.
6. `journalctl -ru aberlink.service` - view recent logs

## General maintenance

1. `pipenv update` to update dependencies
2. `git pull` to pull updates from the repository
3. `systemctl restart aberlink` to restart the service
