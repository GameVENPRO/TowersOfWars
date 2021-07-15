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
(ME,    MEINFO,     MEWEAPONS,
BR,     BRNO1,      BRS1,       BRTALK,     BRNOTALK,
DC,     DCNO1,      DCS1,       DCDUEL,
BS,     BSWEAPONS,  BSPECIAL,   BSSBUY,
L7,     L7NO1,      L7S1,       L7PLAY,
HELP,   HME,        HBR,        HDC,        HBS,        HL7,
BACK
) = range(27)


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
import signal
import time
import datetime
from datetime import datetime, timezone

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
# print(str(TiendaDB))
# storeDB = Fire.get("/store",None)
# print(str(storeDB))
categories = ["daga","espada","hacha",
            "arco ","casco","armadura",
            "guantes","botas","escudos"]
tmpPlayers = {'0':'null'}
ArenaList = {'0':'null'}

class kb:
    def kb(op = None, args = None):
        IKB = InlineKeyboardButton
        IKB2 = KeyboardButton
        if(op == 'data'):
            keyboard = [[IKB("Join", callback_data = args)]]
        elif(op == 'dice'):
            keyboard = [[IKB("Roll", callback_data = args)]]
        elif(op == 'start'):
            keyboard = [
                [
                    IKB2("⚔️Atacar"),
                    IKB2("🗺Misiones"),
                    IKB2("🛡Defender")
                ],
                [
                    IKB2("🏅Yo"),
                    IKB2("🏰Castillo"),
                    IKB2("👥Clanes")
                ]
            ]
        elif(op == 'hits'):
            keyboard = [
                [
                    IKB("🗡Cabeza", callback_data="{\"op\":\"batt|mov:ah\",\"room\":\"%s\",\"host\":\"%s\"}"%(args)),
                    IKB("🛡Cabeza", callback_data="{\"op\":\"batt|mov:dh\",\"room\":\"%s\",\"host\":\"%s\"}"%(args))
                ],

                [
                    IKB("🗡Cuerpo", callback_data="{\"op\":\"batt|mov:ab\",\"room\":\"%s\",\"host\":\"%s\"}"%(args)),
                    IKB("🛡Cuerpo", callback_data="{\"op\":\"batt|mov:db\",\"room\":\"%s\",\"host\":\"%s\"}"%(args))
                ],

                [
                    IKB("🗡Pierna", callback_data="{\"op\":\"batt|mov:al\",\"room\":\"%s\",\"host\":\"%s\"}"%(args)),
                    IKB("🛡Pierna", callback_data="{\"op\":\"batt|mov:dl\",\"room\":\"%s\",\"host\":\"%s\"}"%(args))
                ],
            ]
        elif(op == 'wtypes'):
            keyboard = [
                [
                    IKB("Espada",    callback_data="{\"op\":\"%s\",\"d1\":\"espada\",\"d2\":\"%s\"}"%(args)),
                    IKB("Daga",   callback_data="{\"op\":\"%s\",\"d1\":\"daga\",\"d2\":\"%s\"}"%(args)),
                    IKB("Hacha",      callback_data="{\"op\":\"%s\",\"d1\":\"hacha\",\"d2\":\"%s\"}"%(args))
                ],
                [
                    IKB("Arco",  callback_data="{\"op\":\"%s\",\"d1\":\"arco\",\"d2\":\"%s\"}"%(args)),
                    IKB("Botas",   callback_data="{\"op\":\"%s\",\"d1\":\"botas\",\"d2\":\"%s\"}"%(args)),
                    IKB("Armadura",     callback_data="{\"op\":\"%s\",\"d1\":\"armadura\",\"d2\":\"%s\"}"%(args))
                ],
                [
                    IKB("Guantes",   callback_data="{\"op\":\"%s\",\"d1\":\"guantes\",\"d2\":\"%s\"}"%(args)),
                    IKB("Lanza",    callback_data="{\"op\":\"%s\",\"d1\":\"lanza\",\"d2\":\"%s\"}"%(args)),
                    IKB("Escudo",   callback_data="{\"op\":\"%s\",\"d1\":\"escudo\",\"d2\":\"%s\"}"%(args))
                ],                
                [
                    IKB("Cascos",   callback_data="{\"op\":\"%s\",\"d1\":\"casco\",\"d2\":\"%s\"}"%(args))
                ],
            ]
        else:
            keyboard = [[IKB("╔"),IKB("╗")],[IKB("╚"),IKB("╝")]]
        return keyboard

class Player:
    def __init__(self,name,last_name,id):
        self.name = name
        self.last_name = last_name
        self.id = id
        self.link = ('<a href="tg://user?id={}">{}</a>'.format(id,escape(name))).strip()
        self.hp = 100
        self.Atk = None
        self.Def = None
        self.ready = False
        self.time = None
        self.pron = ''
        self.mainW = {}
        self.offHW = {}
        self.registered = False
        self.regCheck()
        self.genAssign()
        self.weapAssign()
        return

    def regCheck(self):
        global PlayerDB
        if(str(self.id) in list(PlayerDB.keys())):
            self.registered = True
        else:
            self.registered = False

    def weapAssign(self):
        global PlayerDB
        if(str(self.id) in list(PlayerDB.keys())):
            self.mainW = TiendaDB[PlayerDB[str(self.id)]["mainW"]]
            self.offHW = TiendaDB[PlayerDB[str(self.id)]["offHW"]]
        else:
            self.mainW = TiendaDB['01']
            self.offHW = TiendaDB['02']
        return

    def genAssign(self):
        pronouns = {
            'he':{
                'nomin':'he',
                'object':'him',
                'possAdj':'his',
                'possPro':'his',
                'reflex':'himself'
            },
            'she':{
                'nomin':'she',
                'object':'her',
                'possAdj':'her',
                'possPro':'hers',
                'reflex':'herself'
            },
            'it':{
                'nomin':'it',
                'object':'it',
                'possAdj':'its',
                'possPro':'its',
                'reflex':'itself'
            },
            'we':{
                'nomin':'we',
                'object':'us',
                'possAdj':'our',
                'possPro':'ours',
                'reflex':'ourself'
            },
            'they':{
                'nomin':'they',
                'object':'them',
                'possAdj':'their',
                'possPro':'theirs',
                'reflex':'themself'
                }
            }
        if(str(self.id) in list(PlayerDB.keys())):
            self.pron = pronouns[PlayerDB[str(self.id)]['pron']]
        else:
            self.pron = pronouns['it']
        return

    def texts(self):
        txt = """{}, seguro de su poder y habilidad sobre {} no se imagino el salvajismo 
        indescriptible e inimaginable de lo que este era capaz,quedando así a merced de su espada al haber subestimao a su oponente...
        Tras horas de arduo e intenso combate {} logró descubrir una apertura en la legendaria defensa de su oponente, y 
        con movimientos dignos de un gran guerrero logró someter a su fiero rival En esta 
        ocasion su espada ha encontrado un adversario digno, con el cual ha sostenido uno 
        de los encuentros mas emocionantes pues su adversario al igual que él no planeaba rendirse hasta que su sed de sangre fuese satisfecha
        Con dolor y dificultad levanta su espada con manchas de sangre enemiga, transformando así el dolor y sangre que recorre su cuerpo en gritos 
        de gloria, pues su oponente ha encontrado en sus manos una muerte gloriosa como aquellas de antaño"""
        return ''

    def to_dict(self):
        data = {}
        data["name"] = self.name
        data["last_name"] = self.last_name
        data["id"] = self.id
        data["link"] = self.link
        data["hp"] = self.hp
        data["atk"] = self.Atk
        data["def"] = self.Def
        data["ready"] = self.ready
        data["time"] = self.time
        data["pron"] = self.pron
        data["mainW"] = self.mainW
        data["offHW"] = self.offHW
        data["registered"] = self.registered
        return data

    def chrono(self):
        time = 0
        while((self.ready == False) and (time < 30000)):
                sleep(.00085)
                time += 1
        #print('stop -> {t} seconds'.format(t=str(time/1000)))
        if(time >= 30000):
            if(self.Atk == None):
                self.Atk = "nop"
            if(self.Def == None):
                self.Def = "nop"
        self.time = time/1000
        return

