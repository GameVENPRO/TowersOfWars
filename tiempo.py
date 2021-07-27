#Librerías para interactuar con la API de Telegram
from telegram import *
from telegram.ext import *
from funciones import  *
from kb import *

def tiempo(update: Update, context: CallbackContext):
    dt = datetime.datetime.now()     # Fecha y hora actual


    anno = dt.year
    m =  dt.month
    dia= dt.day 
    hora= str(dt.hour)
    min= dt.minute

    text= "<b>En el mundo de Chat Wars ahora</b>"    

    if(m == 1):
       mes="Wintar "
            #    Invierno 31"
    if(m == 2):
      mes= "Hornung "
         #   Invierno 28"
    if(m == 3):
        mes="estrellas"
               #  Primavera 30"
    if(m == 5):
	    mes=" Winni "
               # Primavera 31"
    if(m == 6):
	    mes="Brāh "
               # Verano 30"
    if(m == 7):
 	    mes="Hewi "
              #  Verano 31"
    if(m == 8):
    	m="Aran "
               # Verano 31"
    if(m == 9):
    	    mes="Witu "
               # Otoño 30"
    if(m == 10):
	    mes="Wīndume "
               # Otoño 31"
    if(m == 11):
	    mes="Herbista "
               # Otoño 30"
    if(m == 12):
	    mes=" Hailag "
               # Invierno 31"
        
    if(hora == "00"):
        text+="\n🌤Mañana"
    elif(hora == "01"):
        text+="\n🌞Día"
    elif(hora == "02"):
        text+="\n🌞Día"
    elif(hora == "03"):
        text+= "\n⛅️Tarde"
    elif(hora == "04"):
        text+= "\n⛅️Tarde"
    elif(hora == "05"):
        text+="\n🌙Noche"
    elif(hora == "06"):
        text+="\n🌙Noche"
    elif(hora == "07"):
        text+="\n🌤Mañana"
    elif(hora == "08"):
        text+="\n🌤Mañana"
    elif(hora == "09"):
        text+="\n🌞Día"
    elif(hora == "10"):
        text+="\n🌞Día"
    elif(hora == "11"):
        text+= "\n⛅️Tarde"
    elif(hora == "12"):
        text+= "\n⛅️Tarde"  
    elif(hora == "13"):
        text+="\n🌙Noche"
    elif(hora == "14"):
        text+="\n🌙Noche"
    elif(hora == "15"):
        text+="\n🌤Mañana"
    elif(hora == "16"):
        text+="\n🌤Mañana"
    elif(hora == "17"):
        text+="\n🌞Día"
    elif(hora == "18"):
        text+="\n🌞Día"
    elif(hora == "19"):
        text+= "\n⛅️Tarde"
    elif(hora == "20"):
        text+= "\n⛅️Tarde"
    elif(hora == "21"):
        text+="\n🌙Noche"
    elif(hora == "22"):
        text+="\n🌙Noche"
    elif(hora == "23"):
        text+="\n🌤Mañana"
        
    text+= "\n{h}:{m}".format(h=hora ,m=min)    

    text+= "\n{d} {m} {a}".format(d=dia , m=mes, a=anno)

    text+= "\n\n<b>Pronóstico del tiempo</b>"
    text+= "\n[🌫→🌤] (Inactivo)"

    
    reply_markup = ReplyKeyboardMarkup(kb.kb("start"),resize_keyboard=True)

    update.message.reply_text(
        text=text,
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML
    )
    return

def pronostico():
    
    # estados climáticos: Soleado ☀️, Nublado 🌤, Lluvioso 🌧 y Brumoso 🌫
    return

