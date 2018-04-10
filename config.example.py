import logging

# -- Rename this file to config.py! --

import os

## --  Main
# Enter discord token from https://discordapp.com/developers/applications/me/
token = 'yoursupersecrettoken'
# keywords to trigger the bot in passive channels
keywords = ['!pob']
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
owners = ['Faust#2687']
auto_log = False
