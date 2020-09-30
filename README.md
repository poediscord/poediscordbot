# poediscordbot [![Build Status](https://travis-ci.org/poediscord/poediscordbot.svg?branch=master)](https://travis-ci.org/poediscord/poediscordbot)
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
    - Poison/Ignite and Dots in general are crude
    - Maybe:
        - Balls
        - Arrows
- Start/Stop script: https://wolfpaulus.com/technology/pythonlauncher/
- Number of totems
- Support for Auras from Items (check if they're active)
- Add support for "Notable" Uniques that are displayed in the extended version

### Usage
- Bot reacts to `!pob <pastebin (not raw!) link>` in all configured passive channels on the invited server or to pastebin links it can parse in active channels.

### Showcase
![](https://cdn.discordapp.com/attachments/418758449954947076/423174211373236224/unknown.png)