class ArenaObject:
    def __init__(self,room,P1,P2,text):
        self.room = room
        self.Players = {}
        self.Players[P1.id]=P1
        self.Players[P2.id]=P2
        self.round = 0
        self.text = text
        self.alive = False
        return

    def playersInfo(self):
        prs = {}
        for p in self.Players.keys():
            prs[p] = {**self.Players[p].to_dict()}
        return prs

    def movAssign(self,Pid,mov):
        if(mov[0] == 'a'):
            if(self.Players[Pid].Atk == None):
                self.Players[Pid].Atk = mov[1]
            else:
                return False
        else:
            if(self.Players[Pid].Def == None):
                self.Players[Pid].Def = mov[1]
            else:
                return False
        return True

    def movCheck(self):
        p1,p2 = list(self.Players.keys())

        if((self.Players[p1].Atk != None) and (self.Players[p1].Def != None)):
            self.Players[p1].ready = True

        if((self.Players[p2].Atk != None) and (self.Players[p2].Def != None)):
            self.Players[p2].ready = True

        sleep(0.0002)
        if((self.Players[p1].time != None) and (self.Players[p2].time != None)):
            return True
        else:
            return False

    def movClear(self):
        prs = list(self.Players.keys())
        for p in prs:
            self.Players[p].Atk = None
            self.Players[p].Def = None
            self.Players[p].ready = False
            self.Players[p].time = None
        return

    def dmgCalc(self):
        prs = list(self.Players.keys())
        part = {'h':'Head','b':'Body','l':'Legs'}
        crit = 1
        critxt = ""
        text = "\n<b>Ronda: %i</b>"%(self.round+1)
        t1 = self.Players[prs[0]].time
        t2 = self.Players[prs[1]].time

        if(t1 > t2):
            prs.reverse()
            if((t1-3) > t2):
                crit = (int(self.Players[prs[0]].mainW["crit"])+int(self.Players[prs[0]].offHW["crit"]))/2
                critxt = "<b>(*CRIT*💀)</b>"
        else:
            if((t2-3) > t1):
                crit = 1.5
                critxt = "<b>(*CRIT*💀)</b>"

        atk = self.Players[prs[0]].Atk
        df = self.Players[prs[1]].Def
        dam = self.atkdef(atk,df,crit)

        if(dam == 0):
            critxt = ""


        if(dam < 0):
            if(dam == -10):
                if(self.Players[prs[1]].hp >= 100):
                    self.Players[prs[1]].hp += dam
                text += '\n%s parece cansado de hacer algo, dando a %s tiempo para recuperar algo de salud(+%i❤️)'%(
                    self.Players[prs[0]].name,
                    self.Players[prs[1]].name,
                    -dam
                )
            elif(dam == -100):
                text = '\nAmbos guerreros parecen tan aburridos, por lo que decidieron abandonar la batalla e ir a dar un paseo...'
                self.Players[prs[0]].hp = 0
                self.Players[prs[1]].hp = 0
                return text
        else:
            if(dam == 100):
                text += '\n%s me atraparon totalmente inconsciente por %s, permitir %s para tratar un <code>%s</code> en %s (%i).'%(
                    self.Players[prs[1]].name,
                    self.Players[prs[0]].name,
                    self.Players[prs[0]].name,
                    fw.toFullWidth("FATAL BLOW"),
                    self.Players[prs[1]].pron['object'],
                    dam

                )
            else:
                text += "\n%s atacar %s's %s con %s %s"%(
                    self.Players[prs[0]].name,
                    self.Players[prs[1]].name,
                    part[atk].lower(),
                    self.Players[prs[0]].pron['possAdj'],
                    self.Players[prs[0]].mainW["name"]
                    )

                if(dam > 0):
                    text += ', trato %s%s daño.'%(
                        str(dam),
                        critxt
                    )

                else:
                    text += ', pero %s logró defender %s utilizar %s %s.'%(
                        self.Players[prs[1]].name,
                        self.Players[prs[1]].pron['reflex'],
                        self.Players[prs[1]].pron['possAdj'],
                        self.Players[prs[1]].offHW['name']
                    )
        self.Players[prs[1]].hp -= dam

        if(self.Players[prs[1]].hp > 0):
            atk = self.Players[prs[1]].Atk
            df = self.Players[prs[0]].Def
            dam = self.atkdef(atk,df,crit)

            if(dam < 0):
                if(dam == -10):
                    if(self.Players[prs[0]].hp >= 100):
                        self.Players[prs[0]].hp += dam
                    text += '\n%s parece cansado de hacer algo, dando %s tiempo para recuperar algo de salud(+%i❤️)'%(
                        self.Players[prs[1]].name,
                        self.Players[prs[0]].name,
                        -dam
                    )
                elif(dam == -100):
                    text = '\nAmbos guerreros parecen tan aburridos, por lo que decidieron abandonar la batalla e ir a dar un paseo...'
                    self.Players[prs[1]].hp = 0
                    self.Players[prs[0]].hp = 0
                    return text
            else:
                if(dam == 100):
                    text += '\n%s me atraparon totalmente inconsciente por %s, permitir %s para tratar un <code>%s</code> en %s.'%(
                        self.Players[prs[0]].name,
                        self.Players[prs[1]].name,
                        self.Players[prs[1]].name,
                        fw.toFullWidth("FATAL BLOW"),
                        self.Players[prs[0]].pron['object']

                    )
                else:
                    text += "\n%s atacar %s's %s con %s %s"%(
                        self.Players[prs[1]].name,
                        self.Players[prs[0]].name,
                        part[atk].lower(),
                        self.Players[prs[1]].pron['possAdj'],
                        self.Players[prs[1]].mainW["name"]
                        )

                    if(dam > 0):
                        text += ', trato %s daño.'%(
                            str(dam)
                        )

                    else:
                        text += ', pero %s logró defender %s usando %s %s.'%(
                            self.Players[prs[0]].name,
                            self.Players[prs[0]].pron['reflex'],
                            self.Players[prs[0]].pron['possAdj'],
                            self.Players[prs[0]].offHW['name']
                        )
            self.Players[prs[0]].hp -= dam
        else:
            self.Players[prs[1]].hp = 0
            text += "\n%s estaba demasiado débil para seguir luchando."%(self.Players[prs[1]].name)
        if(self.Players[prs[0]].hp < 0):
            self.Players[prs[0]].hp = 0
        return text+'\n'

    def atkdef(self,atk,df,crit):#Dam (== -100), (-10), (== 0), (> 0), (== 100)
        if(atk == df):
            if(atk == 'nop'):
                return -100
            else:
                return 0
        elif(df == 'nop'):
            return 100
        else:
            if(atk == 'h'):
                return rng(15,25)*crit
            elif(atk == 'b'):
                return rng(12,20)*crit
            elif(atk == 'l'):
                return rng(5,10)*crit
            else:#atk == 'nop'
                return -10

    def throwChronos(self):
        prs = list(self.Players.keys())
        for p in prs:
            threading.Thread(target=self.Players[p].chrono).start()
        return

    def lifeCheck(self):
        text = ''
        prs = list(self.Players.keys())
        if(self.Players[prs[0]].hp > self.Players[prs[1]].hp):
            win = self.Players[prs[0]].id
            lose = self.Players[prs[1]].id
        elif(self.Players[prs[1]].hp > self.Players[prs[0]].hp):
            win = self.Players[prs[1]].id
            lose = self.Players[prs[0]].id
        else:
            text = "Qué batalla tan aburrida... Qué pérdida de tiempo..."
            return "<b>⚔Duelo⚔</b>"+self.text+'\n'+text

        if(self.Players[win].hp > 100):
            status = [
                "Uno puede sentir fuertes náuseas por lo que acaba de pasar aquí...",
                ",a igual que un vampiro acaba de chupar la",
                "'vida... Que los dioses nos guarde de tal abominación!"
                ]
        elif(self.Players[win].hp == 100):
            status = [
                "Contra todo pronóstico, el guerrero",
                "consiguió una victoria impecable contra {possAdj} oponente".format(possAdj=self.Players[win].pron["possAdj"]),
                "Damas y caballeros, esta es la cara de un verdadero campeón!!!"
                ]
        elif(self.Players[win].hp > 66):
            status = [
                "Como si fuera un juego de niños,",
                "fácil de vencer",
                "en combate."]
        elif(self.Players[win].hp > 33):
            if(self.round > 5):
                length = "long"
            else:
                length = "short"
            status = [
                "Después de {} una batalla acalorada,".format(length),
                "was able to overtake",
                "in what it seemed a paired match."
                ]
        else:
            status = [
                "La pelea fue sangrienta y brutal, pero al final",
                "apenas podría superar {possAdj} oponente".format(possAdj=self.Players[win].pron["possAdj"]),
                "en el último segundo."
                ]

        text += "\n{}❤️{}\n\t\t\t<b>VS</b>\n{}❤️{}".format(
            self.Players[prs[0]].hp,
            self.Players[prs[0]].link,
            self.Players[prs[1]].hp,
            self.Players[prs[1]].link,)

        text += "<i>\n\n{} </i>{}<i> {} </i>{}<i> {}</i> \n<b>🎊 🎉 Felicidades {}!!! 🎉 🎊</b>".format(
                                        status[0],
                                        self.Players[win].name,
                                        status[1],
                                        self.Players[lose].name,
                                        status[2],
                                        self.Players[win].name)

        return "<b>⚔Duelo⚔</b>"+self.text+'\n'+text

