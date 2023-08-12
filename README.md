# poediscordbot [![Discord POB](https://github.com/poediscord/poediscordbot/actions/workflows/python-app.yml/badge.svg)](https://github.com/poediscord/poediscordbot/actions/workflows/python-app.yml)
built with discordpy rewrite / python 3.7; supports pypy 3.6

## Running the bot
Currently, there's no way to just invite an instance of the bot. You can run it on your own machine or in the cloud though and do so. Follow the [wiki installation guide](https://github.com/poediscord/poediscordbot/wiki/Installation) if you need directions.

If you encounter issues or need more support feel free to open an issue or visit the [Reddit PoE Discord](https://discord.com/invite/pathofexile) and post in `#tooldev-general`

## Changelog
- 2023-08-17: add configurable decimals for offense and defense (see config example) default is 1 and 0 respectively
- 2023-04-18: add 3.21 tree
- 2023-04-18: rework embed
  - embed is now inlined by default and has condensed numbers 10000=>10k, 1000000=>1M
  - add new command syncing logic / command to resync for the guild leader
- 2022-11-13: add tree renderer
  - the bot will now embed a small preview of the tree if you enable the function in the config:
    ```python
    render_tree_image = True
    # deletion "scheduler" timer - runs every 20min by default
    tree_image_cleanup_minute_cycle = 20
    # folder within the root dir containing the images - leave as is if you don't need to change it
    tree_image_dir = ROOT_DIR + "tmp/img"
    # delete files where the diff between now and the creation date is bigger than this amount (in seconds)
    tree_image_delete_threshold_seconds = 60 * 20
    ```
    - images are stored as svg and pngs in the directory you have this bot in the subfolder `tmp/img`
    - generated images are cleaned up routinely (every 20 minutes)
- 2022-09-15: update to discord.py 2.0.x
  - configuration updated
    - `owner` is now expecting user ids, not `nick#number` 
    - `active_channels` is now expecting channel ids, not channel names
  - active channels now also include threads (and hopefully the forums function)
  - migrate `!pob` to `/pob` slash command
  - currently sync command tree on every restart
- 2022-02-02: reworked importers, added flag `enable_open_in_pob_feature = True` which will use a static site to redirect to a `pob://` link
  - support pobbin and poe.ninja as sites to parse builds from, examples: https://pobb.in/qO1_QpuQLeDd & https://poe.ninja/pob/19
  - example Link: https://fwidm.github.io/pob-redirect/index.html?pobbin=qO1_QpuQLeDd will open the link in pob if you have the [handlers setup (reddit infopost)](https://www.reddit.com/r/pathofexile/comments/siao2j/poblink_quickload_links_for_path_of_building/).
## Docker
- `docker compose up` - start the container
    - add `--build` to rebuild the image
    
## PoB Cog
Do not forget to re-do your config.py every time you pull. Breaking changes may happen at this stage.

### Utilized libraries & Inspiration:
- [discord.py](https://github.com/Rapptz/discord.py)
- [PoBPreviewBott](https://github.com/aggixx/PoBPreviewBot)
- [LiftDiscord Bot](https://github.com/andreandersen/LiftDiscord/)

### Future Work
- Refine Offense output
- !pob `manually input build name here` <pob link>
- output mind over matter%
- small output command to spam less as configs have been blown up
    - basically display consolidated defenses and offense and the info vs what (sirus,...)
### Usage
- Bot reacts to `!pob <pastebin (not raw!) link>` in all configured passive channels on the invited server or to pastebin links it can parse in active channels.

### Showcase
![](https://cdn.discordapp.com/attachments/175005585203396622/832324723794116636/unknown.png)

