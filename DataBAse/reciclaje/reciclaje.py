def help(update: Update, context: CallbackContext):
    text='¿En qué puedo ayudarle, viajero?'
    IKB = KeyboardButton
    reply_markup = ReplyKeyboardMarkup(
        [
            [
                IKB("📝🎫"),
                IKB("📝🍻Cerveza"),
            ],
            [
                IKB("📝⚔️Duelo"),
                IKB("📝🎲Dados")
            ],
            [
                IKB("📝⚒🏰Castillo"),
                IKB("↩️Volver")
            ]
        ],
        resize_keyboard=True,
    )

    update.message.reply_text(
        text=text,
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML
    )
    return HELP

def helpinfo(update: Update, context: CallbackContext):
    choice = update.message.text
    reply_markup = None
    if(choice == "📝🏅Yo"):
        text = str("<i>Bueno, cada viajero tiene una 🏅Tarjeta de viajero, ahí es donde"
            +"mantenga un registro de todo su progreso y su información básica. Allí"
            +"también puede ver todo su equipo de propiedad, y desde allí se puede gestionar y"
            +"cámbialo de una manera que se adapte mejor a tu estilo de combate.</i>")
    elif(choice == "📝🍻Cerveza"):
        text = str("<i>Dime, viajero, ¿qué crees que sería una Taberna sin una buena Beer cerveza para servir?\n"
            +"Sí, de eso se trata todo esto, beber cerveza, hacer amigos y eso... Cuando bebes, "
            +"tienes la oportunidad de conocer gente nueva, bueno, solo si quieres hablar con ellos... "
            +"A los viajeros generalmente les gusta ver caras conocidas dondequiera que vayan, y qué mejor manera de hacerlo "
            +"posible, si no hacer un nuevo amigo primero?"
            +"\nAsí que, si quieres, no dudes en hablar con alguien nuevo... Quién sabe? Tal vez su próxima aventura está esperando junto con una nueva cara?</i>"
            +"\n\n<code>ADVERTENCIA: Pulsando sobre </code>🍻Cerveza<code> se te ofrecerá hablar con otra persona, si el matchmaking encuentra a alguien."
            +" Si ambos aceptan, su nombre de usuario será compartido con otra persona. Tener eso en mente!</code>")
    elif(choice == "📝⚔️Duelo"):
        text = str("<i>¡Ajá! Por lo tanto, usted está interesado en el combate, ¿eh?... Si es así, usted es libre de utilizar el ⚔️Duelo."
            +" Como dije antes, puedes desafiar a un extraño aleatorio desde aquí, o puedes desafiar a un amigo a través de un mensaje en línea en cualquier ventana de chat."
            +"\nTodo lo que tienes que hacer es escribir:</i>\n\n@Torre_RPGBot + <code>espacio</code>\n\n <i>y se te dará la opción de ⚔️Duelo con cualquier amigo."
            +" Solo ten en cuenta que jugar con cualquier persona no registrada no tiene ningún efecto en las estadísticas de tu personaje, como el dinero, la experiencia o la gloria</i>")
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(text="¡Inténtalo! ⚔️",switch_inline_query="")]])
    elif(choice == "📝⚒🏰Castillo"):
        text = str("<i>¿Quién? Ah, sí! El tipo que vende y forja armas al lado de la corte de duelo! Es un ⚒🏰Castillo."
            +"\n¡Si necesitas equipo, él es el hombre! Él tiene muchas armas en su stock, también, forja armas personalizadas, "
            +"perfecto para aquellos que quieren un arma de la firma de la que los bardos pueden contar en los cuentos épicos!</i>")
    elif(choice == "📝🎲Dados"):
        text = str("<i>¿Te sientes afortunado? Trate de tener una ronda en las mesas de juego. Pagas 10, y obtienes 20 a cambio, fácil, ¿no?"
            +"\nSolo tienes que conseguir un número más alto que tu oponente en los dados, y ganarás el partido. Pero si los dados suman 7, "
            +"¡ganarás automáticamente el partido! Simple. \nBien... A menos que haya un empate. En ese caso, solo se contarán los dados más altos."
            +"\n\nTambién puedes jugar con amigos, o darle a los dados cualquier otro uso que quieras. Igual que los duelos, puede llamar a los dados a través de un mensaje en línea:"
            +"</i>\n\n@Torre_RPGBot + <code>espacio</code>\n\nY presiona Dice Dados en la lista.\n\n<i>¡Así de fácil!"
            +"</i>")
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(text="¡Inténtalo! 🎲",switch_inline_query="")]])

    update.message.reply_text(text=text,parse_mode=ParseMode.HTML,reply_markup=reply_markup)
    return

def luckyseven(update: Update, context: CallbackContext):
    text='Las mesas de juego están vacías, nadie quiere probar suerte por ahora...\nIntenta volver en otro momento.'
    IKB = KeyboardButton
    reply_markup = ReplyKeyboardMarkup(
        [
            [
                IKB("↩️Dejar")
            ]
        ],
        resize_keyboard=True,
    )

    update.message.reply_text(
        text=text,
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML
    )
    return 