def keepAlive(update:Update,context:CallbackContext,arena:ArenaObject):
    query = update.callback_query
    data = json.loads(query.data)
    room = data['room']
    host = int(data['host'])
    counter = 0
    while(counter < 4):
        sleep(1)
        counter += 1
        if(arena.alive):
            arena.alive = False
            counter = 0
            #print("Reset!")
    #print("Time's up!")
    if(arena.movCheck()):
        arena.text += arena.dmgCalc()
        prs = list(arena.Players.keys())
        if((arena.Players[prs[0]].hp > 0) and (arena.Players[prs[1]].hp > 0)):
            text = "<b>⚔ Duelo ⚔</b>"+arena.text+"\n%s❤️ %s\nVs\n%s❤️ %s\n"%(
                arena.Players[prs[0]].hp,
                arena.Players[prs[0]].name,
                arena.Players[prs[1]].hp,
                arena.Players[prs[1]].name,
            )
            rpmkup = InlineKeyboardMarkup(kb.kb(op='hits',args=(room,host)))
            arena.movClear()
            arena.throwChronos()
            arena.round += 1
            threading.Thread(target=keepAlive,args=(update,context,arena,)).start()
        else:
            text = arena.lifeCheck()
            rpmkup = None
        context.bot.edit_message_text(
            text=text,
            inline_message_id=query.inline_message_id,
            reply_markup=rpmkup,
            parse_mode=ParseMode.HTML
        )
        return
    else:
        #print('retrying...')
        keepAlive(update,context,arena)
    return

