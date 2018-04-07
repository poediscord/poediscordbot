import logging

# -- Rename this file to config.py! --

import os
# Enter discord token from https://discordapp.com/developers/applications/me/
token = 'yoursupersecrettoken'
# color of the embed
color = 0x859900
# keywords to trigger the bot in passive channels
keywords = ['!pob']
# reacts to pastebin posts with pob info in these channels
active_channels = ['pob']
# debug level
debug_level = logging.DEBUG
# bot status (presence) message
presence_message = '!pob <pastebin>'
# This is your Project Root
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))