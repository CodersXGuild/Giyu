import html
import json
import os
from typing import Optional

from Giyu import (
    FLAMES,
    OWNER_ID,
    CO_OWNER_ID,
    THUNDERS,
    SUPPORT_CHAT,
    WINDS,
    WATERS,
    BEASTS,
    dispatcher,
)
from Giyu.modules.helper_funcs.chat_status import (
    dev_plus,
    sudo_plus,
    whitelist_plus,
)
from Giyu.modules.helper_funcs.extraction import extract_user
from Giyu.modules.log_channel import gloggable
from telegram import ParseMode, TelegramError, Update
from telegram.ext import CallbackContext, CommandHandler
from telegram.utils.helpers import mention_html

ELEVATED_USERS_FILE = os.path.join(os.getcwd(), "Giyu/elevated_users.json")


def check_user_id(user_id: int, context: CallbackContext) -> Optional[str]:
    bot = context.bot
    if not user_id:
        reply = "That...is a chat! baka ka omae?"

    elif user_id == bot.id:
        reply = "This does not work that way."

    else:
        reply = None
    return reply


# This can serve as a deeplink example.
# disasters =
# """ Text here """

# do not async, not a handler
# def send_disasters(update):
#    update.effective_message.reply_text(
#        disasters, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)

### Deep link example ends


@dev_plus
@gloggable
def addthunder(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)
    rt = ""

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, "r") as infile:
        data = json.load(infile)

    if user_id in THUNDERS:
        message.reply_text("This member is already a the Thunder Breather")
        return ""

    if user_id in WINDS:
        rt += "Succesfully trained wind Breather to thunder Breather."
        data["winds"].remove(user_id)
        WINDS.remove(user_id)

    if user_id in BEASTS:
        rt += "Succesfully trained to beast breather to thunder breather"
        data["beasts"].remove(user_id)
        BEASTS.remove(user_id)

    data["thunders"].append(user_id)
    THUNDERS.append(user_id)

    with open(ELEVATED_USERS_FILE, "w") as outfile:
        json.dump(data, outfile, indent=4)

    update.effective_message.reply_text(
        rt
        + "\nSuccessfully trained {} to thunder breather".format(
            user_member.first_name,
        ),
    )

    log_message = (
        f"#WindBreather\n"
        f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
        f"<b>User:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
    )

    if chat.type != "private":
        log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

    return log_message


@sudo_plus
@gloggable
def addwind(
    update: Update,
    context: CallbackContext,
) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)
    rt = ""

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, "r") as infile:
        data = json.load(infile)

    if user_id in THUNDERS:
        rt += "Demote this thunder breather to wind breather"
        data["thunders"].remove(user_id)
        THUNDERS.remove(user_id)

    if user_id in WINDS:
        message.reply_text("This user is already wind breather.")
        return ""

    if user_id in BEASTS:
        rt += "Succesfully raised beast breather to wind breather"
        data["beasts"].remove(user_id)
        BEASTS.remove(user_id)

    data["winds"].append(user_id)
    WINDS.append(user_id)

    with open(ELEVATED_USERS_FILE, "w") as outfile:
        json.dump(data, outfile, indent=4)

    update.effective_message.reply_text(
        rt + f"\n{user_member.first_name} was trained as a wind breather!",
    )

    log_message = (
        f"#WindBreather\n"
        f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
        f"<b>User:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
    )

    if chat.type != "private":
        log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

    return log_message


@sudo_plus
@gloggable
def addbeast(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)
    rt = ""

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, "r") as infile:
        data = json.load(infile)

    if user_id in THUNDERS:
        rt += "This member is a thunder breather, Demoting to beast breather"
        data["thunders"].remove(user_id)
        THUNDERS.remove(user_id)

    if user_id in WINDS:
        rt += "This user is already a wind breather, Demoting to beast breather"
        data["winds"].remove(user_id)
        WINDS.remove(user_id)

    if user_id in BEASTS:
        message.reply_text("This user is already in beast breather")
        return ""

    data["beasts"].append(user_id)
    BEASTS.append(user_id)

    with open(ELEVATED_USERS_FILE, "w") as outfile:
        json.dump(data, outfile, indent=4)

    update.effective_message.reply_text(
        rt + f"\nSuccessfully trained {user_member.first_name} to be a  beast breather!",
    )

    log_message = (
        f"#BeastBreather\n"
        f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))} \n"
        f"<b>User:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
    )

    if chat.type != "private":
        log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

    return log_message