def battle(update:Update,context:CallbackContext):
    global ArenaList,tmpPlayers
    query = update.callback_query
    data = json.loads(query.data)

    option,phase = data["op"].split("|")
    if("mov:" in phase):
        phase,mov = phase.split(":")
    room = data['room']
    host = int(data['host'])
    try:
        host_link = ('<a href="tg://user?id={}">{}</a>'.format(host,escape(tmpPlayers[host]['first_name']))).strip()
    except KeyError as e:
        context.bot.answerCallbackQuery(query.id,"Esta sesión ha expirado.",True)
        context.bot.edit_message_text(
                                        text="<b>⚔Duelo⚔</b>\n<i>Una fuerte tormenta ha comenzado... Ambos combatientes han decidido posponer su lucha hasta que cese la tormenta...</i>",
                                        inline_message_id=query.inline_message_id,
                                        parse_mode=ParseMode.HTML)
        #error(update,e)
        return

    presser = update.effective_user
    presser_link = ('<a href="tg://user?id={}">{}</a>'.format(presser.id,escape(presser.first_name))).strip()

    if(phase == 'p2'):
        if(host == presser.id):
            quotes = ['Las luchas más difíciles son las que luchas contigo mismo...',
                'Una pelea contigo mismo para ganar la batalla por ti mismo es la más grande e importante.',
                'Lucha contigo mismo para obtener lo mejor de ti mismo.',
                'Cuando luchas por descubrir tu verdadero yo, solo hay un ganador.',
                'No te das cuenta de lo fuerte que eres hasta que estás luchando contra ti mismo.',
                'Nunca es el mundo en el que luchas. Siempre, siempre, eres tú mismo.',
                'La batalla más dura que jamás lucharás en tu vida es la batalla dentro de ti mismo.',
                'Pelear con otros no te hace dormir; pelear contigo mismo es lo que te inquieta.']
            context.bot.answerCallbackQuery(query.id,'“'+choice(quotes)+'”',True)
            return
        else:
            text = '<b>⚔Duel</b>\n¡Ambos oponentes están listos! \n%s se enfrentará %s en la arena! \n<i>Que los dioses estén con ustedes, guerreros...</i>\n\nEsperando a que el anfitrión inicie el duelo...'%(host_link,presser_link)
            ArenaList[room] = ArenaObject(
                                            room = room,
                                            P1 = Player(tmpPlayers[host]['first_name'],tmpPlayers[host]['last_name'],host),
                                            P2 = Player(presser.first_name,presser.last_name,presser.id),
                                            text = '')
            context.bot.edit_message_text(
                                            text=text,
                                            inline_message_id=query.inline_message_id,
                                            reply_markup = InlineKeyboardMarkup (
                                                                                    [
                                                                                        [
                                                                                            InlineKeyboardButton(
                                                                                                text = "Comience el partido!",
                                                                                                callback_data = "{\"op\":\"batt|start\",\"room\":\"%s\",\"host\":\"%s\"}"%(room,host)
                                                                                            )
                                                                                        ]
                                                                                    ]
                                                                                ),
                                            parse_mode=ParseMode.HTML)
            return
    try:
        arena = ArenaList[room]#From here on, there's only blood and glory!
    except KeyError as e:
        context.bot.answerCallbackQuery(query.id,"Esta sesión ha expirado.",True)
        context.bot.edit_message_text(
                                        text="<b>⚔Duelo</b>\n<i>Una fuerte tormenta ha comenzado... Ambos combatientes han decidido posponer su lucha hasta que cese la tormenta...</i>",
                                        inline_message_id=query.inline_message_id,
                                        parse_mode=ParseMode.HTML)
        #error(update,e)
        return

    if(presser.id not in list(arena.Players.keys())):
        context.bot.answerCallbackQuery(query.id,"¿Qué es lo que haces? Esta no es tu Lucha!",True)
        return
    elif(phase == 'start'):
        if(presser.id != host):
            context.bot.answerCallbackQuery(query.id,"Tienes que esperar a que el anfitrión inicie el partido.",True)
            return
        P1,P2 = arena.Players.keys()
        text = "<b>⚔Duelo</b>\nEl partido ha comenzado!\n%s❤️ %s\nVs\n%s❤️ %s\n\nRonda: %s\n¿Qué harás?\n<b>Elige puntos de ataque y defensa.</b>"%(
            str(int(arena.Players[P1].hp)),
            arena.Players[P1].name,
            str(int(arena.Players[P2].hp)),
            arena.Players[P2].name,
            arena.round+1)
        context.bot.edit_message_text(
                                        text=text,
                                        inline_message_id=query.inline_message_id,
                                        reply_markup=InlineKeyboardMarkup(kb.kb(op='hits',args=(room,host))),
                                        parse_mode=ParseMode.HTML)
        arena.throwChronos()
        threading.Thread(target=keepAlive,args=(update,context,arena,)).start()
        return

    elif(phase == 'mov'):
        act = {'a':'Attack','d':'Defend'}
        part = {'h':'Head','b':'Body','l':'Legs'}
        mc = arena.movAssign(presser.id,mov)
        if(mc):
            context.bot.answerCallbackQuery(query.id,act[mov[0]]+' '+part[mov[1]],False)
            arena.alive = True
        else:
            context.bot.answerCallbackQuery(query.id,"Lo siento, ya elegiste qué %s"%(act[mov[0]]),True)
            return
        if(arena.movCheck()):
            battletext = arena.dmgCalc()
            arena.round += 1
            p1,p2 = list(arena.Players.keys())
            p1n = arena.Players[p1].link
            p1h = arena.Players[p1].hp

            p2n = arena.Players[p2].link
            p2h = arena.Players[p2].hp
            arena.text += battletext
            text = str("<b>⚔Duelo⚔</b>\n"
                +"{btext}".format(btext=arena.text)
                +"\n\n{health}❤️ {name}".format(health=str(math.ceil(p1h)),name=p1n)
                +"\n\t\t\t\tVs"
                +"\n{health}❤️ {name}\n".format(health=str(math.ceil(p2h)),name=p2n)
            )
            if(p1h > 0 and p2h > 0 ):
                arena.movClear()
                arena.throwChronos()
                rpmkup = InlineKeyboardMarkup(kb.kb(op='hits',args=(room,host)))
            else:
                arena.movClear()
                text = arena.lifeCheck()
                rpmkup = None
            try:
                context.bot.edit_message_text(
                                                text=text,
                                                inline_message_id=query.inline_message_id,
                                                reply_markup=rpmkup,
                                                parse_mode=ParseMode.HTML)
            except Exception as e:
                error(update,e)
            return

    return

def start(update: Update, context: CallbackContext):
    query = update.message.from_user
    text = """Te acercas y ves un cartel en la puerta:\n
            < i > Discúlpenos, por el momento que ' re bajo mantenimiento...
            Sin embargo, siempre se puede utilizar nuestra pista de duelo que está en la parte de atrás. Solo escribe: 
            \n \ " @TorreRPG_bot + <code > space< / code > \"\n y pulse\" Duel Duel \ " en cualquier ventana de chat para acceder a ella.
            <s>(cosas aleatorias pueden suceder debido a la física cuántica.)</s>
            Estaremos de negocios en un par de días...</me>
            \n"""
    update.message.reply_text(
                                text,
                                reply_markup = None,
                                parse_mode=ParseMode.HTML
                            )

    return

