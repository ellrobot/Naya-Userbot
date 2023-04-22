# Ayra - UserBot
# Copyright (C) 2021-2022 senpai80
#
# This file is a part of < https://github.com/senpai80/Ayra/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/senpai80/Ayra/blob/main/LICENSE/>.
"""
✘ **Bantuan Untuk Notes**

๏ **Perintah:** `snote` <nama catatan><balas pesan>
◉ **Keterangan:** Tambahkan catatan .

๏ **Perintah:** `rnote` <nama catatan>
◉ **Keterangan:** Hapus catatan .

๏ **Perintah:** `notes`
◉ **Keterangan:** Daftar semua catatan.

◉ **Notes:** Bisa menggunakan media apapun serta menggunakan button.
◉ **Contoh:**
Kirim ke
[Dana|https://link.dana]
"""
import os

from telegraph import upload_file as uf
from telethon.utils import pack_bot_file_id

from .database.notesdb import *
from ._inline import something
from . import *

@ayra_cmd(pattern="snote( (.*)|$)")
async def an(e):
    wrd = (e.pattern_match.group(1).strip()).lower()
    wt = await e.get_reply_message()
    bahan = int(udB.get_key("LOG_CHANNEL"))
    user = e.sender_id
    if not (wt and wrd):
        return await e.eor(get_string("notes_1"), time=5)
    if "#" in wrd:
        wrd = wrd.replace("#", "")
    btn = format_btn(wt.buttons) if wt.buttons else None
    if wt and wt.media:
        wut = mediainfo(wt.media)
        if wut.startswith(("pic", "gif")):
            dl = await wt.download_media()
            variable = uf(dl)
            os.remove(dl)
            m = f"https://graph.org{variable[0]}"
        elif wut == "video":
            if wt.media.document.size > 8 * 1000 * 1000:
                return await e.eor(get_string("com_4"), time=5)
            dl = await wt.download_media()
            variable = uf(dl)
            os.remove(dl)
            m = f"https://graph.org{variable[0]}"
        else:
            m = pack_bot_file_id(wt.media)
        if wt.text:
            txt = wt.text
            if not btn:
                txt, btn = get_msg_button(wt.text)
            add_note(user, wrd, txt, m, btn)
        else:
            add_note(user, wrd, None, m, btn)
    else:
        txt = wt.text
        if not btn:
            txt, btn = get_msg_button(wt.text)
        add_note(user, wrd, txt, None, btn)
    await e.eor(get_string("notes_2").format(wrd))
    ayra_bot.add_handler(notes, events.NewMessage())


@ayra_cmd(pattern="rnote( (.*)|$)")
async def rn(e):
    wrd = (e.pattern_match.group(1).strip()).lower()
    user = e.sender_id
    if not wrd:
        return await e.eor(get_string("notes_3"), time=5)
    if wrd.startswith("#"):
        wrd = wrd.replace("#", "")
    rem_note(int(user), wrd)
    await e.eor(f"Selesai Catatan: `{wrd}` Dihapus.")


@ayra_cmd(pattern="notes")
async def lsnote(e):
    user = e.sender_id
    if x := list_note(user):
        sd = "**❏ Daftar Notes**\n"
        return await e.eor(sd + x)
    await e.eor("**Belum ada catatan**")


async def notes(e):
    user = e.sender_id
    xx = [z.replace("#", "") for z in e.text.lower().split() if z.startswith("#")]
    for word in xx:
        if k := get_notes(user, word):
            msg = k["msg"]
            media = k["media"]
            if k.get("button"):
                btn = create_tl_btn(k["button"])
                return await something(e, msg, media, btn)
            await e.client.send_message(
                e.chat_id, msg, file=media, reply_to=e.reply_to_msg_id or e.id
            )


if udB.get_key("NOTE"):
    ayra_bot.add_handler(notes, events.NewMessage())