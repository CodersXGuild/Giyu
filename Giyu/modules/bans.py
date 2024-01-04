import html
import requests

from time import sleep
from telegram import (
    ParseMode,
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from telegram import ParseMode, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import BadRequest
from telegram.ext import CallbackContext, CommandHandler, Filters, run_async, CallbackQueryHandler
from telegram.utils.helpers import mention_html
from typing import Optional, List
from telegram import TelegramError

from telegram.error import BadRequest
from Giyu import (
    FLAMES,
    LOGGER,
    OWNER_ID,
    CO_OWNER_ID,
    THUNDERS,
    WINDS,
    WATERS,
    dispatcher,
    TOKEN,
    BOT_USERNAME,
    SUPPORT_CHAT
) 
import Giyu.modules.sql.users_sql as sql
from Giyu.modules.helper_funcs.chat_status import dev_plus
from Giyu.modules.helper_funcs.filters import CustomFilters
from Giyu.modules.disable import DisableAbleCommandHandler
from Giyu.modules.helper_funcs.chat_status import (
    bot_admin,
    can_restrict,
    connection_status,
    is_user_admin,
    is_user_ban_protected,
    is_user_in_chat,
    user_admin_no_reply,
    user_admin,
    user_can_ban,
    can_delete,
)
from Giyu.modules.helper_funcs.extraction import extract_user_and_text
from Giyu.modules.helper_funcs.string_handling import extract_time
from Giyu.modules.log_channel import loggable, gloggable


@connection_status
@bot_admin
@can_restrict
@user_admin
@user_can_ban
@loggable
def ban(update: Update, context: CallbackContext) -> str:
    chat = update.effective_chat
    user = update.effective_user
    message = update.effective_message
    log_message = ""
    bot = context.bot
    args = context.args
    user_id, reason = extract_user_and_text(message, args)
    if not user_id:
        message.reply_text("I doubt that's a user.")
        return log_message

    # Channel Ban By https://t.me/x11fq
    if str(user_id).startswith('-100'):
        BAN_CHANNEL_INFO = bot.get_chat(user_id)
        BAN_CHANNEL_USERNAME = BAN_CHANNEL_INFO.username
        cbanbuttons = [
    [
         InlineKeyboardButton(
            text="Unban", callback_data=f"cunbaninlinebutton{user_id}",
        )
    ]
    ]

        linked_group_channel = bot.get_chat(chat.id)
        lgc_id = linked_group_channel.linked_chat_id
        if str(user_id) == str(lgc_id):
            return log_message
        BAN_CHAT_CHANNEL = f"https://api.telegram.org/bot{TOKEN}/banChatSenderChat?chat_id={update.message.chat.id}&sender_chat_id={user_id}"
        respond = requests.post(BAN_CHAT_CHANNEL)
        if respond.status_code == 200:
            cbanreply = f'''
<code>🚫</code> <b>Ban Event</b>
<code>•</code> <b>Chat:</b> @{BAN_CHANNEL_USERNAME}'''
            if reason:
                cbanreply += f"\n<code>•</code> <b>Reason:</b> <code>{reason}</code>"
                bot.sendMessage(chat.id, cbanreply, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(cbanbuttons))
                return log_message
            else:
                bot.sendMessage(chat.id, cbanreply, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(cbanbuttons))
                return log_message
    try:
        member = chat.get_member(user_id)
    except BadRequest as excp:
        if excp.message != "User not found":
            raise
        message.reply_text("Can't seem to find this person.")
        return log_message
    if user_id == bot.id:
        message.reply_text("Oh yeah, ban myself, noob!")
        return log_message

    if is_user_ban_protected(chat, user_id, member) and user not in FLAMES:
        
        if user_id == OWNER_ID:
            message.reply_text("Trying to put me against my creator huh ? I'm not gonna ban him")
        elif user_id in FLAMES:
            message.reply_text("I can't act against rengoku san")
        elif user_id in THUNDERS:
            message.reply_text(
                "Thunder breathers are ban immune"
            )
        elif user_id in WINDS:
            message.reply_text(
                "Wind breathers are ban immune"
            )
        elif user_id in WATERS:
            message.reply_text(
                "Water breathers can't be ban."
            )
            
        else:
            message.reply_text("This user has immunity and cannot be banned.")
        return log_message
    if message.text.startswith("/s"):
        silent = True
        if not can_delete(chat, context.bot.id):
            return ""
    elif message.text.startswith("/d"):
        dban = True
        if not can_delete(chat, context.bot.id):
            message.reply_text(f"• Bot do not have the delete permission\n• Make sure @{BOT_USERNAME} is admin with all rights")
    else:
        silent = False
        dban = False
    log = (
        f"<b>{html.escape(chat.title)}:</b>\n"
        f"#{'S' if silent else ''}{'D' if dban else ''}BANNED\n"
        f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
        f"<b>User:</b> {mention_html(member.user.id, html.escape(member.user.first_name))}"
    )
    if reason:
        log += "\n<b>Reason:</b> {}".format(reason)

    try:
        chat.ban_member(user_id)

        if silent:
            if message.reply_to_message:
                message.reply_to_message.delete()
            message.delete()
            return log
        if dban:
            if message.reply_to_message:
                message.reply_to_message.delete()

        # bot.send_sticker(chat.id, BAN_STICKER)  # banhammer marie sticker
        reply = (
            f"<code>❕</code><b>Ban Event</b>\n"
            f"<code> </code><b>•  User:</b> {mention_html(member.user.id, html.escape(member.user.first_name))}"
        )
        if reason:
            reply += f"\n<code> </code><b>•  Reason:</b> \n{html.escape(reason)}" 
        bot.sendMessage(
            chat.id,
            reply,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="🔄  Unban", callback_data=f"unbanb_unban={user_id}"
                        ),
                        InlineKeyboardButton(text="🗑️  Delete", callback_data="unbanb_del"),
                    ]
                ]
            ),
            parse_mode=ParseMode.HTML,
        )
        return log
       
    except BadRequest as excp:
        if excp.message == "Reply message not found":
            # Do not reply
            if silent:
                return log
            message.reply_text("Banned!\n")
            return log
        else:
            LOGGER.warning(update)
            LOGGER.exception(
                "ERROR banning user %s in chat %s (%s) due to %s",
                user_id,
                chat.title,
                chat.id,
                excp.message,
            )
            message.reply_text("Uhm...that didn't work...")

    return log_message



