import logging

# -- Rename this file to config.py! --

import os

## --  Main
# Enter discord token from https://discordapp.com/developers/applications/me/
token = 'yoursupersecrettoken'

# reacts to pastebin posts with pob info in these channels
active_channels = ['active-pob']
# debug level
debug_level = logging.INFO
# This is your Project Root
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
# Enable PMs
allow_pming = True

## -- Adaptions
# bot status (presence) message
presence_message = '!pob <pastebin>'
# Color of the embed
color = 0x859900


## -- Logging
# Owners of the bot that can use the advanced/admin commands to export logs.
owners = ['Owner#1337']
dm_auto_log = True
# required vars: {ts}=timestamp, {u}=username, {uid} = user id, {content} = message content
dm_log_format = '{ts} <{u}({uid})>: {content}'
# Poll dm's every 60 minutes once.
dm_poll_rate_seconds=60*60*60

## -- Additionl Information at the bottom of the bot output
# text/configuration for the bottom
web_pob_text = "**Web PoB**"

poe_technology_enabled = True
poe_technology_text = "**Web Viewer"