def forge(update: Update, context: CallbackContext):
    text='Lo siento amigo, no puedo hacer nada sin mis herramientas... Al menos que quieras usar un palillo como estoque, ja ja!'
    update.message.reply_text(text=text)
    return

def duellingcourt(update: Update, context: CallbackContext):
    text='La corte de duelo parece vacía ahora...\n¡Tal vez si trajeras a un amigo, ambos podrían practicar un rato!'
    IKB = KeyboardButton
    reply_markup = ReplyKeyboardMarkup(
        [
            [
                IKB("↩️Dejar")
            ]
        ],
        resize_keyboard=True,
    )

    update.message.reply_text(
        text=text,
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML
    )
    return 

def beer(update: Update, context: CallbackContext):
    text="Te sentaste y disfrutaste de una cerveza fría y espumosa... Desafortunadamente, el tabern parece vacío por ahora.\nTal vez más tarde vendrá más gente.\n\nPero no te preocupes, la casa invita a esta ronda! 🍻🍻🍻"
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


# heroe - Su perfil de resumen
# alm - Almacén de recursos básicos
# inv - Mostrar equipo (equipado y en bolsa)
# varios - Almacén de artículos diversos
# intercambios - Sus ofertas de intercambio activas
# clase - Distribución de habilidades elegidas personalmente
# top - Resumen de la clasificación de todos los jugadores
# worldtop - Resumen global del castillo
# guildtop - Resumen de la clasificación de todos los Clanes
# tiempo - Tiempo del juego
# promo - Invitacion de amigos
# ayuda - Guía del juego
# terminos - Reglas


manana = "🌤"
    "Thead = 01"
    "Stick = 02"
    "Pelt = 03"
    "Bone = 04"
    "Coal = 05"
    "Cloth = 09"
    "Powder = 07"
    "Silver Ore = 10"
    "Bone Powder = 21"
    "Rope = 31"
    "Lvl Alto"
    "Bauxite = 11"
    "Metal Plate = 33"
    mediodia = "🌞"
    "Thead = 01"
    "Pelt = 03"
    "Bone = 04"
    "Powder = 07"
    "Cloth = 09"
    "Leather = 20"
    "String = 22"
    "Coke = 23"
    "Lvl Alto"
    "Bauxite = 11"
    tarde = "⛅️"
    "Thead = 01"
    "Stick = 02"
    "Pelt = 03"
    "Bone = 04"
    "Coal = 05"
    "Powder = 07"
    "Cloth = 09"
    "Leather = 20"    
    "Bone Powder = 21"
    "String = 22"
    "Coke = 23"
    noche = "🌙"
    "Thead = 01"
    "Stick = 02"
    "Pelt = 03"
    "Coal = 05"
    "Charcoal = 06"
    "Powder = 07"
    "Iron Ore = 08"
    "Magic Stone = 13"
    "String = 22"
    "Coke = 23"


def shop_apagado(update: Update, context: CallbackContext):
    text = str("¡Mira esto, hombre! Aquí tenemos suficientes armas para cazar un dragón, o para atacar un templo maldito!"
               + "\nEcha un vistazo a lo que quieras, y si algo te interesa, no dudes en preguntar!")
    reply_markup = InlineKeyboardMarkup(kb.kb("wtypes", ("bsmith|na", "null")))
    update.message.reply_text(
        text=text,
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML
    )
    return

def shopcat_apagado(update: Update, context: CallbackContext):
    global TiendaDB
    user = update.callback_query.from_user
    data = json.loads(update.callback_query.data)
    Juagador = PlayerDB[str(user.id)]
    weapons = False

    if(len(Juagador["bolso_arm"]) >= 15):
        text = "\n<b>Tienes lleno el inventario!!!</b>"
        reply_markup = None

    else:
        text = "<b>Aquí, algunas mercancías:</b>\n"
        for w in list(sorted(TiendaDB.keys())):
            # if(int(w < 100):
                # print(str(TiendaDB[w]["g_type"]))
                if(TiendaDB[w]["g_type"] == data["d1"]):
                    text += "\n\n<b>{name}</b> ".format( name=TiendaDB[w]["nombre"], id=TiendaDB[w]["id"])
                    if(TiendaDB[w]["atributos"]["ataque"] > 0):
                        text += "<b>+{actaque}</b>⚔️".format(actaque=TiendaDB[w]["atributos"]["ataque"])
                    if(TiendaDB[w]["atributos"]["defensa"] > 0):
                        text += "<b>+{defensa}</b>🛡".format(defensa=TiendaDB[w]["atributos"]["defensa"])
                    if(TiendaDB[w]["tier"] == 1):
                        text += "\nRequerido: 📕"
                    text += "\n{precio}💰 \n/buy_{id}".format(precio=TiendaDB[w]["precio"], id=w)
                    weapons = True

        if(weapons == False):
            text += "\n<b>((Vacio))</b>"

        reply_markup = InlineKeyboardMarkup(
            kb.kb("wtypes", ("bsmith|na", "null")))

    context.bot.edit_message_text(
        text=text,
        chat_id=user.id,
        message_id=update.callback_query.message.message_id,
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML
    )
    return
