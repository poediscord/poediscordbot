# PoB Parsing Bot for Discord
*Written in Python 3.6*

Utilized libraries & Inspiration:
- [discord.py](https://github.com/Rapptz/discord.py)
- [PoBPreviewBott](https://github.com/aggixx/PoBPreviewBot)
- [LiftDiscord Bot](https://github.com/andreandersen/LiftDiscord/)

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