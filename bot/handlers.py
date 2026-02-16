from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import CallbackContext

from bot.database import db


def start_command(update: Update, context: CallbackContext):
    user = update.effective_user

    db.add_user(user_id=user.id, first_name=user.first_name)

    update.message.reply_text(
        text=f"Assalomu alaykum {user.first_name}!\n\nSmartphone Shop Botga xush kelibsiz!",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton("Telefonlar"), KeyboardButton("Haridlarim")]],
            resize_keyboard=True,
            one_time_keyboard=True,
        ),
    )


def text_router(update: Update, context: CallbackContext):
    text = update.message.text.strip().lower()

    if text == "telefonlar":
        send_smartphones_handler(update, context)
        return

    if text == "haridlarim":
        haridlarim_handler(update, context)
        return

    phone_detail_handler(update, context)


def haridlarim_handler(update: Update, context: CallbackContext):
    cart = context.user_data.get("cart", [])

    if not cart:
        update.message.reply_text("Savatchangiz bo'sh")
        return

    text = "Siz tanlagan telefonlar:\n"
    for i, item in enumerate(cart, start=1):
        text += f"{i}. {item}\n"

    update.message.reply_text(text)


def send_smartphones_handler(update: Update, context: CallbackContext):
    update.message.reply_text("Marhamat, brend nomini yozing")


def phone_detail_handler(update: Update, context: CallbackContext):
    text = update.message.text.strip().lower()

    data = db.read_database()
    phones = data.get("smartphones", {})

    found = False

    for phone in phones.values():
        if phone["brand"].lower() == text:
            found = True

            name = f"{phone['brand']} {phone['model']}"

            cart = context.user_data.get("cart", [])
            cart.append(name)
            context.user_data["cart"] = cart

            if phone["docs"]:
                doc_text = "Bor"
            else:
                doc_text = "Yo'q"

            message = (
                f"{name}\n"
                f"Narx: {phone['price']}\n"
                f"RAM: {phone['ram']} GB\n"
                f"Rang: {phone['color']}\n"
                f"Hujjat: {doc_text}"
            )

            update.message.reply_photo(photo=phone["image"], caption=message)

    if not found:
        update.message.reply_text("Bu brend bo'yicha telefon topilmadi")