@sudo_plus
@gloggable
def addwater(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)
    rt = ""

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, "r") as infile:
        data = json.load(infile)

    if user_id in THUNDERS:
        rt += "This member is a thunder breather,Demoting to water breather"
        data["thunders"].remove(user_id)
        THUNDERS.remove(user_id)

    if user_id in WINDS:
        rt += "This user is already a wind breather, Demoting to water breather."
        data["winds"].remove(user_id)
        WINDS.remove(user_id)

    if user_id in BEASTS:
        rt += "This user is already a beast breather, Demoting to water breather"
        data["beasts"].remove(user_id)
        BEASTS.remove(user_id)

    if user_id in WATERS:
        message.reply_text("This user is already a water breaather.")
        return ""

    data["waters"].append(user_id)
    WATERS.append(user_id)

    with open(ELEVATED_USERS_FILE, "w") as outfile:
        json.dump(data, outfile, indent=4)

    update.effective_message.reply_text(
        rt + f"\nSuccessfully trained {user_member.first_name} for to be a water breather!",
    )

    log_message = (
        f"#WaterBreather\n"
        f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))} \n"
        f"<b>User:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
    )

    if chat.type != "private":
        log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

    return log_message


@dev_plus
@gloggable
def removethunder(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, "r") as infile:
        data = json.load(infile)

    if user_id in THUNDERS:
        message.reply_text("Requested DemonslayerCorps to demote this Breathe user to Civilian")
        THUNDERS.remove(user_id)
        data["thunders"].remove(user_id)

        with open(ELEVATED_USERS_FILE, "w") as outfile:
            json.dump(data, outfile, indent=4)

        log_message = (
            f"#DemoteThunder\n"
            f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
            f"<b>User:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
        )

        if chat.type != "private":
            log_message = "<b>{}:</b>\n".format(html.escape(chat.title)) + log_message

        return log_message
    message.reply_text("This user is not a Thunder Breather!")
    return ""


@sudo_plus
@gloggable
def removewind(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, "r") as infile:
        data = json.load(infile)

    if user_id in WINDS:
        message.reply_text("Requested DemonslayerCorps demote this Breathe user to Civilian")
        WINDS.remove(user_id)
        data["winds"].remove(user_id)

        with open(ELEVATED_USERS_FILE, "w") as outfile:
            json.dump(data, outfile, indent=4)

        log_message = (
            f"#DemoteWind\n"
            f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
            f"<b>User:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
        )

        if chat.type != "private":
            log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

        return log_message
    message.reply_text("This user is not a Captain!")
    return ""


@sudo_plus
@gloggable
def removebeast(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, "r") as infile:
        data = json.load(infile)

    if user_id in BEASTS:
        message.reply_text("Demoting to normal user")
        BEASTS.remove(user_id)
        data["beasts"].remove(user_id)

        with open(ELEVATED_USERS_FILE, "w") as outfile:
            json.dump(data, outfile, indent=4)

        log_message = (
            f"#DemoteBeast\n"
            f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
            f"<b>User:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
        )

        if chat.type != "private":
            log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

        return log_message
    message.reply_text("This user is not a Beast Breather!")
    return ""


@sudo_plus
@gloggable
def removewater(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, "r") as infile:
        data = json.load(infile)

    if user_id in WATERS:
        message.reply_text("Demoting to normal user")
        WATERS.remove(user_id)
        data["waters"].remove(user_id)

        with open(ELEVATED_USERS_FILE, "w") as outfile:
            json.dump(data, outfile, indent=4)

        log_message = (
            f"#DemoteWater\n"
            f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
            f"<b>User:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
        )

        if chat.type != "private":
            log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

        return log_message
    message.reply_text("This user is not a Water Breather!")
    return ""


@whitelist_plus
def beastslist(update: Update, context: CallbackContext):
    reply = "<b>Known Beast Breathers 🐗:</b>\n"
    m = update.effective_message.reply_text(
        "<code>Gathering intel..</code>",
        parse_mode=ParseMode.HTML,
    )
    bot = context.bot
    for each_user in BEASTS:
        user_id = int(each_user)
        try:
            user = bot.get_chat(user_id)

            reply += f"• {mention_html(user_id, html.escape(user.first_name))}\n"
        except TelegramError:
            pass
    m.edit_text(reply, parse_mode=ParseMode.HTML)


@whitelist_plus
def waterlist(update: Update, context: CallbackContext):
    reply = "<b>Known Water Breathers 🌊♂:</b>\n"
    m = update.effective_message.reply_text(
        "<code>Gathering intel..</code>",
        parse_mode=ParseMode.HTML,
    )
    bot = context.bot
    for each_user in WATERS:
        user_id = int(each_user)
        try:
            user = bot.get_chat(user_id)
            reply += f"• {mention_html(user_id, html.escape(user.first_name))}\n"
        except TelegramError:
            pass
    m.edit_text(reply, parse_mode=ParseMode.HTML)


