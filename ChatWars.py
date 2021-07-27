#Librerías para interactuar con la API de Telegram
from telegram import *
from telegram.ext import *
categories = ["dagas","espadas","desafilados",
            "arcos","cascos","armaduras",
            "guantes","botas","escudos"]
from funciones import *
from batallas import *
from duelos import *
from registro import *
from ChatWars import *
from castillo import *
from misiones import *
from clan import *
from stock import *
from heroe import *
from tiempo import *



def start(update: Update, context: CallbackContext):
    query = update.message.from_user
    text = """Te acercas y ves un cartel en la puerta:\n
            < i > Discúlpenos, por el momento esta bajo mantenimiento...
            <s>(cosas aleatorias pueden suceder debido a la física cuántica.)</s>
            Estaremos de negocios en un par de días...</me>
            \n"""
    update.message.reply_text(
                                text,
                                reply_markup = None,
                                parse_mode=ParseMode.HTML
                            )

    return



def main():
    global updater
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('start', register),
            MessageHandler(Filters.regex("^(⚔️Atacar)$"), ata_castillo),
            MessageHandler(Filters.regex("^(🛡Defender)$"), def_castillo),            
            MessageHandler(Filters.regex("^(🗺Misiones)$"), misiones),
            MessageHandler(Filters.regex("^(🏅Yo)$"), me),            
            MessageHandler(Filters.regex("^(💬)$"), cominicacion),            
            MessageHandler(Filters.regex("^(🏰Castillo)$"), castillo),
            MessageHandler(Filters.regex("^(⚒Taller)$"), taller),
            MessageHandler(Filters.regex("^(⚒Mesa de trabajo)$"), mesa_trabajo),
            MessageHandler(Filters.regex("^(⚒Artesanía)$"), craf),
            MessageHandler(Filters.regex("^(📖Fórmula)$"), formulas),
            MessageHandler(Filters.regex("^(🏷Envolver)$"), envolver),
                        
            MessageHandler(Filters.regex("^(🍺Taberna)$"), taberna),
            MessageHandler(Filters.regex("^(🛎Subastas)$"), subastas),
            MessageHandler(Filters.regex("^(⚖️Instercambios)$"), inetercambio),
            MessageHandler(Filters.regex("^(🏚Tienda)$"), shop),
            MessageHandler(Filters.regex("^(💎Lujo)$"), diamantes),
            MessageHandler(Filters.regex("^(💰Vender)$"), vender),
            MessageHandler(Filters.regex("^(🐾Casa de fieras)$"), casa_pet),
            MessageHandler(Filters.regex("^(🎟Consigue una mascota)$"), get_mascotas),
            MessageHandler(Filters.regex("^(💁Refugio)$"), refugio),
            MessageHandler(Filters.regex("^(⚰️Bodega)$"), bodega),            
            
            MessageHandler(Filters.regex("^(👥Clanes)$"), clan),
            MessageHandler(Filters.regex("^(📦Almacen)$"), alam_clan),
            MessageHandler(Filters.regex("^(📋Lista)$"), lista_clan),
            MessageHandler(Filters.regex("^(ℹ️Otros)$"), otros_clan),
            MessageHandler(Filters.regex("^(🤝Alianza)$"), alianza_clan),
            MessageHandler(Filters.regex("^(🏕Misiones)$"), misiones_clan),
            
            MessageHandler(Filters.regex("/inv"), inventario),
            MessageHandler(Filters.regex("🎒Bolso"), inventario),
            MessageHandler(Filters.regex("📦Recursos"), recursos),
            MessageHandler(Filters.regex("🗃Varios"), varios),
            MessageHandler(Filters.regex("⚗️Alquimia"), alquimia),
            MessageHandler(Filters.regex("⚒Elaboración"), elaboracion),
            MessageHandler(Filters.regex("🏷Equipo"), equipo_en),      
            MessageHandler(Filters.regex("^(🎲Dados)$"), dados),
            MessageHandler(Filters.regex(r"^\/info_\d+$"), winfo),
            MessageHandler(Filters.regex("/tiempo"), tiempo),
            MessageHandler(Filters.regex("/heroe"), heroe),
            MessageHandler(Filters.regex(r"^\/on_\d+$"), equip),
            MessageHandler(Filters.regex(r"^\/off_\d+$"), equipoff),
            MessageHandler(Filters.regex(r"^\/buy_\d+$"), buy),
            MessageHandler(Filters.regex("^(/r)$"), reload),
            CommandHandler('reload', reload),
            MessageHandler(Filters.text,register)
            ],

        states={
            # ME: []

            #BR: [MessageHandler(Filters.regex("^(👥 Talk)$"), connect)],

            # DC: [MessageHandler(Filters.regex("^(↩️Dejar)$"), register)],

            # BS: [],

            # L7: [MessageHandler(Filters.regex("^(↩️Dejar)$"), register)],

            # HELP: [MessageHandler(Filters.regex("^(📝🏅Yo)$"), helpinfo),
            #     MessageHandler(Filters.regex("^(📝🍻Cerveza)$"), helpinfo),
            #     MessageHandler(Filters.regex("^(📝⚔️Duelo)$"), helpinfo),
            #     MessageHandler(Filters.regex("^(📝🏰Castillo)$"), helpinfo),
            #     MessageHandler(Filters.regex("^(📝🎲Dados)$"), helpinfo)],
            },

        fallbacks=[MessageHandler(Filters.regex("^(❌Cancelar)$"), register),
                   MessageHandler(Filters.regex("^(↩️Volver)$"), register),
                   CommandHandler("reload", reload)]
    )
    updater.dispatcher.add_handler(conv_handler)
    updater.dispatcher.add_handler(CallbackQueryHandler(queryHandler))
    updater.dispatcher.add_handler(InlineQueryHandler(inlinequery,pass_user_data=True, pass_chat_data=True))
    updater.user_sig_handler = lastrestart
    updater.start_polling(poll_interval = 0.1,clean = True,read_latency=1.0)

    updater.idle()
    return

if __name__ == '__main__':
    main()
