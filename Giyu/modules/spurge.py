import asyncio
import time
from telethon import events

from Giyu import telethn
from Giyu.modules.helper_funcs.telethn.chatstatus import (
    can_delete_messages,
    user_is_admin,
)

async def purge_messages(event):
    start = time.perf_counter()
    if event.from_id is None:
        return

    if (
        not await user_is_admin(
            user_id=event.sender_id,
            message=event,
        )
        and event.from_id not in [1087968824]
    ):
        await event.reply("Only Admins are allowed to use this command")
        return

    reply_msg = await event.get_reply_message()
    if not reply_msg:
        await event.reply("Reply to a message to select where to start purging from.")
        return
    messages = []
    message_id = reply_msg.id
    delete_to = event.message.id

    messages.append(event.reply_to_msg_id)
    for msg_id in range(message_id, delete_to + 1):
        messages.append(msg_id)
        if len(messages) == 100:
            await event.client.delete_messages(event.chat_id, messages)
            messages = []
     
    try:
        await event.client.delete_messages(event.chat_id, messages)
    except:
        pass
    time_ = time.perf_counter() - start
    text = ""
    await event.respond(text, parse_mode="markdown")

SPURGE_HANDLER = purge_messages, events.NewMessage(pattern="^[!/.]spurge$")

telethn.add_event_handler(*SPURGE_HANDLER)

__command_list__ = ["spurge", ""]
__handlers__ = [SPURGE_HANDLER]

__mod_name__ = "Purges"
__help__ = """
Need to delete lots of messages? here are some cnd for your help (~‾▿‾)~!

•`/del` *:* deletes the message you replied to
•`/purge` *:* deletes all messages between this and the replied to message.
•`/purge` <integer X>*:* deletes the replied message, and X messages following it if replied to a message.
•`/spurge` *:* Same as purge, but doesnt send the final confirmation message.
"""
