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

REMNAWAVE_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IklhbVN1cGVyQWRtaW4iLCJ1dWlkIjoiNTI3OWQ0YzItMDAyZC00NjM5LWFhYzEtNWI1NzQ4MWJhMGZiIiwicm9sZSI6IkFETUlOIiwiaWF0IjoxNzc3MjQ4Njc3LCJleHAiOjE3NzcyOTE4Nzd9.B1G_hWyCIzanrKItl4ZetgCqzY5bFPsaj5j2uhKTKkU"

import requests
from datetime import datetime, timedelta

REMNAWAVE_URL = "https://admin.akajhwbsn.ru"

def get_user(username):
    url = f"{REMNAWAVE_URL}/api/users?search={username}"

    headers = {
        "Authorization": f"Bearer {REMNAWAVE_TOKEN}"
    }

    r = requests.get(url, headers=headers)

    if r.status_code == 200:
        data = r.json()
        if data.get("response"):
            return data["response"][0]  # берём первого
    return None

def create_user(username, days):
    url = f"{REMNAWAVE_URL}/api/users"

    headers = {
        "Authorization": f"Bearer {REMNAWAVE_TOKEN}",
        "Content-Type": "application/json"
    }

    expire = (datetime.utcnow() + timedelta(days=days)).isoformat() + "Z"

    payload = {
        "username": username,
        "status": "ACTIVE",
        "trafficLimitBytes": 0,
        "trafficLimitStrategy": "NO_RESET",
        "expireAt": expire,
        "description": f"tg:{username}",
        "activeInternalSquads": ["fbc3bb64-442f-49bc-a653-0aa12ee7a3cf"]
    }

    r = requests.post(url, json=payload, headers=headers)

    if r.status_code in (200, 201):
        return r.json()["response"]
    else:
        print(r.text)
        return None

def update_user(uuid, days):
    url = f"{REMNAWAVE_URL}/api/users/{uuid}"

    headers = {
        "Authorization": f"Bearer {REMNAWAVE_TOKEN}",
        "Content-Type": "application/json"
    }

    expire = (datetime.utcnow() + timedelta(days=days)).isoformat() + "Z"

    payload = {
        "expireAt": expire
    }

    r = requests.patch(url, json=payload, headers=headers)

    return r.status_code == 200

async def handle_buy(query, days):
    tg_id = str(query.from_user.id)

    user = get_user(tg_id)

    # если пользователь уже есть → продлеваем
    if user:
        update_user(user["uuid"], days)
        sub_url = user["subscriptionUrl"]

        text = "🔄 Подписка продлена!\n\n"

    else:
        user = create_user(tg_id, days)

        if not user:
            await query.message.edit_text("❌ Ошибка создания")
            return

        sub_url = user["subscriptionUrl"]
        text = "✅ Доступ выдан!\n\n"

    await query.message.edit_text(
        text + f"🔗 Ваша подписка:\n<code>{sub_url}</code>",
        parse_mode="HTML",
        reply_markup=main_menu()
    )
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))

app.run_polling()
