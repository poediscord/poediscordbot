# PoB Parsing Bot for Discord
*Written in Python 3.6*

### Used Libraries
- refer to the [requirements.txt](/requirements.txt)

### Utilized libraries & Inspiration:
- [discord.py](https://github.com/Rapptz/discord.py)
- [PoBPreviewBott](https://github.com/aggixx/PoBPreviewBot)
- [LiftDiscord Bot](https://github.com/andreandersen/LiftDiscord/)

### Finished
- Support for having active channels where the bot fetches all pastebin links and tries to past
- Support for having passive channels where the bot only triggers when using the command
- Parsing most of the information from the XML into classes to facilitate extensive custom output
- Various config options in `config.py`
- Secondary Defenses
- Primary defenses need to hit Thresholds to be displayed

### Future Work
- Configuration rework
    - Py3.5: not all configs are returned although they are available
- Refine Offense output
    - Poison/Ignite and Dots in general are crude
    - Maybe:
        - Balls
        - Arrows

- Start/Stop script: https://wolfpaulus.com/technology/pythonlauncher/
- Add supports for Active Skills from items (Ice Storm)
- Add support for Keystones
    - Add support for Endu/Frenzy/Power Charges
    - Number of totems
- Add support for "Notable" Uniques that are displayed in the extended version


### How To Run
- Copy and rename `config.example.py`
  ```bash
  cp config.example.py config.py
  ```
- Edit the new `config.py`
    - replace token
    - add channels the bots should react to and define keyword(s)
- Run `discord_pob.py`
- Bot logs into `discord_pob.log`

### Usage
- Bot reacts to `!pob <pastebin (not raw!) link>` in all configured passive channels on the invited server or to pastebin links it can parse in active channels.

### Showcase
![](https://cdn.discordapp.com/attachments/418758449954947076/423174211373236224/unknown.png)

