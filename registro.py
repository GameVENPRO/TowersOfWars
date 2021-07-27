#Librerías para interactuar con la API de Telegram
from telegram import *
from telegram.ext import *
from funciones import  *
from kb import *

def register(update: Update, context: CallbackContext):
    user = update.message.from_user    
    IKB = InlineKeyboardButton
    if(str(user.id) in list(PlayerDB.keys())):
        Juagador = PlayerDB[str(user.id)]
        level = Juagador["level"] 
        welcometext = "Bienvenido de vuelta, {name}! \n¿Cómo puedo servirle hoy?".format(name=user.first_name)
        reply_markup = ReplyKeyboardMarkup(kb.ini_kb(level),resize_keyboard=True)


        update.message.reply_text(
            text=welcometext,
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )
        threading.Thread(target=updateUser,args=(user,)).start()
        return ConversationHandler.END
    else:
        text = "Elige el castillo al que jurarás lealtad 🗡"  
        id_stiker= "CAACAgEAAxkBAAEB7BdgOA8VimAAATplEjtXp0IRxejpASoAAiwBAAJ9BsBFdTpwxjEI5z0eBA"   
           
        
        reply_markup = InlineKeyboardMarkup([
                                                [
                                                    IKB("🐉Escama de dragon",callback_data = '{'+"\"op\":\"reg|gen\",\"d1\":\"{d1}\",\"d2\":\"{d2}\"".format(d1='dragon',d2=str(user.id))+'}'),
                                                    IKB("🌑Luz lunar",callback_data = '{'+"\"op\":\"reg|gen\",\"d1\":\"{d1}\",\"d2\":\"{d2}\"".format(d1='luna',d2=str(user.id))+'}')
                                                ],
                                                [
                                                    IKB("🥔Papa",callback_data = '{'+"\"op\":\"reg|gen\",\"d1\":\"{d1}\",\"d2\":\"{d2}\"".format(d1='papa',d2=str(user.id))+'}'),
                                                    IKB("🐺Manada de lobos",callback_data = '{'+"\"op\":\"reg|gen\",\"d1\":\"{d1}\",\"d2\":\"{d2}\"".format(d1='lobos',d2=str(user.id))+'}')
                                                ],
                                                [   IKB("🦌Cuerno de ciervo",callback_data = '{'+"\"op\":\"reg|gen\",\"d1\":\"{d1}\",\"d2\":\"{d2}\"".format(d1='ciervos',d2=str(user.id))+'}'),
                                                    IKB("🦅Nido alto",callback_data = '{'+"\"op\":\"reg|gen\",\"d1\":\"{d1}\",\"d2\":\"{d2}\"".format(d1='agilas',d2=str(user.id))+'}'),                                            
                                                ],
                                                [   IKB("🦈Dientes de Tiburón",callback_data = '{'+"\"op\":\"reg|gen\",\"d1\":\"{d1}\",\"d2\":\"{d2}\"".format(d1='tiburon',d2=str(user.id))+'}')
                                                ]
                                            ] 
                                          )
        
        context.bot.send_sticker(chat_id=user.id, sticker=id_stiker)
        update.message.reply_text(text, reply_markup = reply_markup, parse_mode=ParseMode.HTML)

        return

def reg(update: Update, context: CallbackContext):
    query = update.callback_query
    data = json.loads(query.data)
    option,next = data["op"].split("|")
    user = query.from_user
    level = 1
    if(next == 'gen'):      
        if(data["d1"] == "dragon"):
            castillo = "Escamas de dragon"
            flag = "🐉"
        if(data["d1"] == "luna"):
            castillo = "Luz lunar"
            flag = "🌑"
        if(data["d1"] == "lobos"):
            castillo = "Manadas de Lobos"
            flag = "🐺"
        if(data["d1"] == "ciervos"):
            castillo = "Cuernos de Ciervo"
            flag = "🦌"
        if(data["d1"] == "agilas"):
            castillo = "Nido Alto" 
            flag = "🦅"                                  
        if(data["d1"] == "tiburon"):
            castillo = "Dientes de Tiburón"
            flag = "🦈"
        if(data["d1"] == "papa"):
            castillo = "Papa"
            flag = "🥔"
 
            
        text = str('🎉Usted se une a los valientes guerreros del {fla}{castle}.\n\n'.format(fla=flag,castle=castillo)
             +"Date prisa y únete al chat de nuestros jugadores: @TorreDeDiosRPG")
        
        try:
            context.bot.edit_message_reply_markup(
                chat_id=user.id,
                message_id=query.message.message_id,
                #inline_message_id=query.inline_message_id,
                reply_markup=None
            ) 
            reply_markup = ReplyKeyboardMarkup(kb.ini_kb(level),resize_keyboard=True)
            context.bot.send_message(
                chat_id=user.id,
                text=text,
                parse_mode=ParseMode.HTML,
                reply_markup=reply_markup)
            threading.Thread(target=newUser,args=(user,data["d1"],)).start()
        except Exception as e:
            error(update,e)
    return

def newUser(user,pron):
    global PlayerDB
    castillo = ''
    flag = ''
    Castillos = pron
    if(Castillos == "dragon"):
        castillo = "Escamas de dragon"
        flag = "🐉"
    if(Castillos == "luna"):
        castillo = "Luz lunar"
        flag = "🌑"
    if(Castillos == "lobos"):
        castillo = "Manadas de Lobos"
        flag = "🐺"
    if(Castillos == "ciervos"):
        castillo = "Cuernos de Ciervo"
        flag = "🦌"
    if(Castillos == "agilas"):
        castillo = "Nido Alto" 
        flag = "🦅"                                  
    if(Castillos == "tiburon"):
        castillo = "Dientes de Tiburón"
        flag = "🦈"
    if(Castillos == "papa"):
        castillo = "Papa"
        flag = "🥔"

    info = {
        "username":user.username,
        "nombre_hero":user.username,
        "castillo":castillo,
        "flag_casti":flag,
        "level":1,
        "exp":0,
        "ataque":1,
        "defensa":1,
        "resis_max":5,
        "resis_min":5,
        "vida_max":300,
        "vida_min":300,
        "mana_max":0,
        "mana_min":0,
        "oro":0,
        "bol_oro":0,
        "gemas":0,        
        "bolso_min":0,        
        "bolso":15,        
        "stock":4000,               
        "manoPrincipal":"None",
        "mano":"None",
        "casco":"None",
        "guantes":"None",
        "armadura":"None",
        "botas":"None",
        "especial":"None",
        "anillo":"None",
        "collar":"None",  
        "pron":"le",
        "estado":"🛌Descanso",
        "puntos_habili":"0",
        "equipados_arm": [[0]],   
        "bolso_arm":[[0]],  
        "almacen_re":[[0]],
        "clase":[[0]],        
        "mascota":"0", 
        "rank":0,
        "lastlog":datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    }
    Fire.put("/players",user.id,info)
    PlayerDB[str(user.id)] = info
    #print(PlayerDB[str(user.id)])
    return