@connection_status
@bot_admin
@can_restrict
@user_admin
@user_can_ban
@loggable
def temp_ban(update: Update, context: CallbackContext) -> str:
    chat = update.effective_chat
    user = update.effective_user
    message = update.effective_message
    log_message = ""
    bot, args = context.bot, context.args
    user_id, reason = extract_user_and_text(message, args)

    if not user_id:
        message.reply_text("I doubt that's a user.")
        return log_message

    try:
        member = chat.get_member(user_id)
    except BadRequest as excp:
        if excp.message != "User not found":
            raise
        message.reply_text("I can't seem to find this user.")
        return log_message
    if user_id == bot.id:
        message.reply_text("I'm not gonna BAN myself!!")
        return log_message

    if is_user_ban_protected(chat, user_id, member):
        message.reply_text("I don't feel like it.")
        return log_message

    if not reason:
        message.reply_text("You haven't specified a time to ban this user for!")
        return log_message

    split_reason = reason.split(None, 1)

    time_val = split_reason[0].lower()
    reason = split_reason[1] if len(split_reason) > 1 else ""
    bantime = extract_time(message, time_val)

    if not bantime:
        return log_message

    log = (
        f"<b>{html.escape(chat.title)}:</b>\n"
        "#TEMP BANNED\n"
        f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
        f"<b>User:</b> {mention_html(member.user.id, html.escape(member.user.first_name))}\n"
        f"<b>Time:</b> {time_val}"
    )
    if reason:
        log += "\n<b>Reason:</b> {}".format(reason)

    try:
        chat.kick_member(user_id, until_date=bantime)
        # bot.send_sticker(chat.id, BAN_STICKER)  # banhammer marie sticker
        bot.sendMessage(
            chat.id,
            reply_msg,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="🔄  Unban", callback_data=f"unbanb_unban={user_id}"
                        ),
                        InlineKeyboardButton(text="🗑️  Delete", callback_data="unbanb_del"),
                    ]
                ]
            ),
            parse_mode=ParseMode.HTML,
        )
        return log
    except BadRequest as excp:
        if excp.message == "Reply message not found":
            # Do not reply
            message.reply_text(
                f"Banned! User will be banned for {time_val}."
            )
            return log
        else:
            LOGGER.warning(update)
            LOGGER.exception(
                "ERROR banning user %s in chat %s (%s) due to %s",
                user_id,
                chat.title,
                chat.id,
                excp.message,
            )
            message.reply_text("Well damn, I can't ban that user.")

    return log_message



