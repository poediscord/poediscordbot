import logging

# -- Rename this file to config.py! --

# Enter discord token from https://discordapp.com/developers/applications/me/
token = 'NDE4Nzc3Mjk1NzEzNzMwNTcw.DXnH5w.MbbuPBLif2H8rPWNqNoAilXtYtU'
# color of the embed
color = 0x859900
# keywords to trigger the bot in passive channels
keywords = ['!pob','!longasscustomcommand']

# reacts to pastebin posts with pob info in these channels
active_channels = ['active-pob']
# debug level
debug_level = logging.INFO

presence_message = '!pob <pastebin>'