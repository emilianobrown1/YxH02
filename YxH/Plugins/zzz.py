# NEVER RENAME THIS FILE

from pyrogram import Client, filters

from .fw import cwf as fw_cwf
from .info_watcher import cwf as info_cwf
from .copx import cwf as copx_cwf
from .scramble import catch_scramble_response  
from .couple_messages import handle_couple_messages
from .power import track_activity

from .watchers import (
    info_watcher,
    fw_watcher,
    copx_watcher,
    scramble_watcher,
    couple_message_watcher,
    track_activity_watcher
)

@Client.on_message(filters.group, group=fw_watcher)
async def fw(_, m):
    await fw_cwf(_, m)

@Client.on_message(filters.group, group=copx_watcher)
async def copx(_, m):
    await copx_cwf(_, m)

@Client.on_message(filters.group, group=info_watcher)
async def info(_, m):
    await info_cwf(_, m)
    
@Client.on_message((filters.text & filters.group), group=scramble_watcher)
async def scramble(_, m):
    await catch_scramble_response(_, m)

@Client.on_message(filters.group, group=couple_message_watcher)
async def couple_messages(_, m):
    await handle_couple_messages(_, m)


@Client.on_message(filters.group, group=info_watcher)
async def info(_, m):
    await info_cwf(_, m)

@Client.on_message(filters.group, group=tracker_activity_watcher)
async def track_activity_watcher(_, m):
    await track_activity(_, m)


    