@connection_status
@bot_admin
@can_restrict
@user_admin
@user_can_ban
@loggable
def punch(update: Update, context: CallbackContext) -> str:
    chat = update.effective_chat
    user = update.effective_user
    message = update.effective_message
    log_message = ""
    bot, args = context.bot, context.args
    user_id, reason = extract_user_and_text(message, args)

    if not user_id:
        message.reply_text("I doubt that's a user.")
        return log_message

    try:
        member = chat.get_member(user_id)
    except BadRequest as excp:
        if excp.message != "User not found":
            raise

        message.reply_text("I can't seem to find this user.")
        return log_message
    if user_id == bot.id:
        message.reply_text("Yeahhh I'm not gonna do that.")
        return log_message

    if is_user_ban_protected(chat, user_id):
        message.reply_text("I really wish I could headbutt this user....")
        return log_message

    res = chat.unban_member(user_id)  # unban on current user = kick
    if res:
        # bot.send_sticker(chat.id, BAN_STICKER)  # banhammer marie sticker
        bot.sendMessage(
            chat.id,
            f"One Punched! {mention_html(member.user.id, html.escape(member.user.first_name))}.",
            parse_mode=ParseMode.HTML,
        )
        log = (
            f"<b>{html.escape(chat.title)}:</b>\n"
            f"#KICKED\n"
            f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
            f"<b>User:</b> {mention_html(member.user.id, html.escape(member.user.first_name))}"
        )
        if reason:
            log += f"\n<b>Reason:</b> {reason}"

        return log

    else:
        message.reply_text("Well damn, I can't punch that user.")

    return log_message


@connection_status
@bot_admin
@can_restrict
@user_admin
@user_can_ban
@loggable
def kick(update: Update, context: CallbackContext) -> str:
    chat = update.effective_chat
    user = update.effective_user
    message = update.effective_message
    log_message = ""
    bot, args = context.bot, context.args
    user_id, reason = extract_user_and_text(message, args)

    if not user_id:
        message.reply_text("I doubt that's a user.")
        return log_message

    try:
        member = chat.get_member(user_id)
    except BadRequest as excp:
        if excp.message != "User not found":
            raise

        message.reply_text("I can't seem to find this user.")
        return log_message
    if user_id == bot.id:
        message.reply_text("Yeahhh I'm not gonna do that.")
        return log_message

    if is_user_ban_protected(chat, user_id):
        message.reply_text("I really wish I could Kick this user....")
        return log_message

    res = chat.unban_member(user_id)  # unban on current user = kick
    if res:
        # bot.send_sticker(chat.id, BAN_STICKER)  # banhammer marie sticker
        bot.sendMessage(
            chat.id,
            f"Kicked! {mention_html(member.user.id, html.escape(member.user.first_name))}.",
            parse_mode=ParseMode.HTML,
        )
        log = (
            f"<b>{html.escape(chat.title)}:</b>\n"
            f"#KICKED\n"
            f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
            f"<b>User:</b> {mention_html(member.user.id, html.escape(member.user.first_name))}"
        )
        if reason:
            log += f"\n<b>Reason:</b> {reason}"

        return log

    else:
        message.reply_text("Well damn, I can't Kick that user.")

    return log_message


@bot_admin
@can_restrict
def lmao(update: Update, context: CallbackContext):
    user_id = update.effective_message.from_user.id
    if is_user_admin(update.effective_chat, user_id):
        update.effective_message.reply_text("I wish I could... but you're an admin.")
        return

    res = update.effective_chat.unban_member(user_id)  # unban on current user = kick
    if res:
        update.effective_message.reply_text("Farewell (╯︵╰,)")
    else:
        update.effective_message.reply_text("Huh? I can't gave you death :/")

