import asyncio
import time
from telethon import events
from Giyu import telethn
from Giyu.modules.helper_funcs.telethn.chatstatus import (
    can_delete_messages,
    user_is_admin,
)
from Giyu.modules.helper_funcs.alternate import typing_action


string = "HEHE i've eaten your text lmao ;)"

@typing_action
async def delete_messages(event):
    if event.from_id is None:
        return

    if (
        not await user_is_admin(
            user_id=event.sender_id,
            message=event,
        )
        and event.from_id not in [1087968824]
    ):
        await event.reply("Only Admins are allowed to give me texts to eat.")
        return

    if not await can_delete_messages(message=event):
        await event.reply("If i eat this, I'll be not able to disgest it :(")
        return

    message = await event.get_reply_message()
    if not message:
        await event.reply("What should i eat?")
        return
    chat = await event.get_input_chat()
    del_message = [message, event.message]
    await event.client.delete_messages(chat, del_message)
    await event.reply("that text was tastyyyyy yum yum😋😋.")
    
TASTE_HANDLER = delete_messages, events.NewMessage(pattern="^[!/]taste$")

telethn.add_event_handler(*TASTE_HANDLER)

__mod_name__ = "TEXT EATER"
__command_list__ = ["taste"]
__handlers__ = [TASTE_HANDLER]