def register(update: Update, context: CallbackContext):
    user = update.message.from_user
    IKB = InlineKeyboardButton
    if(str(user.id) in list(PlayerDB.keys())):
        welcometext = "Bienvenido de vuelta, {name}! \n¿Cómo puedo servirle hoy?".format(name=user.first_name)
        reply_markup = ReplyKeyboardMarkup(kb.kb("start"),resize_keyboard=True)
        update.message.reply_text(
            text=welcometext,
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )
        threading.Thread(target=updateUser,args=(user,)).start()
        return ConversationHandler.END
    else:
        text = str("Vaya, vaya, vaya... ¿Qué tenemos aquí? Pareces nuevo por aquí, ¿no?"
            +" Bienvenido a la <i>Taberna Trotamundos</i>, viajero, donde puedes encontrar la mejor cerveza que jamás encontrarás en todo el continente."
            +"\nMi nombre es @JuanShotLC, y yo soy el que sirve por aquí."
            +"\nAntes que nada, por favor, viajero, hazme saber tu género...")
        reply_markup = InlineKeyboardMarkup([
                                                [
                                                    IKB("♀ Dama",callback_data = '{'+"\"op\":\"reg|gen\",\"d1\":\"{d1}\",\"d2\":\"{d2}\"".format(d1='she',d2=str(user.id))+'}'),
                                                    IKB("♂ Caballero",callback_data = '{'+"\"op\":\"reg|gen\",\"d1\":\"{d1}\",\"d2\":\"{d2}\"".format(d1='he',d2=str(user.id))+'}')
                                                ],
                                                [
                                                    IKB("🕈 Muerto",callback_data = '{'+"\"op\":\"reg|gen\",\"d1\":\"{d1}\",\"d2\":\"{d2}\"".format(d1='it',d2=str(user.id))+'}'),
                                                    IKB("☭ Compañero",callback_data = '{'+"\"op\":\"reg|gen\",\"d1\":\"{d1}\",\"d2\":\"{d2}\"".format(d1='we',d2=str(user.id))+'}')
                                                ],
                                                [   IKB("▣ Otro",callback_data = '{'+"\"op\":\"reg|gen\",\"d1\":\"{d1}\",\"d2\":\"{d2}\"".format(d1='they',d2=str(user.id))+'}')]
                                            ]
                                          )
        update.message.reply_text(
                                    text,
                                    reply_markup = reply_markup,
                                    parse_mode=ParseMode.HTML
                                )
        return

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

def reg(update: Update, context: CallbackContext):
    query = update.callback_query
    data = json.loads(query.data)
    option,next = data["op"].split("|")
    user = query.from_user
    if(next == 'gen'):
        if(data["d1"] == "we"):
            namename = "Comrade"
        else:
            namename = user.first_name
        text = '<i>Tu nombre es... Ya veo. Mucho gusto, {name}!\n\n'.format(name=namename)
        try:
            context.bot.edit_message_reply_markup(
                chat_id=user.id,
                message_id=query.message.message_id,
                #inline_message_id=query.inline_message_id,
                reply_markup=None
            )
            reply_markup = ReplyKeyboardMarkup(kb.kb("start"),resize_keyboard=True)
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
    info = {
        "username":user.username,
        "nombre_hero":user.username,
        "castillo":0,
        "flag_casti":0,
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
        "oro":1000,
        "bol_oro":50,
        "gemas":100,        
        "bolso":15,        
        "stock":4000,        
        "clase":0,        
        "mascota":0,        
        "mainW":0,
        "offHW":"02",      
        "manoPrincipal":"None",
        "mano":"None",
        "casco":"None",
        "guantes":"None",
        "armadura":"None",
        "botas":"None",
        "especial":"None",
        "anillo":"None",
        "collar":"None",  
        "pron":pron,
        "estado":"🛌Descanso",
        "puntos_habili":"0",
        "bolso_arm":[{"01":"01"}],
        "weapons":[False],
        "rank":0,
        "lastlog":datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    }
    Fire.put("/players",user.id,info)
    PlayerDB[str(user.id)] = info
    #print(PlayerDB[str(user.id)])
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

def queryHandler(update: Update, context: CallbackContext):
    query = update.callback_query
    data = json.loads(query.data)
    option,next = data["op"].split("|")
    #print(tree(update.to_dict(),HTML=False))
    ##print("Acá elijo qué se va a hacer :9")
    if(option == "batt"):
        threading.Thread(target = battle, args = (update,context,)).start()
        ##print("Acá fue battle!")
    if(option == "dice"):
        threading.Thread(target = dice, args = (update,context,)).start()
        ##print("Acá fue dado!")
    if(option == "reg"):
        threading.Thread(target = reg, args = (update,context,)).start()
    if(option == "owned"):
        threading.Thread(target = owned, args = (update,context,)).start()
    if(option == "bsmith"):
        threading.Thread(target = shopcat, args = (update,context,)).start()
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

def inlinequery(update: Update, context: CallbackContext):
    #Handle the inline query.
    global tmpPlayers
    query = update.inline_query
    target = update.inline_query.from_user
    target_name = ('<a href="tg://user?id={}">{}</a>'.format(target.id,escape(target.first_name))).strip()
    reply_markup = None
    tmpPlayers[target.id] = {
        'first_name':target.first_name,
        'last_name':target.last_name,
        'username':target.username}
    #print(tree(update.to_dict()))

    results = [
                InlineQueryResultArticle(
                                            id=uuid4(),
                                            title="⚔Duelo",
                                            reply_markup = InlineKeyboardMarkup(kb.kb(op = "data",args = "{\"op\":\"batt|p2\",\"room\":\"%s\",\"host\":\"%s\"}"%(str(int(list(ArenaList.keys())[-1])+1),str(target.id)))),
                                            input_message_content= InputTextMessageContent(
                                                                                            message_text = "<b>⚔Duelo</b>\n{} está buscando un oponente digno...{}".format(target_name,"\n\n<code>También puede registrarse en</code>@Torre_RPGBot<code> para personalizarte...</code>"),
                                                                                            parse_mode=ParseMode.HTML,
                                                                                            reply_markup = reply_markup,
                                                                                         )
                                        ),
                InlineQueryResultArticle(
                                            id=uuid4(),
                                            title="🎲Dice",
                                            reply_markup = InlineKeyboardMarkup(kb.kb(op = "dice",args = "{\"op\":\"dice|dice\",\"next\":\"dice\",\"room\":\"%s\"}"%(target.username))),
                                            input_message_content=InputTextMessageContent(
                                                                                            message_text = "Pulsar <i>\"Roll\"</i> para rodar los dados...",
                                                                                            parse_mode=ParseMode.HTML,
                                                                                            reply_markup = reply_markup
                                                                                        ),

                                        ),
                InlineQueryResultArticle(
                                            id=uuid4(),
                                            title="🍺Cerveza",
                                            input_message_content=InputTextMessageContent(
                                                                                            message_text = "Se le da un frasco lleno de cerveza espumosa🍺.\n{}: <i>Brindemos por el placer de estar aquí y ahora!</i>".format(target_name),
                                                                                            parse_mode=ParseMode.HTML
                                                                                        )
                                        )
              ]
    if("&Codify" in query.query):
        txt = query.query.replace("&Codify ","")
        txt = br.toBraile(txt)
        results.append(
                        InlineQueryResultArticle(
                                                    id=uuid4(),
                                                    title="⠨⠉⠕⠝⠧⠑⠗⠞⠖",
                                                    input_message_content= InputTextMessageContent(
                                                                                                    message_text = txt,
                                                                                                    parse_mode=ParseMode.HTML
                                                                                                    #reply_markup = reply_markup,
                                                                                                 )
                                                )
                        )
    if(False):
        results.append(
                        InlineQueryResultArticle(
                                                    id=uuid4(),
                                                    title="🎖{} Tournament🏅".format(query.query.title()),
                                                    input_message_content= InputTextMessageContent(
                                                                                                    message_text = "<b>Join the {} Tournament!</b>\n\nPlayers:\n".format(query.query.title()),
                                                                                                    parse_mode=ParseMode.HTML
                                                                                                    #reply_markup = reply_markup,
                                                                                                 )
                                                )
                        )
    context.bot.answer_inline_query(
                        update.inline_query.id,results=results,
                        cache_time = 1,
                        is_personal=True,
                        switch_pm_text='Enter the Tavern',
                        switch_pm_parameter='register')
    #update.inline_query.answer(results)
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

