from typing import Optional, Union, NewType
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum, auto
import discord
from gino import Gino

db = Gino()

UserId = NewType('UserId', int)

class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    discord_id = db.Column(db.Integer)
    display_name = db.Column(db.String)

class Guild(db.Model):
    __tablename__ = "guild"

    id = db.Column(db.Integer, primary_key=True)
    discord_id = db.Column(db.Integer)
    display_name = db.Column(db.String)

class Channel(db.Model):
    __tablename__ = "channel"

    id = db.Column(db.Integer, primary_key=True)
    discord_id = db.Column(db.Integer)
    display_name = db.Column(db.String)

    guild_id = db.Column(None, db.ForeignKey('guild.id'))

class Role(db.Model):
    __tablename__ = "role"

    id = db.Column(db.Integer, primary_key=True)
    discord_id = db.Column(db.Integer)
    display_name = db.Column(db.String)

    guild_id = db.Column(None, db.ForeignKey('guild.id'))

class Rapsheet(db.Model):
    __tablename__ = "rapsheet"

    id = db.Column(db.Integer, primary_key=True)
    guild_id = db.Column(None, db.ForeignKey('guild.id'))
    user_id = db.Column(None, db.ForeignKey('user.id'))
    creator_id = db.Column(None, db.ForeignKey('user.id'))

    type = db.Column(db.String)
    reason = db.Column(db.String)
    added = db.Column(db.DateTime)
    expires = db.Column(db.DateTime)

class Job(db.Model):
    __tablename__ = "job"

    id = db.Column(db.Integer, primary_key=True)

    # initiating
    guild_id = db.Column(None, db.ForeignKey('guild.id'))
    user_id = db.Column(None, db.ForeignKey('user.id'))

    task = db.Column(db.String)
    stage = db.Column(db.String)
    started = db.Column(db.DateTime)
    ended = db.Column(db.DateTime)
    data = db.Column(db.Json)


class InfractionTypes(Enum):
    Ban = "ban"
    Mute = "mute"
    Warn = "warn"
    Note = "note"

class DiscordEvents(Enum):
    Join = auto()