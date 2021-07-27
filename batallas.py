#Librerías para interactuar con la API de Telegram
from telegram import *
from telegram.ext import *
from kb import *

def ata_castillo(update: Update, context: CallbackContext):
    text='No esta Disponible'
    update.message.reply_text(text=text)
    return

def def_castillo(update: Update, context: CallbackContext):
    text='No esta Disponible'
    update.message.reply_text(text=text)
    return

def cominicacion(update: Update, context: CallbackContext):     
    text="📯Comunicación con otros castillos\n Únete a @TorreDeDiosRPG y empieza a hablar con los ciudadanos de los siete castillos.\n\n"
    text+="📢Nuevas Noticias del juego\n Únase a @TorreDeDiosRPG para mantenerse al día con las últimas actualizaciones.\n\n"
    text+="📊Ranking\n Jugadores: /top\n Castillos: /worldtop\n Gremios: /guildtop\n"
    text+="✏️Nombre del juego\n Para cambiar tu nombre en el bot del juego, escribe / name seguido de tu nuevo nombre\n"
    text+="Ejemplo:\n /nombre Jon Snow\n\n 🚹Masculino. Género en el juego. \n"
    text+="No hay manera de cambiar los textos y menciones en el mundo del juego severo. Pero puede cambiar todos los gráficos disponibles.\n"
    text+="Comando: /gender_change\n"
    text+="Advertencia! Solo el primer intento es gratis. Siguiente le costará 💎15"

    IKB = KeyboardButton
    reply_markup = ReplyKeyboardMarkup(kb.kb("start"),resize_keyboard=True)

    update.message.reply_text(
        text=text,
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML
    )
    return 

