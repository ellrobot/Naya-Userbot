# Ayra - UserBot
# Copyright (C) 2021-2022 senpai80
#
# This file is a part of < https://github.com/senpai80/Ayra/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/senpai80/Ayra/blob/main/LICENSE/>.
"""
✘ **Bantuan Untuk Pinterest**

๏ **Perintah:** `copy` <link>
◉ **Keterangan:** Colong media dari ch private.
"""
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.contacts import UnblockRequest
from telethon.tl.functions.messages import DeleteHistoryRequest

try:
    import cv2
except ImportError:
    cv2 = None

try:
    from htmlwebshot import WebShot
except ImportError:
    WebShot = None

from . import *
LOG_CHANNEL = udB.get_key("LOG_CHANNEL")


@ayra_cmd(pattern="copy(?: |$)(.*)")
async def copay(event):
    if xxnx := event.pattern_match.group(1):
        link = xxnx
    elif event.is_reply:
        link = await event.get_reply_message()
    else:
        return await eod(event, "`Berikan link tautan channel atau grup...`")

    xx = await eor(event, "`Processing...`")
    chat = "@Nyolongbang_bot"
    async with event.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=6152320759)
            )
            await event.client.send_message(chat, link)
            response = await response
        except YouBlockedUserError:
            await event.client(UnblockRequest(chat))
            await event.client.send_message(chat, link)
            response = await response
        if response.text.startswith("Forward"):
            await xx.edit("`Mengunggah...`")
        else:
            await xx.delete()
            await event.client.send_file(
                event.chat_id,
                response.message,
            )
            await event.client.send_read_acknowledge(conv.chat_id)
            await event.client(DeleteHistoryRequest(peer=chat, max_id=0))
            await xx.delete()


@ayra_cmd(pattern=r"curi(?: |$)(.*)")
async def pencuri(event):
    dia = await event.get_reply_message()
    botlog = LOG_CHANNEL
    xx = await event.eor("`...`", time=2)
    if not dia:
        return
    anjing = dia.text or None
    pap = await event.client.download_media(dia)
    try:
        await event.client.send_file(
             botlog,
             pap,
             caption="Pap nya...")
    except Exception as e:
        print(e)
