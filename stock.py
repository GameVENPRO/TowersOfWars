#Librerías para interactuar con la API de Telegram
from telegram import *
from telegram.ext import *


def recursos(update: Update, context: CallbackContext):
    text="No esta disponible"
    IKB = InlineKeyboardButton
    reply_markup = ReplyKeyboardMarkup(
        [
            [
                IKB("👥Hablar"),
                IKB("↩️Volver")
            ]
        ],
        resize_keyboard=True,
    )

    update.message.reply_text(
        text=text,
        reply_markup=None,
        parse_mode=ParseMode.HTML
    )
    return

def varios(update: Update, context: CallbackContext):
    text="No esta disponible"
    IKB = InlineKeyboardButton
    reply_markup = ReplyKeyboardMarkup(
        [
            [
                IKB("👥Hablar"),
                IKB("↩️Volver")
            ]
        ],
        resize_keyboard=True,
    )

    update.message.reply_text(
        text=text,
        reply_markup=None,
        parse_mode=ParseMode.HTML
    )
    return

def alquimia(update: Update, context: CallbackContext):
    text="No esta disponible"
    IKB = InlineKeyboardButton
    reply_markup = ReplyKeyboardMarkup(
        [
            [
                IKB("👥Hablar"),
                IKB("↩️Volver")
            ]
        ],
        resize_keyboard=True,
    )

    update.message.reply_text(
        text=text,
        reply_markup=None,
        parse_mode=ParseMode.HTML
    )
    return

def elaboracion(update: Update, context: CallbackContext):
    text="No esta disponible"
    IKB = InlineKeyboardButton
    reply_markup = ReplyKeyboardMarkup(
        [
            [
                IKB("👥Hablar"),
                IKB("↩️Volver")
            ]
        ],
        resize_keyboard=True,
    )

    update.message.reply_text(
        text=text,
        reply_markup=None,
        parse_mode=ParseMode.HTML
    )
    return

def equipo_en(update: Update, context: CallbackContext):
    text="No esta disponible"
    IKB = InlineKeyboardButton
    reply_markup = ReplyKeyboardMarkup(
        [
            [
                IKB("👥Hablar"),
                IKB("↩️Volver")
            ]
        ],
        resize_keyboard=True,
    )

    update.message.reply_text(
        text=text,
        reply_markup=None,
        parse_mode=ParseMode.HTML
    )
    return