@bot_admin
@can_restrict
def banme(update: Update, context: CallbackContext):
    user_id = update.effective_message.from_user.id
    if is_user_admin(update.effective_chat, user_id):
        update.effective_message.reply_text("I wish I could... but you're an admin.")
        return

    res = update.effective_chat.kick_member(user_id)  # ban the user
    if res:
        update.effective_message.reply_text("Done Banned!")
    else:
        update.effective_message.reply_text("Huh? I can't :/")
    
@bot_admin
@can_restrict
def kickme(update: Update, context: CallbackContext):
    user_id = update.effective_message.from_user.id
    if is_user_admin(update.effective_chat, user_id):
        update.effective_message.reply_text("I wish I could... but you're an admin.")
        return

    res = update.effective_chat.unban_member(user_id)  # unban on current user = kick
    if res:
        update.effective_message.reply_text("Done Kicked!")
    else:
        update.effective_message.reply_text("Huh? I can't :/")



@connection_status
@bot_admin
@can_restrict
@user_admin
@user_can_ban
@loggable
def unban(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    log_message = ""
    bot, args = context.bot, context.args
    user_id, reason = extract_user_and_text(message, args)

    if not user_id:
        message.reply_text("I doubt that's a user.")
        return log_message
    if str(user_id).startswith('-100'):
        UNBAN_CHANNEL_INFO = bot.get_chat(user_id)
        UNBAN_CHAT_CHANNEL = f"https://api.telegram.org/bot{TOKEN}/unbanChatSenderChat?chat_id={update.message.chat.id}&sender_chat_id={user_id}"
        respond = requests.post(UNBAN_CHAT_CHANNEL)
        if respond.status_code == 200:
            UNBANNED_CHANNEL_LINK = UNBAN_CHANNEL_INFO.username
            update.message.reply_text(f'''
<b>Successfully Unbanned </b>
<b>Chat:</b> @{UNBANNED_CHANNEL_LINK}
                ''', parse_mode=ParseMode.HTML)
            return log_message
        else:
            update.message.reply_text(f'''
There was an error occured during this unban. please report this to @{SUPPORT_CHAT}.
• Error: `{respond}`
                ''')
            return log_message
    try:
        member = chat.get_member(user_id)
    except BadRequest as excp:
        if excp.message != "User not found":
            raise
        message.reply_text("I can't seem to find this user.")
        return log_message
    if user_id == bot.id:
        message.reply_text("How would I unban myself if I wasn't here...?")
        return log_message

    if is_user_in_chat(chat, user_id):
        message.reply_text("Isn't this person already here??")
        return log_message

    chat.unban_member(user_id)
    message.reply_text("Yep, this user can join!")

    log = (
        f"<b>{html.escape(chat.title)}:</b>\n"
        f"#UNBANNED\n"
        f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
        f"<b>User:</b> {mention_html(member.user.id, html.escape(member.user.first_name))}"
    )
    if reason:
        log += f"\n<b>Reason:</b> {reason}"

    return log 

@dev_plus
def snipe(update: Update, context: CallbackContext):
    args = context.args
    bot = context.bot
    try:
        chat_id = str(args[0])
        del args[0]
    except TypeError:
        update.effective_message.reply_text("Please give me a chat to echo to!")
    to_send = " ".join(args)
    if len(to_send) >= 2:
        try:
            bot.sendMessage(int(chat_id), str(to_send))
        except TelegramError:
            LOGGER.warning("Couldn't send to group %s", str(chat_id))
            update.effective_message.reply_text(
                "Couldn't send the message. Perhaps I'm not part of that group?"
            )


@connection_status
@bot_admin
@can_restrict
@user_admin_no_reply
@user_can_ban
@loggable
def unbanb_btn(update: Update, context: CallbackContext) -> str:
    bot = context.bot
    query = update.callback_query
    chat = update.effective_chat
    user = update.effective_user
    if query.data != "unbanb_del":
        splitter = query.data.split("=")
        query_match = splitter[0]
        if query_match == "unbanb_unban":
            user_id = splitter[1]
            if not is_user_admin(chat, int(user.id)):
                bot.answer_callback_query(
                    query.id,
                    text="⚠️ You don't have enough rights to unmute people",
                    show_alert=True,
                )
                return ""
            log_message = ""
            try:
                member = chat.get_member(user_id)
            except BadRequest:
                pass
            chat.unban_member(user_id)
            query.message.edit_text(
                f"{member.user.first_name} [{member.user.id}] Unbanned."
            )
            bot.answer_callback_query(query.id, text="Unbanned!")
            return (
                f"<b>{html.escape(chat.title)}:</b>\n"
                f"#UNBANNED\n"
                f"<b>Admin:</b> {mention_html(user.id, user.first_name)}\n"
                f"<b>User:</b> {mention_html(member.user.id, member.user.first_name)}"
            )

    else:
        if not is_user_admin(chat, int(user.id)):
            bot.answer_callback_query(
                query.id,
                text="⚠️ You don't have enough rights to delete this message.",
                show_alert=True,
            )
            return ""
        query.message.delete()
        bot.answer_callback_query(query.id, text="Deleted!")
        return "" 


__help__ = """
• /kickme*:* kicks the user who Used the command
• /suicide *:* punchs the user who Used the command
 Note: Both Are same
• /banme*:* Ban the user who used
*Admins only:*
• /ban <userhandle>*:* bans a user. (via handle, or reply)
• /sban <userhandle>*:* Silently ban a user. Deletes command, Replied message and doesn't reply. (via handle, or reply)
• /tban <userhandle> x(m/h/d)*:* bans a user for `x` time. (via handle, or reply). `m` = `minutes`, `h` = `hours`, `d` = `days`.
• /unban <userhandle>*:* unbans a user. (via handle, or reply)
• /headbutt <userhandle>*:* headbutt a user out of the group, (via handle, or reply)
• /kick <userhandle>*:* kicks a user out of the group, (via handle, or reply)
 *Admins only:*
• /mute <userhandle>*:* silences a user. Can also be used as a reply, muting the replied to user.
• /tmute <userhandle> x(m/h/d)*:* mutes a user for x time. (via handle, or reply). `m` = `minutes`, `h` = `hours`, `d` = `days`.
• /unmute <userhandle>*:* unmutes a user. Can also be used as a reply, muting the replied to user.
"""

BAN_HANDLER = CommandHandler(["ban", "sban"], ban, run_async=True)
BANME_HANDLER = DisableAbleCommandHandler("banme", banme, filters=Filters.chat_type.groups, run_async=True)
TEMPBAN_HANDLER = CommandHandler(["tban"], temp_ban, run_async=True)
PUNCH_HANDLER = CommandHandler("headbutt", punch, run_async=True)
UNBAN_HANDLER = CommandHandler("unban", unban, run_async=True)
SUICIDE_HANDLER = DisableAbleCommandHandler("suicide", lmao, filters=Filters.chat_type.groups, run_async=True)
KICK_HANDLER = CommandHandler("kick", kick, run_async=True)
KICKME_HANDLER = DisableAbleCommandHandler("kickme", kickme, filters=Filters.chat_type.groups, run_async=True)
UNBAN_BUTTON_HANDLER = CallbackQueryHandler(unbanb_btn, pattern=r"unbanb_")
SNIPE_HANDLER = CommandHandler("crowmsg", snipe, pass_args=True, filters=CustomFilters.thunders_filter, run_async=True)
dispatcher.add_handler(SNIPE_HANDLER)
dispatcher.add_handler(BAN_HANDLER)
dispatcher.add_handler(BANME_HANDLER)
dispatcher.add_handler(TEMPBAN_HANDLER)
dispatcher.add_handler(PUNCH_HANDLER)
dispatcher.add_handler(UNBAN_HANDLER)
dispatcher.add_handler(SUICIDE_HANDLER)
dispatcher.add_handler(KICK_HANDLER)
dispatcher.add_handler(UNBAN_BUTTON_HANDLER)
dispatcher.add_handler(KICKME_HANDLER)
__mod_name__ = "Ban/Mute"
__handlers__ = [
    BAN_HANDLER,
    TEMPBAN_HANDLER,
    PUNCH_HANDLER,
    UNBAN_HANDLER,
    SUICIDE_HANDLER,
    KICK_HANDLER,
    SNIPE_HANDLER,
    UNBAN_BUTTON_HANDLER,
    KICKME_HANDLER,
    BANME_HANDLER,
]
