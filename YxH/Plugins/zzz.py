# NEVER RENAME THIS FILE

from pyrogram import Client, filters

from .fw import cwf as fw_cwf
from .info_watcher import cwf as info_cwf
from .copx import cwf as copx_cwf
from .scramble import catch_scramble_response
from .wordle import cwf as wordle_cwf

from .watchers import (
    info_watcher,
    fw_watcher,
    copx_watcher,
    scramble_watcher,
    wordle_watcher
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

@Client.on_message(filters.group, group=wordle_watcher)
async def wordle_command(_, m, u):
    await wordle_cwf(_, m)

@Client.on_message(filters.group, group=info_watcher)
async def info(_, m):
    await info_cwf(_, m)
