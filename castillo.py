#Librerías para interactuar con la API de Telegram
from telegram import *
from telegram.ext import *
from funciones import  *
from kb import *

def shop(update: Update, context: CallbackContext):
    text=str("¡Mira esto, hombre! Aquí tenemos suficientes armas para cazar un dragón, o para atacar un templo maldito!"
        +"\nEcha un vistazo a lo que quieras, y si algo te interesa, no dudes en preguntar!")
    reply_markup = InlineKeyboardMarkup(kb.kb("wtypes",("bsmith|na","null")))
    update.message.reply_text(
                                text=text,
                                reply_markup = reply_markup,
                                parse_mode=ParseMode.HTML
                            )
    return

def shopcat(update: Update, context: CallbackContext):
    global TiendaDB
    user = update.callback_query.from_user
    data = json.loads(update.callback_query.data)
    Juagador = PlayerDB[str(user.id)]
    weapons = False
    
    if(len(Juagador["bolso_arm"]) >= 15):
        text = "\n<b>Tienes lleno el inventario!!!</b>"
        reply_markup = None
        
    else:
        text="<b>Aquí, algunas mercancías:</b>\n"
        for w in list(set(TiendaDB.keys())):
            if(int(w) < 100):
                # print(str(TiendaDB[w]["g_type"]))
                if(TiendaDB[w]["g_type"] == data["d1"]):
                    text+="\n\n<b>{name}</b> ".format(name=TiendaDB[w]["nombre"],id=TiendaDB[w]["id"])
                    if(TiendaDB[w]["atributos"]["ataque"] > 0):
                        text+="<b>+{actaque}</b>⚔️".format(actaque=TiendaDB[w]["atributos"]["ataque"])
                    if(TiendaDB[w]["atributos"]["defensa"] > 0):
                        text+="<b>+{defensa}</b>🛡".format(defensa=TiendaDB[w]["atributos"]["defensa"])
                    if(TiendaDB[w]["tier"] == 1):
                        text+="\nRequerido: 📕"
                    text+="\n{precio}💰 \n/buy_{id}".format(precio=TiendaDB[w]["precio"],id=w)
                    weapons = True

        if(weapons == False):
            text += "\n<b>((Vacio))</b>"        
        
        reply_markup = InlineKeyboardMarkup(kb.kb("wtypes",("bsmith|na","null")))
            
    context.bot.edit_message_text(
                            text=text,
                            chat_id=user.id,
                            message_id=update.callback_query.message.message_id,
                            reply_markup = reply_markup,
                            parse_mode=ParseMode.HTML
                        )
    return

def buy(update: Update, context: CallbackContext):
    global PlayerDB
    user = update.message.from_user
    player = PlayerDB[str(user.id)]
    weapon = update.message.text.replace("/buy_","")
    try: 
        if(weapon not in player["bolso_arm"]):
            if(int(player["oro"]) >= int(TiendaDB[weapon]["precio"])):            
                # player["bolso_arm"].append(weapon)
                Newcompra(user=user.id,items=weapon)        
                wps = player["bolso_arm"]
                oro = str(int(PlayerDB[str(user.id)]["oro"]) - int(TiendaDB[weapon]["precio"]))
                upload(player=str(user.id),concept=("bolso_arm","oro"),value=(wps,oro))
                text = "Ja, ja! Este <b>{weapon}</b> te queda muy bien, amigo! \nUtilizar sabiamente!".format(weapon = TiendaDB[weapon]["nombre"])
            else:
                text = "Lo siento amigo, pero parece que no puedes permitirte este artículo."
        
            update.message.reply_text(
                                        text=text,
                                        parse_mode=ParseMode.HTML
                                    )
    except Exception as e:
            error(update,e)
    else:
        return
    return

def Newcompra(user,items):
    global PlayerDB,TiendaDB
    Jugador = PlayerDB[str(user)]
    
    info = {
            "id": TiendaDB[items]["id"],
            "estatus": 0,
            "nombre": TiendaDB[items]["nombre"],
            "historia": TiendaDB[items]["historia"],
            "tipo": TiendaDB[items]["tipo"],
            "g_type": TiendaDB[items]["g_type"],
            "dual": TiendaDB[items]["dual"],
            "peso": TiendaDB[items]["peso"],
            "tier": TiendaDB[items]["tier"],
            "envolver": TiendaDB[items]["envolver"],
            "evento_item": TiendaDB[items]["evento_item"],
            "fabricable": TiendaDB[items]["fabricable"],
            "intercanbio": TiendaDB[items]["intercanbio"],
            "precio": TiendaDB[items]["precio"],
            "venta": TiendaDB[items]["venta"],
            "atributos": {
                "ataque": TiendaDB[items]["atributos"]["ataque"],
                "defensa": TiendaDB[items]["atributos"]["defensa"],
                "mana": TiendaDB[items]["atributos"]["mana"],
                "habilidad": TiendaDB[items]["atributos"]["habilidad"],
                "nivel": TiendaDB[items]["atributos"]["nivel"],
                "reforsado": {
                    "1": {
                        "nivel": 1,
                        "ataque": 0,
                        "ataque_total": 0
                    },
                    "2": {
                        "nivel": 2,
                        "ataque": 0,
                        "ataque_total": 0
                    },
                    "3": {
                        "nivel": 3,
                        "ataque": 0,
                        "ataque_total": 0
                    },
                    "4": {
                        "nivel": 4,
                        "ataque": 0,
                        "ataque_total": 0
                    }
                    }
                }
            }
    
    Jugador["bolso_arm"].append(info)
    
    return

