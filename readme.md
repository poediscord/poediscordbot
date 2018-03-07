# PoB Parsing Bot for Discord
*Written in Python 3.6*

### Used Libraries
- zlib
- retry
- discord.py

### Utilized libraries & Inspiration:
- [discord.py](https://github.com/Rapptz/discord.py)
- [PoBPreviewBott](https://github.com/aggixx/PoBPreviewBot)
- [LiftDiscord Bot](https://github.com/andreandersen/LiftDiscord/)

### Finished
- Support for having active channels where the bot fetches all pastebin links and tries to past
- Support for having passive channels where the bot only triggers when using the command
- Parsing most of the information from the XML into classes to facilitate extensive custom output
- Various config options in `config.py`
### Future Work
- Refine Offense output
    - Poison/Ignite and Dots in general are crude
    - Only show crit stats when they are above threshholds
    - Maybe: 
        - Number of totems
        - Balls
        - Arrows 
- Customizable Layout (maybe)
- Start/Stop script: https://wolfpaulus.com/technology/pythonlauncher/
- Add supports for Active Skills from items (Ice Storm)


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
- Bot reacts to `!pob <pastebin (not raw!) link>` in all configured channels on the invited server.
### Showcase
![](https://cdn.discordapp.com/attachments/418758449954947076/419161884139454477/unknown.png)