@whitelist_plus
def windlist(update: Update, context: CallbackContext):
    bot = context.bot
    m = update.effective_message.reply_text(
        "<code>Gathering intel..</code>",
        parse_mode=ParseMode.HTML,
    )
    reply = "<b>Known Wind Breathers💨:</b>\n"
    for each_user in WINDS:
        user_id = int(each_user)
        try:
            user = bot.get_chat(user_id)
            reply += f"• {mention_html(user_id, html.escape(user.first_name))}\n"
        except TelegramError:
            pass
    m.edit_text(reply, parse_mode=ParseMode.HTML)


@whitelist_plus
def thunderlist(update: Update, context: CallbackContext):
    bot = context.bot
    m = update.effective_message.reply_text(
        "<code>Gathering intel..</code>",
        parse_mode=ParseMode.HTML,
    )
    true_sudo = list(set(THUNDERS) - set(FLAMES))
    reply = "<b>Known the Thunder Breathers ⚡:</b>\n"
    for each_user in true_sudo:
        user_id = int(each_user)
        try:
            user = bot.get_chat(user_id)
            reply += f"• {mention_html(user_id, html.escape(user.first_name))}\n"
        except TelegramError:
            pass
    m.edit_text(reply, parse_mode=ParseMode.HTML)


@whitelist_plus
def flamelist(update: Update, context: CallbackContext):
    bot = context.bot
    m = update.effective_message.reply_text(
        "<code>Gathering intel..</code>",
        parse_mode=ParseMode.HTML,
    )
    true_dev = list(set(FLAMES) - {OWNER_ID})
    reply = "<b>Known Flame Breathers🔥:</b>\n"
    for each_user in true_dev:
        user_id = int(each_user)
        try:
            user = bot.get_chat(user_id)
            reply += f"• {mention_html(user_id, html.escape(user.first_name))}\n"
        except TelegramError:
            pass
    m.edit_text(reply, parse_mode=ParseMode.HTML)


THUNDER_HANDLER = CommandHandler(("addthunder", "trainthunder"), addthunder, run_async=True)
WIND_HANDLER = CommandHandler(("addwind", "trainwind"), addwind, run_async=True)
WATER_HANDLER = CommandHandler(("addwater", "trainwater"), addwater, run_async=True)
BEASTS_HANDLER = CommandHandler(
    ("addbeast", "trainbeast"), addbeast, run_async=True
)
REMTHUNDER_HANDLER = CommandHandler(
    ("remthunder", "removethunder"), removethunder, run_async=True
)
REMWIND_HANDLER = CommandHandler(
    ("remwind", "removewind"), removewind, run_async=True
)
REMWATER_HANDLER = CommandHandler(("remwater", "removewater"), removewater, run_async=True)
REMBEAST_HANDLER = CommandHandler(
    ("rembeast", "removebeast"), removebeast, run_async=True
)
BEASTSLIST_HANDLER = CommandHandler(
    ["beastslist", "beastlist"], beastslist, run_async=True
)
WATERLIST_HANDLER = CommandHandler(["waterlist"], waterlist, run_async=True)
WINDLIST_HANDLER = CommandHandler(
    ["windlist"], windlist, run_async=True
)
THUNDERLIST_HANDLER = CommandHandler(["thunderlist"], thunderlist, run_async=True)
FLAMELIST_HANDLER = CommandHandler(["flamelist"], flamelist, run_async=True)

dispatcher.add_handler(THUNDER_HANDLER)
dispatcher.add_handler(WIND_HANDLER)
dispatcher.add_handler(WATER_HANDLER)
dispatcher.add_handler(BEASTSLIST_HANDLER)
dispatcher.add_handler(REMTHUNDER_HANDLER)
dispatcher.add_handler(REMWIND_HANDLER)
dispatcher.add_handler(REMWATER_HANDLER)
dispatcher.add_handler(REMBEAST_HANDLER)

dispatcher.add_handler(BEASTS_HANDLER)
dispatcher.add_handler(WATERLIST_HANDLER)
dispatcher.add_handler(WINDLIST_HANDLER)
dispatcher.add_handler(THUNDERLIST_HANDLER)
dispatcher.add_handler(FLAMELIST_HANDLER)

__mod_name__ = "Disasters"
__handlers__ = [
    THUNDER_HANDLER,
    WIND_HANDLER,
    WATER_HANDLER,
    BEASTSLIST_HANDLER,
    REMTHUNDER_HANDLER,
    REMWIND_HANDLER,
    REMWATER_HANDLER,
    BEASTS_HANDLER,
    REMBEAST_HANDLER,
    WATERLIST_HANDLER,
    WINDLIST_HANDLER,
    THUNDERLIST_HANDLER,
    FLAMELIST_HANDLER,
]
