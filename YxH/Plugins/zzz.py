# NEVER RENAME THIS FILE

from pyrogram import Client, filters

from .fw import cwf as fw_cwf
from .info_watcher import cwf as info_cwf
from .copx import cwf as copx_cwf

from .watchers import (
    info_watcher,
    fw_watcher,
    copx_watcher
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