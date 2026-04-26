from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import random


def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💰 Тарифы", callback_data="plans")],
        [InlineKeyboardButton("🛒 Купить доступ", callback_data="buy")]
    ])


TOKEN = "8700188117:AAHme6Wm5xrosrU_TFQyBciI72V8HRgDpg0"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Добро пожаловать в VPN Store\nВыберите действие:",
        reply_markup=main_menu()
    )


def plans_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🥉 Basic - 1$", callback_data="buy_basic")],
        [InlineKeyboardButton("🥈 Pro - 5$", callback_data="buy_pro")],
        [InlineKeyboardButton("🔙 Назад", callback_data="back")]
    ])


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "plans":
        await query.message.edit_text("💰 Выберите тариф:", reply_markup=plans_menu())

    elif data == "buy":
        await query.message.edit_text("🛒 Выберите тариф:", reply_markup=plans_menu())

    elif data == "buy_basic":
        key = "BASIC-" + str(random.randint(10000, 99999))
        await query.message.edit_text(
            f"✅ Оплата (тест)\n\nВаш доступ:\n🔑 {key}",
            reply_markup=back_menu()
        )

    elif data == "buy_pro":
        key = "PRO-" + str(random.randint(10000, 99999))
        await query.message.edit_text(
            f"✅ Оплата (тест)\n\nВаш доступ:\n🔑 {key}",
            reply_markup=back_menu()
        )

    elif data == "back":
        await query.message.edit_text(
            "👋 Добро пожаловать в VPN Store\nВыберите действие:",
            reply_markup=main_menu()
        )


def back_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Назад", callback_data="back")]
    ])


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))

app.run_polling()
