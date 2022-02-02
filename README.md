# poediscordbot ![Build Status](https://github.com/poediscord/poediscordbot/workflows/Python%20application/badge.svg)
built with discordpy rewrite / python 3.7; supports pypy 3.6

## Changelog
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

