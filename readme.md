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

### Future Work
- Add support to adequately title the pob's (e.g. totem <main skill>, mine <main skill>)
- Add support for parsing unique items to add them into the gem links (e.g. soul mantle => main link + Spell Totem Lvl 20)
- Refine Offense output
- Customizable Layout (maybe)
- Start/Stop script: https://wolfpaulus.com/technology/pythonlauncher/
- Build.slots => Itemslot.item => Item
                    |<=> Skill
### How To Run
- Copy and rename `config.example.py`
  ```bash
  cp config.example.py config.py
  ```
- Edit the new `config.py`
    - replace token
    - add channels the bots should react to
- Run `discord_pob.py`

### Usage
- Bot reacts to `!pob <pastebin (not raw!) link>` in all configured channels on the invited server.
### Showcase
![](https://cdn.discordapp.com/attachments/418758449954947076/419161884139454477/unknown.png)

