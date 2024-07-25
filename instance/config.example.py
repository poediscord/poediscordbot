import logging

# -- Rename this file to config.py! --

import os

## --  Main
# Enter discord token from https://discordapp.com/developers/applications/me/
# expected format: `token = 'supersecrettoken'`
token = 'supersecrettoken'

# reacts to pastebin posts with pob info in these channels (get the id via right click)
active_channels = [111]
# debug level
debug_level = logging.INFO
# This is your Project Root (fixme: remove the dirty .. workaround!)
ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) + os.sep + ".." + os.sep
# Enable PMs
allow_pming = True

## -- Adaptions
# bot status (presence) message
presence_message = 'with pastebins'
# Color of the embed
color = 0x859900

## -- Logging
# Owner of the bot that can use the advanced/admin commands to export logs (id)
owners = [111]
dm_auto_log = True
# required vars: {ts}=timestamp, {u}=username, {uid} = user id, {content} = message content
dm_log_format = '{ts} <{u}({uid})>: {content}'
# Poll dm's every 60 minutes once.
dm_poll_rate_seconds = 60 * 60 * 60

## -- Additionl Information at the bottom of the bot output
# enable the new feature to redirect to a pob:// link via static github page
enable_open_in_pob_feature = True

# -- Enable image rendering for peoples trees - resulting images are stored under tmp/img/<pastesourcename>_<key>.[svg &
# png] - e.g. pobbin_ATMRSryREQej.png
render_tree_image = True
# deletion "scheduler" timer - runs every 20min by default
tree_image_cleanup_minute_cycle = 20
# folder within the root dir containing the images - leave as is if you don't need to change it
tree_image_dir = ROOT_DIR + "tmp/img"
# delete files where the diff between now and the creation date is bigger than this amount (in seconds)
tree_image_delete_threshold_seconds = 60 * 15

# here you can change the colors used for tree rendering. Currently we only support named colors for svgs:
# https://www.december.com/html/spec/colorsvg.html
# any inactive elements are colored like this and are transparent
renderer_inactive_color = 'grey'
# any active elements are colored like this unless they are defined below
renderer_active_color = 'darkgoldenrod'
# any masteries are colored like this
renderer_mastery_color = 'papayawhip'
# keystone colors
renderer_keystone_color = 'peru'

# decimal output adaptions
dps_decimals = 1
defense_decimals = 0

# custom mods
custom_mods_lines = 5