def me(update: Update, context: CallbackContext):
    global PlayerDB
    user = update.message.from_user
    player = PlayerDB[str(user.id)]
    level = player["level"] 
    exp_niveles = NivelesBD[level+1]       
    
    bolso_arm = len(player["bolso_arm"])
    if(bolso_arm == 0):
        cantid_armas = "0" 
    else:
        cantid_armas = bolso_arm    
    

        text="\n🌟Congratulations Felicitaciones! Nuevo nivel!🌟"
        text+="\n\nAsignar puntos /level_up"
        text+="\nBatlla"
        text+="\n\n🦅🌑"
        text+="[]Clan!"
        text+="{name}".format(name=user.first_name)
        text+="ClaseAqui"
        text+="del"
        text+="Castillo"
        text+="\n🏅Nivel: {level}".format(level=str(player["level"]))        
        text+="\n⚔️Ataque: {ataq}".format(ataq=str(player["ataque"]))
        text+="🛡Defensa: {defensa}".format(defensa=str(player["defensa"]))
        text+="\n🔥Exp: {exp}".format(exp=str(player["exp"])) 
        text+="/{exp_niv}".format(exp_niv=str(exp_niveles))
        text+="\n❤️Vida: {vdmin}".format(vdmin=str(player["vida_min"]))
        text+="/{vdmax}".format(vdmax=str(player["vida_max"]))        
        text+="\n🔋Resistencia:{rsmin}".format(rsmin=str(player["resis_min"]))
        text+="/{rsmax}".format(rsmax=str(player["resis_max"]))
        if(player["mana_max"]>0):
            text+="\n💧Mana:{mnamin}".format(mnamin=str(player["mana_min"]))
            text+="/{mnamax}".format(mnamax=str(player["mana_max"]))          
        text+="\n💰{oro}".format(oro=player["oro"])
        if(player["bol_oro"] > 0):
            text+="👝{bol_oro}".format(bol_oro=str(player["bol_oro"]))
        text+="💎{gemas}".format(gemas=player["gemas"])
        text+="\n\n🎽Euipamiento:"
        text+="\n🎒Balso: {total}".format(total=cantid_armas)
        text+="/{bolso} ".format(bolso=player["bolso"])
        text+="/inv"
        # +"Mascota:{money}".format(money=player["money"])
        text+="\n\nEstado:\n{estado}".format(estado=player["estado"])
        text+="\n\nMás: /heroe"
        #  +"\n\n🎒 Equipo:\n"
        #  +"\t"*4+"► Principal: {main}\n".format(main=TiendaDB[player["mainW"]]["name"])
        #  +"\t"*4+"► Offhand: {offh}".format(offh=offhw)
        
    IKB = KeyboardButton
    reply_markup = ReplyKeyboardMarkup(
        [
            [
                IKB("🗡Armas"),
                IKB("↩️Volver")
            ]
        ],
        resize_keyboard=True,
    )
    # reply_markup = ReplyKeyboardMarkup(kb.kb("start"),resize_keyboard=True)

    update.message.reply_text(
        text=text,
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML
    )
    return 

def heroe(update: Update, context: CallbackContext):
    global PlayerDB
    user = update.message.from_user
    player = PlayerDB[str(user.id)]
    level = player["level"] 
    exp_niveles = NivelesBD[level+1]
         
    
    bolso_arm = len(player["bolso_arm"])
    if(bolso_arm == 0):
        cantid_armas = "0" 
    else:
        cantid_armas = bolso_arm    

    
        text="\n{name}".format(name=user.first_name)
        text+="\n🏅Nivel: {level}".format(level=str(player["level"]))        
        text+="\n⚔️Ataque: {ataq}".format(ataq=str(player["ataque"]))
        text+="🛡Defensa: {defensa}".format(defensa=str(player["defensa"]))
        text+="\n🔥Exp: {exp}".format(exp=str(player["exp"])) 
        text+="/{exp_niv}".format(exp_niv=str(exp_niveles))
        text+="\n❤️Vida: {vdmin}".format(vdmin=str(player["vida_min"]))
        text+="/{vdmax}".format(vdmax=str(player["vida_max"]))        
        text+="\n🔋Resistencia:{rsmin}".format(rsmin=str(player["resis_min"]))
        text+="/{rsmax}".format(rsmax=str(player["resis_max"]))
        if(player["mana_max"]>0):
            text+="\n💧Mana:{mnamin}".format(mnamin=str(player["mana_min"]))
            text+="/{mnamax}".format(mnamax=str(player["mana_max"]))          
        text+="\n💰{oro}".format(oro=player["oro"])
        if(player["bol_oro"] > 0):
            text+="👝{bol_oro}".format(bol_oro=str(player["bol_oro"]))
        text+="💎{gemas}".format(gemas=player["gemas"])
        
        text+="\n📚Especializaciónes:-"
        text+="\n🎉Logro: /ach"
        text+="\n⚒Clase Info: /class"
        text+="\n🚹Male"
        
        text+="\n\n✨Efectos: /effects"
        # +"Mascota:{money}".format(money=player["money"])      
        
        text+="\n\n🎽Euipamiento: "
        
        text+="\n\n🎒Balso: {total}".format(total=cantid_armas)
        text+="/{bolso} ".format(bolso=player["bolso"])
        text+="/inv"
        text+="\n\n📦Almacen: /stock"

    reply_markup = ReplyKeyboardMarkup(kb.kb("start"),resize_keyboard=True)

    update.message.reply_text(
        text=text,
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML
    )
    return 

