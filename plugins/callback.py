

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import MessageNotModified
from pyrogram import Client, emoji
from utils import mp, playlist
from config import Config


HELP = """

<b>
Use /play <channel username>

**Common Commands**:

**/upload** Uploads current playing song as audio file.
**/help** Show help for commands
**/playlist** Shows the playlist.

**Admin Commands**:
**/skip** [n] ...  Skip current or n where n >= 2.
**/shuffle** Shuffle Playlist.
**/stop**  Stop playing.
**/radio** Start Radio.
**/stopradio** Stops Radio Stream.
**/clearplaylist** Clear the playlist.
**/pause** Pause playing.
**/resume** Resume playing.
**/mute**  Mute in VC.
**/unmute**  Unmute in VC.
**/restart**  Update and restarts the Bot.
"""



@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    admins = await mp.get_admins(Config.CHAT)
    if query.from_user.id not in admins and query.data != "help":
        await query.answer(
            "😒 Played Joji.mp3",
            show_alert=True
            )
        return
    else:
        await query.answer()
    if query.data == "replay":
        group_call = mp.group_call
        if not playlist:
            return
        group_call.restart_playout()
        if not playlist:
            pl = f"{emoji.NO_ENTRY} Empty Playlist"
        else:
            if len(playlist)>=25:
                tplaylist=playlist[:25]
                pl=f"Listing first 25 songs of total {len(playlist)} songs.\n"
                pl += f"{emoji.PLAY_BUTTON} **Playlist**:\n" + "\n".join([
                    f"**{i}**. **🎸{x[1]}**\n   👤**Requested by:** {x[4]}"
                    for i, x in enumerate(tplaylist)
                    ])
            else:
                pl = f"{emoji.PLAY_BUTTON} **Playlist**:\n" + "\n".join([
                    f"**{i}**. **🎸{x[1]}**\n   👤**Requested by:** {x[4]}\n"
                    for i, x in enumerate(playlist)
                ])
        try:
            await query.edit_message_text(
                    f"{pl}",
                    parse_mode="Markdown",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("🔄", callback_data="replay"),
                                InlineKeyboardButton("⏯", callback_data="pause"),
                                InlineKeyboardButton("⏩", callback_data="skip")
                            ],
                        ]
                    )
                )
        except MessageNotModified:
            pass

    elif query.data == "pause":
        if not playlist:
            return
        else:
            mp.group_call.pause_playout()
            if len(playlist)>=25:
                tplaylist=playlist[:25]
                pl=f"Listing first 25 songs of total {len(playlist)} songs.\n"
                pl += f"{emoji.PLAY_BUTTON} **Playlist**:\n" + "\n".join([
                    f"**{i}**. **🎸{x[1]}**\n   👤**Requested by:** {x[4]}"
                    for i, x in enumerate(tplaylist)
                    ])
            else:
                pl = f"{emoji.PLAY_BUTTON} **Playlist**:\n" + "\n".join([
                    f"**{i}**. **🎸{x[1]}**\n   👤**Requested by:** {x[4]}\n"
                    for i, x in enumerate(playlist)
                ])

        try:
            await query.edit_message_text(f"{emoji.PLAY_OR_PAUSE_BUTTON} Paused\n\n{pl},",
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("🔄", callback_data="replay"),
                            InlineKeyboardButton("⏯", callback_data="resume"),
                            InlineKeyboardButton("⏩", callback_data="skip")
                        ],
                    ]
                )
            )
        except MessageNotModified:
            pass
    
    elif query.data == "resume":   
        if not playlist:
            return
        else:
            mp.group_call.resume_playout()
            if len(playlist)>=25:
                tplaylist=playlist[:25]
                pl=f"Listing first 25 songs of total {len(playlist)} songs.\n"
                pl += f"{emoji.PLAY_BUTTON} **Playlist**:\n" + "\n".join([
                    f"**{i}**. **🎸{x[1]}**\n   👤**Requested by:** {x[4]}"
                    for i, x in enumerate(tplaylist)
                    ])
            else:
                pl = f"{emoji.PLAY_BUTTON} **Playlist**:\n" + "\n".join([
                    f"**{i}**. **🎸{x[1]}**\n   👤**Requested by:** {x[4]}\n"
                    for i, x in enumerate(playlist)
                ])

        try:
            await query.edit_message_text(f"{emoji.PLAY_OR_PAUSE_BUTTON} Resumed\n\n{pl}",
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("🔄", callback_data="replay"),
                            InlineKeyboardButton("⏯", callback_data="pause"),
                            InlineKeyboardButton("⏩", callback_data="skip")
                        ],
                    ]
                )
            )
        except MessageNotModified:
            pass

    elif query.data=="skip":   
        if not playlist:
            return
        else:
            await mp.skip_current_playing()
            if len(playlist)>=25:
                tplaylist=playlist[:25]
                pl=f"Listing first 25 songs of total {len(playlist)} songs.\n"
                pl += f"{emoji.PLAY_BUTTON} **Playlist**:\n" + "\n".join([
                    f"**{i}**. **🎸{x[1]}**\n   👤**Requested by:** {x[4]}"
                    for i, x in enumerate(tplaylist)
                ])
            else:
                pl = f"{emoji.PLAY_BUTTON} **Playlist**:\n" + "\n".join([
                    f"**{i}**. **🎸{x[1]}**\n   👤**Requested by:** {x[4]}\n"
                    for i, x in enumerate(playlist)
                ])

        try:
            await query.edit_message_text(f"{emoji.PLAY_OR_PAUSE_BUTTON} Skipped\n\n{pl}",
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("🔄", callback_data="replay"),
                            InlineKeyboardButton("⏯", callback_data="pause"),
                            InlineKeyboardButton("⏩", callback_data="skip")
                        ],
                    ]
                )
            )
        except MessageNotModified:
            pass

    elif query.data=="help":
        buttons = [
            [
                InlineKeyboardButton('⚙️ Update Channel', url='t.me/mwkBoTs'),
                InlineKeyboardButton('Developer', url='t.me/shamilnelli'),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(buttons)

        try:
            await query.edit_message_text(
                HELP,
                reply_markup=reply_markup

            )
        except MessageNotModified:
            pass

