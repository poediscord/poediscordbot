import logging

# -- Rename this file to config.py! --

# Enter discord token from https://discordapp.com/developers/applications/me/
import os

token = 'yoursupersecrettoken'
# color of the embed
color = 0x859900
# keywords to trigger the bot in passive channels
keywords = ['!pob']
# reacts to pastebin posts with pob info in these channels
active_channels = ['pob']
# debug level
debug_level = logging.INFO

presence_message = '!pob <pastebin>'
# This is your Project Root
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