def inventario(update: Update, context: CallbackContext):
    global PlayerDB
    global TiendaDB
    user = update.message.from_user
    player = PlayerDB[str(user.id)]
   
    bolso_arm = len(player["bolso_arm"])
    
    if(bolso_arm == 0):
        cantid_armas = "0" 
    else:
        cantid_armas = bolso_arm   
   
    
    
    # text="🎽Euipamiento: {t}{td}".format(t=total_a,td=total_d,t0=total_equi)
    # text+="\n{ap} {a}{d} {id}".format(ap=armp_nom,a=ata,d=defn,id=i)
    # text+="\n{arma_s} {a2}{d2} {id2}".format(arma_s=ars_nom,a2=atas,d2=defns,id2=ids)
    # text+="\n{name_ca} {ataq_ca}{def_ca} {id_ca}".format(name_ca=co_nom,def_ca=defco,ataq_ca=co_ata,id_ca=idco)    
    # text+="\n{name_g} {ataq_g}{def_g} {id_g}".format(name_g=g_nom,def_g=defng,ataq_g=atag,id_g=idg)
    # text+="\n{name_a} {ataq_a}{def_a} {id_ar}".format(name_a=a_nom,def_a=defna,ataq_a=ataa,id_ar=ida)
    # text+="\n{name_b} {ataq_b}{def_b} {id_b}".format(name_b=bnom,def_b=bdef,ataq_b=bata,id_b=bid)
    # text+="\n{name_es} {ataq_es}{def_es} {id_es}".format(name_es=snom,def_es=sdef,ataq_es=sata,id_es=sid)
    # text+="\n{name_an} {ataq_an}{def_an} {id_an}".format(name_an=anom,def_an=adef,ataq_an=aata,id_an=aid)
    # text+="\n{name_co} {ataq_co}{def_co} {id_co}".format(name_co=cnom,def_co=cdef,ataq_co=cata,id_co=cid)
    text="\n🎒Balso: {total}/{max} ".format(total=cantid_armas,max=str(player["bolso"]))
         
    # for w in list(set(player["bolso_arm"].keys())):
        
    #     text+="\n\n<b>{name}</b> ".format(name=TiendaDB[w]["nombre"])
    #     if(TiendaDB[w]["atributos"]["ataque"] > 0):
    #         text+="<b>+{actaque}</b>⚔️".format(actaque=TiendaDB[w]["atributos"]["ataque"])
    #     if(TiendaDB[w]["atributos"]["defensa"] > 0):
    #         text+="<b>+{defensa}</b>🛡".format(defensa=TiendaDB[w]["atributos"]["defensa"])
    #     text+="\n  /on_{id}".format(id=w)


            
    reply_markup = ReplyKeyboardMarkup(kb.kb("start"),resize_keyboard=True)

    update.message.reply_text(
        text=text,
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML
    )
    return

