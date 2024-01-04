import asyncio

from asyncio import sleep
from telethon import events
from telethon.errors import ChatAdminRequiredError, UserAdminInvalidError
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights, ChannelParticipantsAdmins

from Giyu import telethn, OWNER_ID, CO_OWNER_ID, FLAMES, THUNDERS, WINDS

BANNED_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True,
)


UNBAN_RIGHTS = ChatBannedRights(
    until_date=None,
    send_messages=None,
    send_media=None,
    send_stickers=None,
    send_gifs=None,
    send_games=None,
    send_inline=None,
    embed_links=None,
)

SLAYERS = [OWNER_ID, CO_OWNER_ID] + FLAMES + THUNDERS + WINDS

async def is_administrator(user_id: int, message):
    admin = False
    async for user in telethn.iter_participants(
        message.chat_id, filter=ChannelParticipantsAdmins
    ):
        if user_id == user.id or user_id in SLAYERS:
            admin = True
            break
    return admin


@telethn.on(events.NewMessage(pattern="^[!/]demons ?(.*)"))
async def rm_deletedacc(show):
    con = show.pattern_match.group(1).lower()
    del_u = 0
    del_status = "**Group clean, didn't find any demons (deleted account).**"
    if con != "clean":
        kontol = await show.reply("`Searching demons (deleted account)...`")
        async for user in show.client.iter_participants(show.chat_id):
            if user.deleted:
                del_u += 1
                await sleep(1)
        if del_u > 0:
            del_status = (
                f"**Founding** `{del_u}` **Deleted account /demons On this group,"
                "\nClean it with command** `/demons clean`"
            )
        return await kontol.edit(del_status)
    chat = await show.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        return await show.reply("**Sorry you're not admin!**")
    memek = await show.reply("`Deleting deleted account...`")
    del_u = 0
    del_a = 0
    async for user in telethn.iter_participants(show.chat_id):
        if user.deleted:
            try:
                await show.client(
                    EditBannedRequest(show.chat_id, user.id, BANNED_RIGHTS)
                )
            except ChatAdminRequiredError:
                return await show.edit("`Not have a banned rights on this group`")
            except UserAdminInvalidError:
                del_u -= 1
                del_a += 1
            await telethn(EditBannedRequest(show.chat_id, user.id, UNBAN_RIGHTS))
            del_u += 1
    if del_u > 0:
        del_status = f"**Cleaned** `{del_u}` **demons**"
    if del_a > 0:
        del_status = (
            f"**Cleaned** `{del_u}` **demons** "
            f"\n`{del_a}` **Admin villagers corpse not deleted.**"
        )
    await memek.edit(del_status)

__mod_name__ = "Demon"

