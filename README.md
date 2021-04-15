# poediscordbot ![Build Status](https://github.com/poediscord/poediscordbot/workflows/Python%20application/badge.svg)
built with discordpy rewrite / python 3.7; supports pypy 3.6

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

