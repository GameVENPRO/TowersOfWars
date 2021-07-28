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