def winfo(update: Update, context: CallbackContext):
    global TiendaDB
    try:
        weapon = TiendaDB[update.message.text.replace("/info_","")]
        #print(str(weapon))
        text = str(
            "<b>⚜️ {name} ⚜️</b>".format(name=weapon["nombre"])
            +"\n\n<i>“{lore}”</i>\n".format(lore = weapon["historia"])
            +"\n"+"\t"*4+" Ataque: <code>{atk}</code>".format(atk = str(int(weapon["atributos"]["ataque"])))
            +"\n"+"\t"*4+" Defensa: <code>{df}</code>".format(df = str(int(weapon["atributos"]["defensa"])))
            # +"\n"+"\t"*4+" Defensa: <code>{df}</code>".format(df = str(int(weapon["atributos"]["nivel"])))
            # +"\n"+"\t"*4+" Peso: <code>{spe}</code>".format(spe=str(int(weapon["peso"])))
            # # +"\n"+"\t"*4+" Doble Mano: <code>{dual}</code>".format(dual= ("Si" if(weapon["dual"] == True) else "No"))
            # +"\n"+"\t"*4+" Tipo: <code>{g_type}</code>".format(g_type=weapon["tipo_g"].title())
            # +"\n"+"\t"*4+" Clase: <code>{type}</code>".format(type=weapon["tipo"].title())
        )
    except KeyError:
        text = "<code>[SIN INFORMACIÓN]</code>"
    update.message.reply_text(
                                text=text,
                                parse_mode=ParseMode.HTML
                            )

    return


def castillo(update: Update, context: CallbackContext):
    global PlayerDB
    user = update.message.from_user
    player = PlayerDB[str(user.id)]  
    level = player["level"] 
    hora = time.strftime("%H")
    text="El Castillo \n"   
        
    if(hora == "00"):
        text+="🌤Mañana"
    elif (hora == "01"):
        text+="🌞Día"
    elif (hora == "02"):
        text+="🌞Día"
    elif (hora == "03"):
        text+= "⛅️Tarde"
    elif (hora == "04"):
        text+= "⛅️Tarde"
    elif (hora == "05"):
        text+="🌙Noche"
    elif (hora == "06"):
        text+="🌙Noche"
    elif(hora == "07"):
        text+="🌤Mañana"
    elif(hora == "08"):
        text+="🌤Mañana"
    elif (hora == "09"):
        text+="🌞Día"
    elif (hora == "10"):
        text+="🌞Día"
    elif (hora == "11"):
        text+= "⛅️Tarde"
    elif (hora == "12"):
        text+= "⛅️Tarde"  
    elif (hora == "13"):
        text+="🌙Noche"
    elif (hora == "14"):
        text+="🌙Noche"
    elif(hora == "15"):
        text+="🌤Mañana"
    elif(hora == "16"):
        text+="🌤Mañana"
    elif (hora == "17"):
        text+="🌞Día"
    elif (hora == "18"):
        text+="🌞Día"
    elif (hora == "19"):
        text+= "⛅️Tarde"
    elif (hora == "20"):
        text+= "⛅️Tarde"
    elif (hora == 21):
        text+="🌙Noche"
    elif (hora == "22"):
        text+="🌙Noche"
    elif(hora == "23"):
        text+="🌤Mañana"
        
    # text+="[-→-]"
    text+="\n\n💬Castle Chat del castillo: "
    text+="\nLos demás: /otros"
    text+="\n\n🍺La taberna abre por la noche"

    reply_markup = ReplyKeyboardMarkup(kb.castillo_kb(level),resize_keyboard=True)

    update.message.reply_text(
        text=text,
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML
    )
    return 

def mesa_trabajo(update: Update, context: CallbackContext):
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

def taberna(update: Update, context: CallbackContext):
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

def subastas(update: Update, context: CallbackContext):
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

def inetercambio(update: Update, context: CallbackContext):
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

def diamantes(update: Update, context: CallbackContext):
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

def vender(update: Update, context: CallbackContext):
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

def casa_pet(update: Update, context: CallbackContext):
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

def get_mascotas(update: Update, context: CallbackContext):
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

def refugio(update: Update, context: CallbackContext):
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

def bodega(update: Update, context: CallbackContext):
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

def dados(update: Update, context: CallbackContext):
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

def dice(update: Update, context: CallbackContext):
    query = update.callback_query
    data = json.loads(query.data)
    d1 = rng(1,6)
    d2 = rng(1,6)
    dir = "/utils/dice"
    Dices = [ "⚀", "⚁", "⚂", "⚃", "⚄", "⚅" ]
    D1 = Dices[d1-1]
    D2 = Dices[d2-1]
    add = ""
    if(d1+d2 == 7):
        add = " ¡¡Dados!!"
    text = "{} tiró los dados, y...\nLos dados muestran {}({}) y {}({})...\n<b>{} conseguir {}{}!</b>\n\n".format(
                                    query.from_user.first_name,
                                    D1,d1,
                                    D2,d2,
                                    query.from_user.first_name,
                                    d1+d2,
                                    add
                                    )
    ##print(text)
    context.bot.edit_message_text(
                            text=text,
                            inline_message_id=query.inline_message_id,
                            parse_mode=ParseMode.HTML
                        )
    return

def taller(update: Update, context: CallbackContext):
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

def craf(update: Update, context: CallbackContext):
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

def formulas(update: Update, context: CallbackContext):
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

def envolver(update: Update, context: CallbackContext):
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
