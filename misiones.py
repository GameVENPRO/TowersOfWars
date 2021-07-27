#Librerías para interactuar con la API de Telegram
from telegram import *
from telegram.ext import *
from funciones import  *



def misiones(update: Update, context: CallbackContext):
    global PlayerDB
    user = update.message.from_user
    player = PlayerDB[str(user.id)]
    level = player["level"] 
    IKB = InlineKeyboardButton
    text = str('🌲Bosque 3min \n Pueden pasar muchas cosas en el bosque.\n\n')
    if(level >= 20):
        text+='🍄Pantano 4min\n' #lvl 20
        text+='Quién sabe lo que está al acecho en el barro.\n\n'
    if(level >= 20):
        text+='🏔Valle de Montaña 4min\n' #lvl 20
        text+='Cuidado con los deslizamientos de tierra.\n\n'
    if(level >= 3):
        text+='🗡Foray 🔋🔋 \n' #Lvl3
        text+='La incursión es una actividad peligrosa. Alguien puede notarlo y puede golpearlo. Pero si pasas desapercibido, conseguirás mucho botín. \n\n'
    if(level >= 5):
        text+='📯Arena \n' #lvl.5
        text+='Arena no es un lugar para débiles. Aquí luchas contra otros jugadores y si sales victorioso, adquieres una experiencia preciosa.'
    
    reply_markup = InlineKeyboardMarkup([
                                                [   
                                                                                                         
                                                    IKB("🌲Bosque",callback_data = '{'+"\"op\":\"reg|gen\",\"d1\":\"{d1}\",\"d2\":\"{d2}\"".format(d1='he',d2=str(user.id))+'}'),                                                    
                                                    IKB("🍄Pantano" if(level >= 20) else "",callback_data = '{'+"\"op\":\"reg|gen\",\"d1\":\"{d1}\",\"d2\":\"{d2}\"".format(d1='he',d2=str(user.id))+'}'),
                                                    IKB("🏔Valle" if(level >= 20) else "",callback_data = '{'+"\"op\":\"reg|gen\",\"d1\":\"{d1}\",\"d2\":\"{d2}\"".format(d1='it',d2=str(user.id))+'}'),
                                                    
                                                ],
                                                [
                                                    IKB("🗡Foray" if(level >= 3) else "",callback_data = '{'+"\"op\":\"reg|gen\",\"d1\":\"{d1}\",\"d2\":\"{d2}\"".format(d1='we',d2=str(user.id))+'}'),
                                                    IKB("📯Arena" if(level >= 5) else "",callback_data = '{'+"\"op\":\"reg|gen\",\"d1\":\"{d1}\",\"d2\":\"{d2}\"".format(d1='they',d2=str(user.id))+'}')
                                                ]
                                            ]
                                          )
    update.message.reply_text(
                                    text,
                                    reply_markup = reply_markup,
                                    parse_mode=ParseMode.HTML
                                )
    return