def tiempo(update: Update, context: CallbackContext):

  
  #  future = datetime.datetime.utcnow() - datetime.timedelta(hours=1*3 - 331.65)
   # epoch = future - datetime.datetime(1970, 1, 1)
    #dia = epoch.days
   # print(epoch)
    #hora = time.strftime("%H")

    #from datetime import datetime, timezone

    #dt = datetime(1059, 8, 8,21,31,0, tzinfo=timezone.utc )
    #timestamp = int( dt.timestamp() )
    #print( timestamp )

    #m=1

    #if(m==1):
    #	print('Wintar')
    #	
    #hora = dt.horus 
    #minutos = dt.minutes

    #print( str(hora) +':'+str(minutos))

    timestamp = -28729391340
   #-28729468800
    dt = datetime.fromtimestamp( timestamp, tz=timezone.utc )
    print(dt )
    m = dt.month
    dia= dt.day
    anno= dt.year
    hora = dt.hour
    minutos = dt.minutes
    completa=str(hora) +':'+str(minutos)

    if(m  == 1 ):
       mes="Wintar Invierno 31"
    if(m==2 ):
      mes= "Hornung Invierno 28"
    if(m ==3 ):
        mes="estrellas Primavera 30"
    if(m==5):
	mes=" Winni Primavera 31"
    if(m==6):
	mes="Brāh Verano 30"
    if(m==7 ):
 	mes="Hewi Verano 31"
    if(m==8):
	print("Aran Verano 31"
    if(m==9 ):
	mes="Witu Otoño 30"
    if(m==10 ):
	mes="Wīndume Otoño 31"
    if(m==11 ):
	mes="Herbista Otoño 30"
    if(m==12):
	mes=" Hailag Invierno 31"


    text= "<b>En el mundo de Chat Wars ahora</b>"    
        
    if(hora == "00"):
        text+="\n🌤Mañana"
    elif (hora == "01"):
        text+="\n🌞Día"
    elif (hora == "02"):
        text+="\n🌞Día"
    elif (hora == "03"):
        text+= "\n⛅️Tarde"
    elif (hora == "04"):
        text+= "\n⛅️Tarde"
    elif (hora == "05"):
        text+="\n🌙Noche"
    elif (hora == "06"):
        text+="\n🌙Noche"
    elif(hora == "07"):
        text+="\n🌤Mañana"
    elif(hora == "08"):
        text+="\n🌤Mañana"
    elif (hora == "09"):
        text+="\n🌞Día"
    elif (hora == "10"):
        text+="\n🌞Día"
    elif (hora == "11"):
        text+= "\n⛅️Tarde"
    elif (hora == "12"):
        text+= "\n⛅️Tarde"  
    elif (hora == "13"):
        text+="\n🌙Noche"
    elif (hora == "14"):
        text+="\n🌙Noche"
    elif(hora == "15"):
        text+="\n🌤Mañana"
    elif(hora == "16"):
        text+="\n🌤Mañana"
    elif (hora == "17"):
        text+="\n🌞Día"
    elif (hora == "18"):
        text+="\n🌞Día"
    elif (hora == "19"):
        text+= "\n⛅️Tarde"
    elif (hora == "20"):
        text+= "\n⛅️Tarde"
    elif (hora == "21"):
        text+="\n🌙Noche"
    elif (hora == "22"):
        text+="\n🌙Noche"
    elif(hora == "23"):
        text+="\n🌤Mañana"
        
    text+= "\n 24 hrs {h}".format(h=completa)
    #text+= "\n 12 hrs {h}".format(h=time.strftime("%I:%M"))    
    #text+= "\n Rapido {h}".format(h=epoch)    
    text+= "\n{d} {m} {y}".format(d=dia,m=mes,y=anno)
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

def clan(update: Update, context: CallbackContext):
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

def castillo(update: Update, context: CallbackContext):

    hora = time.strftime("%H")
    print(hora)
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

    IKB = KeyboardButton
    reply_markup = ReplyKeyboardMarkup(
        [
            [
                IKB("⚒Taller"),                
                IKB("🍺Taberna"),                
                IKB("🛎Subasta"),                

            ],
            [
                IKB("⚖️Intercambio"),                
                IKB("🏚Tienda"),                
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
    return 

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
    player = PlayerDB[str(user.id)]
    weapons = False
    text="<b>Aquí, algunas mercancías:</b>\n"
    # - set(player["weapons"])
    for w in sorted(list(set(TiendaDB.keys()))):
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
                wps = player["bolso_arm"]
                oro = str(int(PlayerDB[str(user.id)]["oro"]) - int(TiendaDB[weapon]["precio"]))
                upload(player=str(user.id),concept=("bolso_arm","oro"),value=(wps,oro))
                Newcompra(user=user.id,items=weapon)            
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
    
    info = {
        "id": TiendaDB[items]["id"],
        "nombre": TiendaDB[items]["nombre"],
        "historia": TiendaDB[items]["historia"],
        "tipo": TiendaDB[items]["tipo"],
        "g_type": TiendaDB[items]["g_type"],
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
    Fire.put("/players",user,"/bolso_arm",items,"/",info)
    PlayerDB[str(user)]["bolso_arm"] = info
    print(PlayerDB[str(user)]["bolso_arm"])
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

def forge(update: Update, context: CallbackContext):
    text='Lo siento amigo, no puedo hacer nada sin mis herramientas... Al menos que quieras usar un palillo como estoque, ja ja!'
    update.message.reply_text(text=text)
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

def owned(update: Update, context: CallbackContext):
    try:
        user = update.message.from_user
        data = {"op":"owned|na","d1":"sword","d2":"null"}
    except:
        user = update.callback_query.from_user
        data = json.loads(update.callback_query.data)

    player = PlayerDB[str(user.id)]
    text = "<b>{name}'s {type} tipo de armas:</b>\n".format(name=user.first_name,type=data["d1"])
    weapons = False
    for w in [*player["bolso_arm"]]:
        try:
            if(TiendaDB[w]["g_type"] == data["d1"]):
                text+="\n"+"\t"*4+"► {name} /info_{id} \n\t\t\t\t\t\t\t\tEquip: /on_{id}".format(name=TiendaDB[w]["nombre"],id=w)
                weapons = True
        except:
            player["bolso_arm"].remove(None)
            continue

    if(weapons == False):
        text += "\n"+"\t"*4+"<b>((Vacio))</b>"
    reply_markup = InlineKeyboardMarkup(kb.kb(op="wtypes",args=("owned|na","null")))
    try:
        update.message.reply_text(
                                    text,
                                    reply_markup = reply_markup,
                                    parse_mode=ParseMode.HTML
                                )
    except Exception as e:
        context.bot.edit_message_text(
                                text=text,
                                chat_id=user.id,
                                message_id=update.callback_query.message.message_id,
                                reply_markup = reply_markup,
                                parse_mode=ParseMode.HTML
                            )
    return

def equip(update: Update, context: CallbackContext):
    user = update.message.from_user
    player = PlayerDB[str(user.id)]
    weapon = update.message.text.replace("/on_","")
    if(weapon not in TiendaDB.keys()):
        return
    else:
        if(weapon not in player["weapons"]):
            text = "¡No eres el dueño de esta arma!"
        else:
            wpassign(weapon,user)
            text = "<b>{weapon}</b> equipado con éxito!".format(weapon = TiendaDB[weapon]["nombre"])
        update.message.reply_text(
                                    text=text,
                                    parse_mode=ParseMode.HTML
                                )
    return

def wpassign(weapon,user):
    slot = ""
    if(TiendaDB[weapon]["type"] in ["dagger","shield"]):
        slot = "offHW"
    else:
        slot = "mainW"

    if(slot == "mainW"):
        if(TiendaDB[weapon]["dual"] == True):
            """Cambian ambos slots"""
            upload(player=str(user.id),concept=("mainW","offHW"),value=(weapon,"999"))
        else:
            if(TiendaDB[PlayerDB[str(user.id)]["mainW"]]["dual"] == True):
                """Asigna el arma, y Wooden Shield, respectivamente"""
                upload(player=str(user.id),concept=("mainW","offHW"),value=(weapon,"02"))
            else:
                """Cambia normalmente"""
                upload(player=str(user.id),concept=("mainW"),value=(weapon))
    else:
        if(TiendaDB[PlayerDB[str(user.id)]["mainW"]]["dual"] == True):
            """Asigna Iron Sword como principal y la secundaria normalmente"""
            upload(player=str(user.id),concept=("mainW","offHW"),value=("01",weapon))
        else:
            """Asigna secundaria normalmente"""
            upload(player=str(user.id),concept=("offHW"),value=(weapon))
    return

def lastrestart(signum,frame):
    data = {
        "signum":str(signum),
        "hora":datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    }
    Fire.put("/","Last_server_restart",data)
    Fire.put("/","players",PlayerDB)
    print("Datos guardados con éxito!")
    return


def main():
    global updater
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('start', register),
            MessageHandler(Filters.regex("^(⚔️Atacar)$"), beer),
            MessageHandler(Filters.regex("^(🗺Misiones)$"), misiones),
            MessageHandler(Filters.regex("^(🛡Defender)$"), duellingcourt),
            MessageHandler(Filters.regex("^(🏅Yo)$"), me),            
            MessageHandler(Filters.regex("^(🏰Castillo)$"), castillo),
            MessageHandler(Filters.regex("^(👥Clanes)$"), clan),
            MessageHandler(Filters.regex("^(🎲Dados)$"), luckyseven),
            MessageHandler(Filters.regex("^(📦Stock)$"), help),
            MessageHandler(Filters.regex("^(📋Lista)$"), help),
            MessageHandler(Filters.regex("^(ℹ️Otros)$"), help),
            MessageHandler(Filters.regex("^(🏕Misiones)$"), help),
            MessageHandler(Filters.regex("^(📝Ayudar)$"), help),
            MessageHandler(Filters.regex("^(🤝Alianza)$"), help),
            MessageHandler(Filters.regex("^(📝Ayudar)$"), help),
            MessageHandler(Filters.regex(r"^\/info_\d+$"), winfo),
            MessageHandler(Filters.regex("/inv"), inventario),
            MessageHandler(Filters.regex("/tiempo"), tiempo),
            MessageHandler(Filters.regex("/heroe"), heroe),
            MessageHandler(Filters.regex("^(🗡Armas)$"), owned),
            MessageHandler(Filters.regex(r"^\/on_\d+$"), equip),
            MessageHandler(Filters.regex("^(🏚Tienda)$"), shop),
            MessageHandler(Filters.regex(r"^\/info_\d+$"), winfo),
            MessageHandler(Filters.regex(r"^\/buy_\d+$"), buy),
            MessageHandler(Filters.regex("^(♨️Forjar)$"), forge),
            MessageHandler(Filters.regex("^(↩️Dejar)$"), register),
            MessageHandler(Filters.regex("^(/r)$"), reload),
            MessageHandler(Filters.regex(r"^\/info_\d+$"), winfo),
            CommandHandler('reload', reload),
            MessageHandler(Filters.text,register)
            ],

        states={
            # ME: []

            #BR: [MessageHandler(Filters.regex("^(👥 Talk)$"), connect)],

            # DC: [MessageHandler(Filters.regex("^(↩️Dejar)$"), register)],

            # BS: [],

            # L7: [MessageHandler(Filters.regex("^(↩️Dejar)$"), register)],

            HELP: [MessageHandler(Filters.regex("^(📝🏅Yo)$"), helpinfo),
                MessageHandler(Filters.regex("^(📝🍻Cerveza)$"), helpinfo),
                MessageHandler(Filters.regex("^(📝⚔️Duelo)$"), helpinfo),
                MessageHandler(Filters.regex("^(📝🏰Castillo)$"), helpinfo),
                MessageHandler(Filters.regex("^(📝🎲Dados)$"), helpinfo)],
            },

        fallbacks=[MessageHandler(Filters.regex("^(❌Cancelar)$"), register),
            MessageHandler(Filters.regex("^(↩️Volver)$"), register),
            MessageHandler(Filters.regex(r"^\/info_\d+$"), winfo),
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
