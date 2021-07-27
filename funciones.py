#Logging, para empezar a monitorear el desmadre desde el principio
import logging
logging.basicConfig(format=u'%(levelname)s:[%(asctime)s] %(message)s',datefmt='%d/%m/%Y %H:%M:%S' , level=logging.INFO, 
                    handlers=[logging.FileHandler(filename="log.log", encoding='utf8'), logging.StreamHandler()])
logger = logging.getLogger(__name__)

#Librerías para interactuar con la API de Telegram
from telegram import *
from telegram.ext import *

#Configuracion 
from cfg import *

# Crea el Actualizador y pásalo el token de tu bot.
updater = Updater(TOKEN, use_context=True)

#Librerías de utilidades
import json
from random import randint as rng,choice
from time import sleep, time
import miscellaneous as misc
import Braile as br
import FullWidth as fw
from tree import tree as tree
import math
from datetime import datetime
import time
import signal


#Otras librerías para el desarrollo
from uuid import uuid4
import sys, os
import threading
import multiprocessing
from html import escape

#Base de Datos
Fire = Fire()

PlayerDB = Fire.get("/players",None)
# print(str(PlayerDB))
NivelesBD = Fire.get("/niveles_exp",None)
# print(str(NivelesBD))
ObjetosDB = Fire.get("/objetos",None)
# print(str(ObjetosDB))
TiendaDB = Fire.get("/tienda",None)


# Informacion para el servidor
def lastrestart(signum,frame):
    data = {
        "signum":str(signum),
        "hora":datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    }
    Fire.put("/","Last_server_restart",data)
    Fire.put("/","players",PlayerDB)
    print("Datos guardados con éxito!")
    return

def error(update,error="Unexpected Error!"):
    """Log Errors caused by Updates."""
    global updater
    bot=updater.bot
    Mickey = 622952731
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    try:
        update = update.to_dict()
    except:
        update = str(update)
    #print(str(fname))
    message = "Actualizar: \n{} \n...Error causado : \n\n<code>{}:{}</code> en <code>{}</code> en la linea <code>{}</code>\n\nNotas: {}".format(
                tree(update,HTML=True),
                escape(str(exc_type)),
                escape(str(exc_obj)),
                escape(str(fname)),
                escape(str(exc_tb.tb_lineno)),
                escape(str(error)))
    bot.send_message(Mickey,message,parse_mode=ParseMode.HTML)
    message = message.replace("<code>","")
    message = message.replace("</code>","")
    logger.warning(message)
    return

def fallback(update: Update, context: CallbackContext):
  context.update_queue.put(update)
  return ConversationHandler.END

def connect(update: Update, context: CallbackContext):
    user = update.message.from_user
    context.bot.send_message(
        chat_id = user.id,
        text="Conectado!",
        parse_mode = ParseMode.HTML
        )
    return

def updateUser(user):
    global PlayerDB
    Fire.put("/players/"+str(user.id),"username",user.username)
    Fire.put("/players/"+str(user.id),"lastlog",datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    PlayerDB[str(user.id)]["username"] = user.username
    PlayerDB[str(user.id)]["lastlog"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    #print(PlayerDB[str(user.id)])
    return

def reload(update: Update, context: CallbackContext):
    user = update.message.from_user
    if(user.id == 622952731):
        def reloadTask():
            global PlayerDB,NivelesBD,ObjetosDB,TiendaDB
            PlayerDB = Fire.get("/players",None)
            NivelesBD = Fire.get("/niveles_exp",None)
            ObjetosDB = Fire.get("/objetos",None)
            TiendaDB = Fire.get("/tienda",None)
            context.bot.send_message(
                chat_id = user.id,
                text="<code>¡Recargado!</code>",
                parse_mode = ParseMode.HTML
                )
            return
        threading.Thread(target = reloadTask).start()
    return

def upload(player,concept,value):
    threading.Thread(target=manualupload,args=("/players/{id}".format(id=player),concept,value,)).start()
    return

def uploadwp(player,w,concept,value):
    threading.Thread(target=manualuploadwp,args=("/players/{id}/bolso_arm/{p}".format(id=player,p=w),concept,value,)).start()
    return

def manualuploadwp(player,concept,value):
    global PlayerDB
    if(type(concept) in [list,tuple]):
        for c in range(len(concept)):
            try:
                Fire.put(player,concept[c],value[c])
            except:
                e = "{}/{} = {}".format(player,concept[c],value[c])
                error("En la carga manual",e)
    else:
        Fire.put(player,concept,value)
    PlayerDB = Fire.get("/players",None)
    return

def manualupload(player,concept,value):
    global PlayerDB
    if(type(concept) in [list,tuple]):
        for c in range(len(concept)):
            try:
                Fire.put(player,concept[c],value[c])
            except:
                e = "{}/{} = {}".format(player,concept[c],value[c])
                error("En la carga manual",e)
    else:
        Fire.put(player,concept,value)
    PlayerDB = Fire.get("/players",None)
    return

