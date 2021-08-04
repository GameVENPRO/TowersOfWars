# Logging, para empezar a monitorear el desmadre desde el principio
import os
from re import I
import sys
from random import randint as rng, choice
from html import escape
import multiprocessing
import threading
from uuid import uuid4
import signal
import time
from datetime import datetime
import math
from tree import tree as tree
import FullWidth as fw
import Braile as br
import miscellaneous as misc
from time import sleep, time
import json
from drop_items import *
from dialogos import *
from game_logic import *
from cfg import *
from telegram.ext import *
from telegram import *
import logging
import random
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Librerías para interactuar con la API de Telegram
# Configuracion
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


# Librerías de utilidades


# Otras librerías para el desarrollo
# Base de Datos
Fire = Fire()

PlayerDB = Fire.get("/players", None)
# print(str(PlayerDB))
NivelesBD = Fire.get("/niveles_exp", None)
# print(str(NivelesBD))
TiendaDB = Fire.get("/tienda", None)
# print(str(TiendaDB))
RecursosDB = Fire.get("/recursos", None)
# print(str(storeDB))
categories = ["dagas", "espadas", "desafilados",
              "arcos", "cascos", "armaduras",
              "guantes", "botas", "escudos"]
tmpPlayers = {'0': 'null'}
ArenaList = {'0': 'null'}


class kb:
    def kb(op=None, args=None):
        IKB = InlineKeyboardButton
        IKB2 = KeyboardButton
        if(op == 'data'):
            keyboard = [[IKB("Join", callback_data=args)]]
        elif(op == 'dice'):
            keyboard = [[IKB("Roll", callback_data=args)]]
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
                    IKB("🗡Cabeza", callback_data="{\"op\":\"batt|mov:ah\",\"room\":\"%s\",\"host\":\"%s\"}" % (
                        args)),
                    IKB("🛡Cabeza", callback_data="{\"op\":\"batt|mov:dh\",\"room\":\"%s\",\"host\":\"%s\"}" % (
                        args))
                ],

                [
                    IKB("🗡Cuerpo", callback_data="{\"op\":\"batt|mov:ab\",\"room\":\"%s\",\"host\":\"%s\"}" % (
                        args)),
                    IKB("🛡Cuerpo", callback_data="{\"op\":\"batt|mov:db\",\"room\":\"%s\",\"host\":\"%s\"}" % (
                        args))
                ],

                [
                    IKB("🗡Pierna", callback_data="{\"op\":\"batt|mov:al\",\"room\":\"%s\",\"host\":\"%s\"}" % (
                        args)),
                    IKB("🛡Pierna", callback_data="{\"op\":\"batt|mov:dl\",\"room\":\"%s\",\"host\":\"%s\"}" % (
                        args))
                ],
            ]
        elif(op == 'wtypes'):
            keyboard = [
                [
                    IKB("Espadas",    callback_data="{\"op\":\"%s\",\"d1\":\"espadas\",\"d2\":\"%s\"}" % (
                        args)),
                    IKB("Dagas",   callback_data="{\"op\":\"%s\",\"d1\":\"dagas\",\"d2\":\"%s\"}" % (
                        args)),
                    IKB("Desafilados",      callback_data="{\"op\":\"%s\",\"d1\":\"desafilados\",\"d2\":\"%s\"}" % (
                        args))
                ],
                [
                    IKB("Arcos",  callback_data="{\"op\":\"%s\",\"d1\":\"arcos\",\"d2\":\"%s\"}" % (
                        args)),
                    IKB("Botas",   callback_data="{\"op\":\"%s\",\"d1\":\"botas\",\"d2\":\"%s\"}" % (
                        args)),
                    IKB("Armaduras",     callback_data="{\"op\":\"%s\",\"d1\":\"armaduras\",\"d2\":\"%s\"}" % (
                        args))
                ],
                [
                    IKB("Guantes",   callback_data="{\"op\":\"%s\",\"d1\":\"guantes\",\"d2\":\"%s\"}" % (
                        args)),
                    IKB("Lanzas",    callback_data="{\"op\":\"%s\",\"d1\":\"lanzas\",\"d2\":\"%s\"}" % (
                        args)),
                    IKB("Escudos",   callback_data="{\"op\":\"%s\",\"d1\":\"escudos\",\"d2\":\"%s\"}" % (
                        args))
                ],
                [
                    IKB("Cascos",   callback_data="{\"op\":\"%s\",\"d1\":\"cascos\",\"d2\":\"%s\"}" % (
                        args))
                ],
            ]
        else:
            keyboard = [[IKB("╔"), IKB("╗")], [IKB("╚"), IKB("╝")]]
        return keyboard

    def castillo_kb(level):
        IKB = KeyboardButton
        keyboard = [
            [
                IKB("⚒Taller"),
                IKB("🍺Taberna"),
                IKB("🛎Subasta" if(level >= 10) else ""),

            ],
            [
                IKB("⚖️Intercambio" if(level >= 10) else ""),
                IKB("🏚Tienda"),
                IKB("↩️Volver")
            ]
        ]

        return keyboard

    def ini_kb(level):
        IKB2 = KeyboardButton
        keyboard = [
            [
                IKB2("⚔️Atacar"),
                IKB2("🗺Misiones"),
                IKB2("🛡Defender")
            ],
            [
                IKB2("🏅Yo"),
                IKB2("🏰Castillo"),
                IKB2("👥Clanes" if(level >= 15) else "💬")
            ]
        ]

        return keyboard


class Player:
    def __init__(self, name, last_name, id):
        self.name = name
        self.last_name = last_name
        self.id = id
        self.link = (
            '<a href="tg://user?id={}">{}</a>'.format(id, escape(name))).strip()
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
            player = PlayerDB[str(self.id)]
            BolsoJG = player["bolso_arm"]
            self.mainW = BolsoJG[player["manoPrincipal"]]
            self.offHW = BolsoJG[player["mano"]]
        else:
            self.mainW = TiendaDB['01']
            self.offHW = TiendaDB['02']
        return

    def genAssign(self):
        pronouns = {
            'el': {
                'nomin': 'el',
                'object': 'él',
                'possAdj': 'su',
                'possPro': 'su',
                'reflex': 'suyo'
            },
            'ella': {
                'nomin': 'ella',
                'object': 'ella',
                'possAdj': 'ella',
                'possPro': 'suyo',
                'reflex': 'ella misma'
            },
            'se': {
                'nomin': 'se',
                'object': 'se',
                'possAdj': 'su',
                'possPro': 'su',
                'reflex': 'sí mismo'
            },
            'nos': {
                'nomin': 'nos',
                'object': 'nos',
                'possAdj': 'nuestro',
                'possPro': 'nosotros',
                'reflex': 'nosotros mismos'
            },
            'le': {
                'nomin': 'le',
                'object': 'ellos',
                'possAdj': 'su',
                'possPro': 'suyo',
                'reflex': 'ellos mismos'
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
    def __init__(self, room, P1, P2, text):
        self.room = room
        self.Players = {}
        self.Players[P1.id] = P1
        self.Players[P2.id] = P2
        self.round = 0
        self.text = text
        self.alive = False
        return

    def playersInfo(self):
        prs = {}
        for p in self.Players.keys():
            prs[p] = {**self.Players[p].to_dict()}
        return prs

    def movAssign(self, Pid, mov):
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
        p1, p2 = list(self.Players.keys())

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
        part = {'h': 'En la Cabeza', 'b': 'En el Cuerpo', 'l': ' En la Pierna'}
        crit = 1
        critxt = ""
        text = "\n<b>Ronda: %i</b>" % (self.round+1)
        t1 = self.Players[prs[0]].time
        t2 = self.Players[prs[1]].time

        if(t1 > t2):
            prs.reverse()
            if((t1-3) > t2):
                crit = (int(self.Players[prs[0]].mainW["crit"]) +
                        int(self.Players[prs[0]].offHW["crit"]))/2
                critxt = "<b>(*CRIT*💀)</b>"
        else:
            if((t2-3) > t1):
                crit = 1.5
                critxt = "<b>(*CRIT*💀)</b>"

        atk = self.Players[prs[0]].Atk
        df = self.Players[prs[1]].Def
        dam = self.atkdef(atk, df, crit)

        if(dam == 0):
            critxt = ""

        if(dam < 0):
            if(dam == -10):
                if(self.Players[prs[1]].hp >= 100):
                    self.Players[prs[1]].hp += dam
                text += '\n%s parece cansado de hacer algo, dando a %s tiempo para recuperar algo de salud(+%i❤️)' % (
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
                text += '\n%s me atraparon totalmente inconsciente por %s, permitir %s para tratar un <code>%s</code> en %s (%i).' % (
                    self.Players[prs[1]].name,
                    self.Players[prs[0]].name,
                    self.Players[prs[0]].name,
                    fw.toFullWidth("FATAL BLOW"),
                    self.Players[prs[1]].pron['object'],
                    dam

                )
            else:
                text += "\n%s Atacó a %s - %s con %s %s" % (
                    self.Players[prs[0]].name,
                    self.Players[prs[1]].name,
                    part[atk].lower(),
                    self.Players[prs[0]].pron['possAdj'],
                    self.Players[prs[0]].mainW["nombre"]
                )

                if(dam > 0):
                    text += ', trato %s%s daño.' % (
                        str(dam),
                        critxt
                    )

                else:
                    text += ', pero %s logró defender %s utilizando %s %s.' % (
                        self.Players[prs[1]].name,
                        self.Players[prs[1]].pron['reflex'],
                        self.Players[prs[1]].pron['possAdj'],
                        self.Players[prs[1]].offHW['nombre']
                    )
        self.Players[prs[1]].hp -= dam

        if(self.Players[prs[1]].hp > 0):
            atk = self.Players[prs[1]].Atk
            df = self.Players[prs[0]].Def
            dam = self.atkdef(atk, df, crit)

            if(dam < 0):
                if(dam == -10):
                    if(self.Players[prs[0]].hp >= 100):
                        self.Players[prs[0]].hp += dam
                    text += '\n%s parece cansado de hacer algo, dando %s tiempo para recuperar algo de salud(+%i❤️)' % (
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
                    text += '\n%s me atraparon totalmente inconsciente por %s, permitir %s para tratar un <code>%s</code> en %s.' % (
                        self.Players[prs[0]].name,
                        self.Players[prs[1]].name,
                        self.Players[prs[1]].name,
                        fw.toFullWidth("FATAL BLOW"),
                        self.Players[prs[0]].pron['object']

                    )
                else:
                    text += "\n%s Atacó a %s - %s con %s %s" % (
                        self.Players[prs[1]].name,
                        self.Players[prs[0]].name,
                        part[atk].lower(),
                        self.Players[prs[1]].pron['possAdj'],
                        self.Players[prs[1]].mainW["nombre"]
                    )

                    if(dam > 0):
                        text += ', trato %s daño.' % (
                            str(dam)
                        )

                    else:
                        text += ', pero %s logró defender %s usando %s %s.' % (
                            self.Players[prs[0]].name,
                            self.Players[prs[0]].pron['reflex'],
                            self.Players[prs[0]].pron['possAdj'],
                            self.Players[prs[0]].offHW['nombre']
                        )
            self.Players[prs[0]].hp -= dam
        else:
            self.Players[prs[1]].hp = 0
            text += "\n%s estaba demasiado débil para seguir luchando." % (
                self.Players[prs[1]].name)
        if(self.Players[prs[0]].hp < 0):
            self.Players[prs[0]].hp = 0
        return text+'\n'

    def atkdef(self, atk, df, crit):  # Dam (== -100), (-10), (== 0), (> 0), (== 100)
        if(atk == df):
            if(atk == 'nop'):
                return -100
            else:
                return 0
        elif(df == 'nop'):
            return 100
        else:
            if(atk == 'h'):
                return rng(15, 25)*crit
            elif(atk == 'b'):
                return rng(12, 20)*crit
            elif(atk == 'l'):
                return rng(5, 10)*crit
            else:  # atk == 'nop'
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
                "consiguió una victoria impecable contra {possAdj} oponente".format(
                    possAdj=self.Players[win].pron["possAdj"]),
                "Damas y caballeros, esta es la cara de un verdadero campeón!!!"
            ]
        elif(self.Players[win].hp > 66):
            status = [
                "Como si fuera un juego de niños,",
                "fácil de vencer",
                "en combate."]
        elif(self.Players[win].hp > 33):
            if(self.round > 5):
                length = "largo"
            else:
                length = "corto"
            status = [
                "Después de {} una batalla acalorada,".format(length),
                "fue capaz de adelantar",
                "en lo que parecía un partido emparejado."
            ]
        else:
            status = [
                "La pelea fue sangrienta y brutal, pero al final",
                "apenas podría superar {possAdj} oponente".format(
                    possAdj=self.Players[win].pron["possAdj"]),
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


def start(update: Update, context: CallbackContext):
    query = update.message.from_user
    text = """Te acercas y ves un cartel en la puerta:\n
            < i > Discúlpenos, por el momento esta bajo mantenimiento...
            <s>(cosas aleatorias pueden suceder debido a la física cuántica.)</s>
            Estaremos de negocios en un par de días...</me>
            \n"""
    update.message.reply_text(
        text,
        reply_markup=None,
        parse_mode=ParseMode.HTML
    )

    return


def register(update: Update, context: CallbackContext):
    user = update.message.from_user
    IKB = InlineKeyboardButton
    if(str(user.id) in list(PlayerDB.keys())):
        Juagador = PlayerDB[str(user.id)]
        level = Juagador["level"]
        welcometext = "Bienvenido de vuelta, {name}! \n¿Cómo puedo servirle hoy?".format(
            name=user.first_name)
        reply_markup = ReplyKeyboardMarkup(
            kb.ini_kb(level), resize_keyboard=True)

        update.message.reply_text(
            text=welcometext,
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )
        threading.Thread(target=updateUser, args=(user,)).start()
        return ConversationHandler.END
    else:
        text = "Elige el castillo al que jurarás lealtad 🗡"
        id_stiker = "CAACAgEAAxkBAAEB7BdgOA8VimAAATplEjtXp0IRxejpASoAAiwBAAJ9BsBFdTpwxjEI5z0eBA"

        reply_markup = InlineKeyboardMarkup([
            [
                IKB("🐉Escama de dragon", callback_data='{'+"\"op\":\"reg|gen\",\"d1\":\"{d1}\",\"d2\":\"{d2}\"".format(
                    d1='dragon', d2=str(user.id))+'}'),
                IKB("🌑Luz lunar", callback_data='{'+"\"op\":\"reg|gen\",\"d1\":\"{d1}\",\"d2\":\"{d2}\"".format(
                    d1='luna', d2=str(user.id))+'}')
            ],
            [
                IKB("🥔Papa", callback_data='{'+"\"op\":\"reg|gen\",\"d1\":\"{d1}\",\"d2\":\"{d2}\"".format(
                    d1='papa', d2=str(user.id))+'}'),
                IKB("🐺Manada de lobos", callback_data='{'+"\"op\":\"reg|gen\",\"d1\":\"{d1}\",\"d2\":\"{d2}\"".format(
                    d1='lobos', d2=str(user.id))+'}')
            ],
            [IKB("🦌Cuerno de ciervo", callback_data='{'+"\"op\":\"reg|gen\",\"d1\":\"{d1}\",\"d2\":\"{d2}\"".format(d1='ciervos', d2=str(user.id))+'}'),
             IKB("🦅Nido alto", callback_data='{'+"\"op\":\"reg|gen\",\"d1\":\"{d1}\",\"d2\":\"{d2}\"".format(
                 d1='agilas', d2=str(user.id))+'}'),
             ],
            [IKB("🦈Dientes de Tiburón", callback_data='{'+"\"op\":\"reg|gen\",\"d1\":\"{d1}\",\"d2\":\"{d2}\"".format(d1='tiburon', d2=str(user.id))+'}')
             ]
        ]
        )

        context.bot.send_sticker(chat_id=user.id, sticker=id_stiker)
        update.message.reply_text(
            text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)

        return


def reg(update: Update, context: CallbackContext):
    query = update.callback_query
    data = json.loads(query.data)
    option, next = data["op"].split("|")
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

        text = str('🎉Usted se une a los valientes guerreros del {fla}{castle}.\n\n'.format(fla=flag, castle=castillo)
                   + "Date prisa y únete al chat de nuestros jugadores: @TorreDeDiosRPG")

        try:
            context.bot.edit_message_reply_markup(
                chat_id=user.id,
                message_id=query.message.message_id,
                # inline_message_id=query.inline_message_id,
                reply_markup=None
            )
            reply_markup = ReplyKeyboardMarkup(
                kb.ini_kb(level), resize_keyboard=True)
            context.bot.send_message(
                chat_id=user.id,
                text=text,
                parse_mode=ParseMode.HTML,
                reply_markup=reply_markup)
            threading.Thread(target=newUser, args=(user, data["d1"],)).start()
        except Exception as e:
            error(update, e)
    return


def newUser(user, pron):
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
        "username": user.username,
        "nombre_hero": user.username,
        "castillo": castillo,
        "flag_casti": flag,
        "level": 1,
        "exp": 0,
        "ataque": 1,
        "defensa": 1,
        "resis_max": 5,
        "resis_min": 5,
        "vida_max": 300,
        "vida_min": 300,
        "mana_max": 0,
        "mana_min": 0,
        "oro": 0,
        "bol_oro": 0,
        "gemas": 0,
        "bolso_min": 0,
        "bolso": 15,
        "stock": 4000,
        "manoPrincipal": "None",
        "mano": "None",
        "casco": "None",
        "guantes": "None",
        "armadura": "None",
        "botas": "None",
        "especial": "None",
        "anillo": "None",
        "collar": "None",
        "pron": "el",
        "estado": "🛌Descanso",
        "puntos_habili": "0",
        "equipados_arm": [[0]],
        "bolso_arm": [[0]],
        "almacen_re": [[0]],
        "clase": [[0]],
        "mascota": "0",
        "rank": 0,
        "lastlog": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    }
    Fire.put("/players", user.id, info)
    PlayerDB[str(user.id)] = info
    # print(PlayerDB[str(user.id)])
    return


def keepAlive(update: Update, context: CallbackContext, arena: ArenaObject):
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
            # print("Reset!")
    #print("Time's up!")
    if(arena.movCheck()):
        arena.text += arena.dmgCalc()
        prs = list(arena.Players.keys())
        if((arena.Players[prs[0]].hp > 0) and (arena.Players[prs[1]].hp > 0)):
            text = "<b>⚔ Duelo ⚔</b>"+arena.text+"\n%s❤️ %s\nVs\n%s❤️ %s\n" % (
                arena.Players[prs[0]].hp,
                arena.Players[prs[0]].name,
                arena.Players[prs[1]].hp,
                arena.Players[prs[1]].name,
            )
            rpmkup = InlineKeyboardMarkup(kb.kb(op='hits', args=(room, host)))
            arena.movClear()
            arena.throwChronos()
            arena.round += 1
            threading.Thread(target=keepAlive, args=(
                update, context, arena,)).start()
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
        # print('retrying...')
        keepAlive(update, context, arena)
    return


def battle(update: Update, context: CallbackContext):
    global ArenaList, tmpPlayers
    query = update.callback_query
    data = json.loads(query.data)

    option, phase = data["op"].split("|")
    if("mov:" in phase):
        phase, mov = phase.split(":")
    room = data['room']
    host = int(data['host'])
    try:
        host_link = ('<a href="tg://user?id={}">{}</a>'.format(host,
                     escape(tmpPlayers[host]['first_name']))).strip()
    except KeyError as e:
        context.bot.answerCallbackQuery(
            query.id, "Esta sesión ha expirado.", True)
        context.bot.edit_message_text(
            text="<b>⚔Duelo⚔</b>\n<i>Una fuerte tormenta ha comenzado... Ambos combatientes han decidido posponer su lucha hasta que cese la tormenta...</i>",
            inline_message_id=query.inline_message_id,
            parse_mode=ParseMode.HTML)
        # error(update,e)
        return

    presser = update.effective_user
    presser_link = ('<a href="tg://user?id={}">{}</a>'.format(presser.id,
                    escape(presser.first_name))).strip()

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
            context.bot.answerCallbackQuery(
                query.id, '“'+choice(quotes)+'”', True)
            return
        else:
            text = '<b>⚔Duel</b>\n¡Ambos oponentes están listos! \n%s se enfrentará %s en la arena! \n<i>Que los dioses estén con ustedes, guerreros...</i>\n\nEsperando a que el anfitrión inicie el duelo...' % (
                host_link, presser_link)
            ArenaList[room] = ArenaObject(
                room=room,
                P1=Player(tmpPlayers[host]['first_name'],
                          tmpPlayers[host]['last_name'], host),
                P2=Player(presser.first_name, presser.last_name, presser.id),
                text='')
            context.bot.edit_message_text(
                text=text,
                inline_message_id=query.inline_message_id,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="Comience el partido!",
                                callback_data="{\"op\":\"batt|start\",\"room\":\"%s\",\"host\":\"%s\"}" % (
                                    room, host)
                            )
                        ]
                    ]
                ),
                parse_mode=ParseMode.HTML)
            return
    try:
        arena = ArenaList[room]  # From here on, there's only blood and glory!
    except KeyError as e:
        context.bot.answerCallbackQuery(
            query.id, "Esta sesión ha expirado.", True)
        context.bot.edit_message_text(
            text="<b>⚔Duelo</b>\n<i>Una fuerte tormenta ha comenzado... Ambos combatientes han decidido posponer su lucha hasta que cese la tormenta...</i>",
            inline_message_id=query.inline_message_id,
            parse_mode=ParseMode.HTML)
        # error(update,e)
        return

    if(presser.id not in list(arena.Players.keys())):
        context.bot.answerCallbackQuery(
            query.id, "¿Qué es lo que haces? Esta no es tu Lucha!", True)
        return
    elif(phase == 'start'):
        if(presser.id != host):
            context.bot.answerCallbackQuery(
                query.id, "Tienes que esperar a que el anfitrión inicie el partido.", True)
            return
        P1, P2 = arena.Players.keys()
        text = "<b>⚔Duelo</b>\nEl partido ha comenzado!\n%s❤️ %s\nVs\n%s❤️ %s\n\nRonda: %s\n¿Qué harás?\n<b>Elige puntos de ataque y defensa.</b>" % (
            str(int(arena.Players[P1].hp)),
            arena.Players[P1].name,
            str(int(arena.Players[P2].hp)),
            arena.Players[P2].name,
            arena.round+1)
        context.bot.edit_message_text(
            text=text,
            inline_message_id=query.inline_message_id,
            reply_markup=InlineKeyboardMarkup(
                kb.kb(op='hits', args=(room, host))),
            parse_mode=ParseMode.HTML)
        arena.throwChronos()
        threading.Thread(target=keepAlive, args=(
            update, context, arena,)).start()
        return

    elif(phase == 'mov'):
        act = {'a': 'Attack', 'd': 'Defend'}
        part = {'h': 'Head', 'b': 'Body', 'l': 'Legs'}
        mc = arena.movAssign(presser.id, mov)
        if(mc):
            context.bot.answerCallbackQuery(
                query.id, act[mov[0]]+' '+part[mov[1]], False)
            arena.alive = True
        else:
            context.bot.answerCallbackQuery(
                query.id, "Lo siento, ya elegiste qué %s" % (act[mov[0]]), True)
            return
        if(arena.movCheck()):
            battletext = arena.dmgCalc()
            arena.round += 1
            p1, p2 = list(arena.Players.keys())
            p1n = arena.Players[p1].link
            p1h = arena.Players[p1].hp

            p2n = arena.Players[p2].link
            p2h = arena.Players[p2].hp
            arena.text += battletext
            text = str("<b>⚔Duelo⚔</b>\n"
                       + "{btext}".format(btext=arena.text)
                       + "\n\n{health}❤️ {name}".format(health=str(math.ceil(p1h)), name=p1n)
                       + "\n\t\t\t\tVs"
                       + "\n{health}❤️ {name}\n".format(health=str(math.ceil(p2h)), name=p2n)
                       )
            if(p1h > 0 and p2h > 0):
                arena.movClear()
                arena.throwChronos()
                rpmkup = InlineKeyboardMarkup(
                    kb.kb(op='hits', args=(room, host)))
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
                error(update, e)
            return

    return
# Misiones


def misiones(update: Update, context: CallbackContext):
    global PlayerDB
    user = update.message.from_user
    player = PlayerDB[str(user.id)]
    level = player["level"]
    IKB = InlineKeyboardButton
    text = str('🌲Bosque 3min \n Pueden pasar muchas cosas en el bosque.\n\n')
    if(level >= 20):
        text += '🍄Pantano 4min\n'  # lvl 20
        text += 'Quién sabe lo que está al acecho en el barro.\n\n'
    if(level >= 20):
        text += '🏔Valle de Montaña 4min\n'  # lvl 20
        text += 'Cuidado con los deslizamientos de tierra.\n\n'
    if(level >= 3):
        text += '🗡Foray 🔋🔋 \n'  # Lvl3
        text += 'La incursión es una actividad peligrosa. Alguien puede notarlo y puede golpearlo. Pero si pasas desapercibido, conseguirás mucho botín. \n\n'
    if(level >= 5):
        text += '📯Arena \n'  # lvl.5
        text += 'Arena no es un lugar para débiles. Aquí luchas contra otros jugadores y si sales victorioso, adquieres una experiencia preciosa.'

    reply_markup = InlineKeyboardMarkup([
        [

            IKB("🌲Bosque", callback_data='{'+"\"op\":\"bosque|mbosq\",\"d1\":\"{d1}\",\"d2\":\"{d2}\"".format(
                d1='bosque', d2=str(user.id))+'}'),
            IKB("🍄Pantano" if(level >= 20) else "",
                callback_data='{'+"\"op\":\"pantano|mpant\",\"d1\":\"{d1}\",\"d2\":\"{d2}\"".format(d1='pantano', d2=str(user.id))+'}'),
            IKB("🏔Valle" if(level >= 20) else "",
                callback_data='{'+"\"op\":\"valle|mvalle\",\"d1\":\"{d1}\",\"d2\":\"{d2}\"".format(d1='valle', d2=str(user.id))+'}'),

        ],
        [
            IKB("🗡Foray" if(level >= 3) else "",
                callback_data='{'+"\"op\":\"foray|mforay\",\"d1\":\"{d1}\",\"d2\":\"{d2}\"".format(d1='foray', d2=str(user.id))+'}'),
            IKB("📯Arena" if(level >= 5) else "",
                callback_data='{'+"\"op\":\"arena|marena\",\"d1\":\"{d1}\",\"d2\":\"{d2}\"".format(d1='arena', d2=str(user.id))+'}')
        ]
    ]
    )
    update.message.reply_text(
        text,
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML
    )
    return


def bosque(update: Update, context: CallbackContext):
    global PlayerDB, RecursosDB
    query = update.callback_query
    data = json.loads(query.data)
    option, next = data["op"].split("|")
    user = query.from_user
    Jugador = PlayerDB[str(user.id)]
    resis_min = Jugador["resis_min"]

    if(next == 'mbosq'):
        if resis_min == 0:
            text = 'No hay suficiente resistencia. Vuelve después de descansar.\n\n'
            text += 'Para obtener más resistencia, invita a tus amigos al juego a '
            text += 'través del enlace de invitación.\n Pulse /promo para conseguirlo.'
            context.bot.send_message(
                chat_id=user.id, text=text, parse_mode=ParseMode.HTML, reply_markup=None)
        else:
            quitar_res(user, context)
            countdown = 5
            while countdown:
                m, s = divmod(countdown, 60)
                formato = '{:02d}:{:02d}'.format(m, s)
                if formato == "01:59":
                    upload(player=str(user.id), concept=("estado"),
                           value=("🌲En el bosque. Regreso en 1 minuto."))
                if formato == "00:59":
                    upload(player=str(user.id), concept=("estado"), value=(
                        "🌲En el bosque. Regreso en unos segundos."))
                if formato == "00:01":
                    upload(player=str(user.id), concept=(
                        "estado"), value=("🛌Descanso"))
                    quest_fina(user, context)
                countdown -= 1
                sleep(1)
    return


def quitar_res(user, context: CallbackContext):
    global PlayerDB
    Jugador = PlayerDB[str(user.id)]

    resx = str(int(Jugador["resis_min"]) - int(1))
    text = 'En una necesidad extrema de una aventura, fuiste a un bosque.\n Regresarás en 3 minutos.'
    upload(player=str(user.id), concept=("resis_min", "estado"),
           value=(resx, "🌲En el bosque. Regreso en 2 minutos."))
    context.bot.send_message(chat_id=user.id, text=text,
                             parse_mode=ParseMode.HTML, reply_markup=None)

    return


def quest_fina(user, context: CallbackContext):
    global PlayerDB, RecursosDB
    Jugador = PlayerDB[str(user.id)]
    Nivel = int(Jugador["level"])
    Almacen = Jugador["almacen_re"]
    ExpBase = int(NivelesBD[Nivel])
    exp_ganada = exp_bosque(Nivel, ExpBase)
    oro_win = random.randint(0, 4)
    dialogos = QUEST_BOSQUE_SUSS[random.randint(0, 29)]
    text = dialogos
    text += '\n\nObtubiste: <b>{exp}</b> y <b>{oro}</b> oro\n'.format(
        exp=exp_ganada, oro=oro_win)

    suma = int(Jugador["exp"]) + int(exp_ganada)
    suma_oro = int(Jugador["oro"]) + int(oro_win)
    veri_lvl(user, suma, context)
    upload(player=str(user.id), concept=("exp", "oro"), value=(suma, suma_oro))
    
    tiempo_d = "🌤"

    if tiempo_d == "🌤":
        rango = random.randint(1, 4)

        for i in range(rango):
            drps = REC_MAN[random.randint(0, 9)]
            cantida = random.randint(0, 3)
            items_d = drps
            itm_c = cantida
            if itm_c > 0 :
                if(str(items_d) in list(Almacen.keys())):
                    cal = int(Almacen[items_d]["cantidad"])+int(itm_c)
                    Newrecursos(user=user.id, items=items_d , cantidad=cal)
                    text += '\nGanaste: <b>{r}</b>({cant})'.format(r=RecursosDB[items_d]["nombre"], cant=itm_c)                
                else:
                    Newrecursos(user=user.id, items=items_d , cantidad=itm_c)
                    text += '\nGanaste: <b>{r}</b>({cant})'.format(r=RecursosDB[items_d]["nombre"], cant=itm_c)


    elif tiempo_d == "🌞":
        rango = random.randint(1, 4)

        for i in range(rango):
            drps = REC_MED[random.randint(0, 8)]
            cantida = random.randint(0, 3)
            items_d = drps
            itm_c = cantida
            text += '\nGanaste:<b>{r}</b>({cant})'.format(
                r=RecursosDB[items_d]["nombre"], cant=itm_c)

    elif tiempo_d == "⛅️":
        rango = random.randint(1, 4)

        for i in range(rango):
            drps = REC_TAD[random.randint(0, 10)]
            cantida = random.randint(0, 3)
            items_d = drps
            itm_c = cantida
            text += '\nGanaste:<b>{r}</b>({cant})'.format(
                r=RecursosDB[items_d]["nombre"], cant=itm_c)

    elif tiempo_d == "🌙":
        rango = random.randint(1, 4)

        for i in range(rango):
            drps = REC_NOC[random.randint(0, 9)]
            cantida = random.randint(0, 3)
            items_d = drps
            itm_c = cantida
            text += '\nGanaste:<b>{r}</b>({cant})'.format(
                r=RecursosDB[items_d]["nombre"], cant=itm_c)

    context.bot.send_message(chat_id=user.id, text=text,
                             parse_mode=ParseMode.HTML, reply_markup=None)
    return


def pantano(update: Update, context: CallbackContext):
    query = update.callback_query
    data = json.loads(query.data)
    option, next = data["op"].split("|")
    user = query.from_user
    text2 = 'Una aventura está llamando. Pero fuiste a un pantano.\n Regresarás en 6 minutos.'
    resx = str(int(PlayerDB[str(user.id)]["resis_min"]) - int(1))
    upload(player=str(user.id), concept=("resis_min", "estado"),
           value=(resx, "🍄Caminando por un pantano. En 3 minutos"))
    context.bot.send_message(chat_id=user.id, text=text2,
                             parse_mode=ParseMode.HTML, reply_markup=None)

    if(next == 'mpant'):
        countdown = 260
        while countdown:
            m, s = divmod(countdown, 60)
            formato = '{:02d}:{:02d}'.format(m, s)
            if formato == "01:59":
                upload(player=str(user.id), concept=("estado"), value=(
                    "🍄Caminando por un pantano. Regreso en 1 minuto."))
            if formato == "00:59":
                upload(player=str(user.id), concept=("estado"), value=(
                    "🍄Caminando por un pantano. Regreso en unos segundos."))
            if formato == "00:01":
                upload(player=str(user.id), concept=(
                    "estado"), value=("🛌Descanso"))

                text = 'De repente estabas rodeado por una enorme banda de orcos, liderados por un chamán Orco.\n'

            countdown -= 1
            sleep(1)

    try:
        context.bot.send_message(
            chat_id=user.id, text=text, parse_mode=ParseMode.HTML, reply_markup=None)

    except Exception as e:
        error(update, e)

    return


def valle(update: Update, context: CallbackContext):
    query = update.callback_query
    data = json.loads(query.data)
    option, next = data["op"].split("|")
    user = query.from_user
    text2 = 'Las montañas pueden ser un lugar peligroso.\nDecidiste investigar, qué está pasando.\n Regresarás en 4 minutos.'
    resx = str(int(PlayerDB[str(user.id)]["resis_min"]) - int(1))
    upload(player=str(user.id), concept=("resis_min", "estado"), value=(
        resx, "⛰Paseando por las montañas. Vuelvo en unos segundos."))
    context.bot.send_message(chat_id=user.id, text=text2,
                             parse_mode=ParseMode.HTML, reply_markup=None)

    if(next == 'mvalle'):
        countdown = 240
        while countdown:
            m, s = divmod(countdown, 60)
            formato = '{:02d}:{:02d}'.format(m, s)
            if formato == "01:59":
                upload(player=str(user.id), concept=("estado"), value=(
                    "⛰Paseando por las montañas. Vuelvo en 1 minuto."))
            if formato == "00:59":
                upload(player=str(user.id), concept=("estado"), value=(
                    "⛰Paseando por las montañas. Vuelvo en unos segundos."))
            if formato == "00:01":
                upload(player=str(user.id), concept=(
                    "estado"), value=("🛌Descanso"))

                text = 'De repente estabas rodeado por una enorme banda de orcos, liderados por un chamán Orco.\n'

            countdown -= 1
            sleep(1)

    try:
        context.bot.send_message(
            chat_id=user.id, text=text, parse_mode=ParseMode.HTML, reply_markup=None)

    except Exception as e:
        error(update, e)

    return


def foray(update: Update, context: CallbackContext):
    query = update.callback_query
    data = json.loads(query.data)
    option, next = data["op"].split("|")
    user = query.from_user
    text2 = 'Sintiendo una lujuria insatisfactoria por la violencia te diriges al pueblo más cercano.\n Llegará a la más cercana en 4 minutos.'
    resx = str(int(PlayerDB[str(user.id)]["resis_min"]) - int(2))
    upload(player=str(user.id), concept=("resis_min", "estado"),
           value=(resx, "🗡Incursión. Estará de vuelta en 2 minutos"))
    context.bot.send_message(chat_id=user.id, text=text2,
                             parse_mode=ParseMode.HTML, reply_markup=None)

    if(next == 'mforay'):
        countdown = 260
        while countdown:
            m, s = divmod(countdown, 60)
            formato = '{:02d}:{:02d}'.format(m, s)
            if formato == "01:59":
                upload(player=str(user.id), concept=("estado"), value=(
                    "🗡Incursión. Estará de vuelta en 1 minutos"))
            if formato == "00:59":
                upload(player=str(user.id), concept=("estado"), value=(
                    "🗡Incursión. Estará de vuelta en unos segundos"))
            if formato == "00:01":
                upload(player=str(user.id), concept=(
                    "estado"), value=("🛌Descanso"))

                text = 'De repente estabas rodeado por una enorme banda de orcos, liderados por un chamán Orco.\n'

            countdown -= 1
            sleep(1)

    try:
        context.bot.send_message(
            chat_id=user.id, text=text, parse_mode=ParseMode.HTML, reply_markup=None)

    except Exception as e:
        error(update, e)

    return


def arena(update: Update, context: CallbackContext):
    query = update.callback_query
    data = json.loads(query.data)
    option, next = data["op"].split("|")
    user = query.from_user
    if(next == 'marena'):
        text = '📯 Bienvenido a Arena!\n'
        text += 'El aire sucio está empapado con el espeso olor de la sangre.\n'
        text += 'Nadie termina aquí por accidente: no puedes irte una vez que comienzas tu batalla.\n'
        text += 'Espero que tu espada esté afilada y tu escudo firme.\n\n'
        text += 'Su rango: 893\nTus peleas: 0/5\n\n'
        text += 'Clasificación de combate: /top 5\nCrecimiento más rápido: /top 6\n\n'
        text += 'Precio de la entrada: 5 💰'

    try:
        context.bot.send_message(
            chat_id=user.id, text=text, parse_mode=ParseMode.HTML, reply_markup=None)

    except Exception as e:
        error(update, e)

    return


def queryHandler(update: Update, context: CallbackContext):
    query = update.callback_query
    data = json.loads(query.data)
    option, next = data["op"].split("|")
    # print(tree(update.to_dict(),HTML=False))
    ##print("Acá elijo qué se va a hacer :9")
    if(option == "batt"):
        threading.Thread(target=battle, args=(update, context,)).start()
        ##print("Acá fue battle!")
    if(option == "dice"):
        threading.Thread(target=dice, args=(update, context,)).start()
    if(option == "reg"):
        threading.Thread(target=reg, args=(update, context,)).start()
    if(option == "owned"):
        threading.Thread(target=owned, args=(update, context,)).start()
    if(option == "bsmith"):
        threading.Thread(target=shopcat, args=(update, context,)).start()
    if(option == "bosque"):
        threading.Thread(target=bosque, args=(update, context,)).start()
    if(option == "pantano"):
        threading.Thread(target=pantano, args=(update, context,)).start()
    if(option == "valle"):
        threading.Thread(target=valle, args=(update, context,)).start()
    if(option == "foray"):
        threading.Thread(target=foray, args=(update, context,)).start()
    if(option == "arena"):
        threading.Thread(target=arena, args=(update, context,)).start()
    return


def inlinequery(update: Update, context: CallbackContext):
    # Handle the inline query.
    global tmpPlayers
    query = update.inline_query
    target = update.inline_query.from_user
    target_name = ('<a href="tg://user?id={}">{}</a>'.format(target.id,
                   escape(target.first_name))).strip()
    reply_markup = None
    tmpPlayers[target.id] = {
        'first_name': target.first_name,
        'last_name': target.last_name,
        'username': target.username}
    # print(tree(update.to_dict()))

    results = [
        InlineQueryResultArticle(
            id=uuid4(),
            title="⚔Duelo",
            reply_markup=InlineKeyboardMarkup(kb.kb(op="data", args="{\"op\":\"batt|p2\",\"room\":\"%s\",\"host\":\"%s\"}" % (
                str(int(list(ArenaList.keys())[-1])+1), str(target.id)))),
            input_message_content=InputTextMessageContent(
                message_text="<b>⚔Duelo</b>\n{} está buscando un oponente digno...{}".format(
                    target_name, "\n\n<code>También puede registrarse en</code>@Torre_RPGBot<code> para personalizarte...</code>"),
                parse_mode=ParseMode.HTML,
                reply_markup=reply_markup,
            )
        ),
        InlineQueryResultArticle(
            id=uuid4(),
            title="🎲Dados",
            reply_markup=InlineKeyboardMarkup(kb.kb(
                op="dice", args="{\"op\":\"dice|dice\",\"next\":\"dice\",\"room\":\"%s\"}" % (target.username))),
            input_message_content=InputTextMessageContent(
                message_text="Pulsar <i>\"Roll\"</i> para rodar los dados...",
                parse_mode=ParseMode.HTML,
                reply_markup=reply_markup
            ),

        ),
        InlineQueryResultArticle(
            id=uuid4(),
            title="🍺Cerveza",
            input_message_content=InputTextMessageContent(
                message_text="Se le da un frasco lleno de cerveza espumosa🍺.\n{}: <i>Brindemos por el placer de estar aquí y ahora!</i>".format(
                    target_name),
                parse_mode=ParseMode.HTML
            )
        )
    ]
    if("&Codify" in query.query):
        txt = query.query.replace("&Codify ", "")
        txt = br.toBraile(txt)
        results.append(
            InlineQueryResultArticle(
                id=uuid4(),
                title="⠨⠉⠕⠝⠧⠑⠗⠞⠖",
                input_message_content=InputTextMessageContent(
                    message_text=txt,
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
                input_message_content=InputTextMessageContent(
                    message_text="<b>Join the {} Tournament!</b>\n\nPlayers:\n".format(
                        query.query.title()),
                    parse_mode=ParseMode.HTML
                    #reply_markup = reply_markup,
                )
            )
        )
    context.bot.answer_inline_query(
        update.inline_query.id, results=results,
        cache_time=1,
        is_personal=True,
        switch_pm_text='Enter the Tavern',
        switch_pm_parameter='register')
    # update.inline_query.answer(results)
    return


def dice(update: Update, context: CallbackContext):
    query = update.callback_query
    data = json.loads(query.data)
    d1 = rng(1, 6)
    d2 = rng(1, 6)
    dir = "/utils/dice"
    Dices = ["⚀", "⚁", "⚂", "⚃", "⚄", "⚅"]
    D1 = Dices[d1-1]
    D2 = Dices[d2-1]
    add = ""
    if(d1+d2 == 7):
        add = " ¡¡Dados!!"
    text = "{} tiró los dados, y...\nLos dados muestran {}({}) y {}({})...\n<b>{} conseguir {}{}!</b>\n\n".format(
        query.from_user.first_name,
        D1, d1,
        D2, d2,
        query.from_user.first_name,
        d1+d2,
        add
    )
    # print(text)
    context.bot.edit_message_text(
        text=text,
        inline_message_id=query.inline_message_id,
        parse_mode=ParseMode.HTML
    )
    return


def me(update: Update, context: CallbackContext):
    global PlayerDB
    user = update.message.from_user
    player = PlayerDB[str(user.id)]
    level = player["level"]
    habilidad = player["puntos_habili"]
    exp_niveles = NivelesBD[level]
    bolso_arm = len(player["bolso_arm"])-1
    Total_ataque,Total_defensa,Suma = equipamiento_heroe(user)
    text = ""
    if(int(habilidad) > 0):
        text += "\n🌟Congratulations Felicitaciones! Nuevo nivel!🌟"
        text += "\n\nAsignar puntos /level_up"
        # text+="\nBatlla"
        # text+="\n\n"

    text += "{fla}".format(fla=player["flag_casti"])
    # text+="[LSD]"
    text += "{name}".format(name=user.first_name)
    text += " Del Castillo {castillo}".format(castillo=player["castillo"])
    text += "\n🏅Nivel: {level}".format(level=str(player["level"]))
    text += "\n⚔️Ataque: {ataq}".format(ataq=str(player["ataque"]))
    text += "🛡Defensa: {defensa}".format(defensa=str(player["defensa"]))
    text += "\n🔥Exp: {exp}".format(exp=str(player["exp"]))
    text += "/{exp_niv}".format(exp_niv=str(exp_niveles))
    text += "\n❤️Vida: {vdmin}".format(vdmin=str(player["vida_min"]))
    text += "/{vdmax}".format(vdmax=str(player["vida_max"]))
    text += "\n🔋Resistencia:{rsmin}".format(rsmin=str(player["resis_min"]))
    text += "/{rsmax}".format(rsmax=str(player["resis_max"]))
    text += "⏰{rege}min".format(rege="00")
    if(player["mana_max"] > 0):
        text += "\n💧Mana:{mnamin}".format(mnamin=str(player["mana_min"]))
        text += "/{mnamax}".format(mnamax=str(player["mana_max"]))
    text += "\n💰{oro}".format(oro=player["oro"])
    if(player["bol_oro"] > 0):
        text += "👝{bol_oro}".format(bol_oro=str(player["bol_oro"]))
    text += "💎{gemas}".format(gemas=player["gemas"])
    text += "\n\n🎽Euipamiento:"
    if(Suma == 0):
            text += "[-]"
    else:
        if(Total_ataque > 0):
            text += "+{t}⚔️".format(t=Total_ataque)
        if(Total_defensa > 0):
            text += "+{td}🛡".format(td=Total_defensa)
            
    text += "\n🎒Balso: {total}".format(total="0" if bolso_arm == 0 else bolso_arm)
    text += "/{bolso} ".format(bolso=player["bolso"])
    text += "/inv"
    # +"Mascota:{money}".format(money=player["money"])
    text += "\n\nEstado:\n{estado}".format(estado=player["estado"])
    text += "\n\nMás: /heroe"

    reply_markup = ReplyKeyboardMarkup(kb.ini_kb(level), resize_keyboard=True)

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
    BolsoJG = player["bolso_arm"]
    level = player["level"]
    exp_niveles = NivelesBD[level]
    bolso_arm = len(player["bolso_arm"])-1
    alma_re = len(player["almacen_re"])-1
    Total_ataque,Total_defensa,Suma = equipamiento_heroe(user)
    
    text = "{fla}".format(fla=player["flag_casti"])
    # text+="[LSD]"
    text += "{name}".format(name=user.first_name)
    text += "\n🏅Nivel: {level}".format(level=str(player["level"]))
    text += "\n⚔️Ataque: {ataq}".format(ataq=str(player["ataque"]))
    text += "🛡Defensa: {defensa}".format(defensa=str(player["defensa"]))
    text += "\n🔥Exp: {exp}".format(exp=str(player["exp"]))
    text += "/{exp_niv}".format(exp_niv=str(exp_niveles))
    text += "\n❤️Vida: {vdmin}".format(vdmin=str(player["vida_min"]))
    text += "/{vdmax}".format(vdmax=str(player["vida_max"]))
    text += "\n🔋Resistencia:{rsmin}".format(rsmin=str(player["resis_min"]))
    text += "/{rsmax}".format(rsmax=str(player["resis_max"]))
    if(player["mana_max"] > 0):
        text += "\n💧Mana:{mnamin}".format(mnamin=str(player["mana_min"]))
        text += "/{mnamax}".format(mnamax=str(player["mana_max"]))
    text += "\n💰{oro}".format(oro=player["oro"])
    if(player["bol_oro"] > 0):
        text += "👝{bol_oro}".format(bol_oro=str(player["bol_oro"]))
    text += "💎{gemas}".format(gemas=player["gemas"])

    text += "\n📚Especializaciónes:"
    if(level <= 14):
        text += "-"
    if(level >= 15):

        text += "📕"
    if(level >= 25):

        text += "📗"
    if(level >= 35):

        text += "📘"
    if(level >= 45):

        text += "📙"
    if(level >= 60):

        text += "📒"

    text += "\n🎉Logro: /ach"
    if(level >= 20):
        text += "\n⚒Clase Info: /class"
    else:
        text += "\n🏛Clase Info: /class"

    if(level >= 20):
        text += "\n🚹Male"

    #text+="\n\n✨Efectos: /effects"
    # +"Mascota:{money}".format(money=player["money"])

    text += "\n\n🎽Euipamiento:"
    if(Suma == 0):
        text += "[-]"
    else:
        if(Total_ataque > 0):
            text += "+{t}⚔️".format(t=Total_ataque)
        if(Total_defensa > 0):
            text += "+{td}🛡".format(td=Total_defensa)

    if(player["manoPrincipal"] != "None"):
        p = player["manoPrincipal"]
        nombre = str(BolsoJG[p]["nombre"])
        ataque = int(BolsoJG[p]["atributos"]["ataque"])
        defensa = int(BolsoJG[p]["atributos"]["defensa"])
        text += "\n{n} ".format(n=nombre)
        if(ataque > 0):
            text += "+{d}⚔️".format(d=ataque)
        if(defensa > 0):
            text += "+{d}🛡".format(d=defensa)
        text += " /off_{id}".format(id=p)
    if(player["mano"] != "None"):
        p2 = int(player["mano"])
        nombre2 = str(BolsoJG[p2]["nombre"])
        ataque2 = int(BolsoJG[p2]["atributos"]["ataque"])
        defensa2 = int(BolsoJG[p2]["atributos"]["defensa"])
        text += "\n{n} ".format(n=nombre2)
        if(ataque2 > 0):
            text += "+{d}⚔️".format(d=ataque2)
        if(defensa2 > 0):
            text += "+{d}🛡".format(d=defensa2)
        text += " /off_{id}".format(id=p2)
    if(player["casco"] != "None"):
        p3 = int(player["casco"])
        nombre3 = str(BolsoJG[p3]["nombre"])
        ataque3 = int(BolsoJG[p3]["atributos"]["ataque"])
        defensa3 = int(BolsoJG[p3]["atributos"]["defensa"])
        text += "\n{n} ".format(n=nombre3)
        if(ataque3 > 0):
            text += "+{d}⚔️".format(d=ataque3)
        if(defensa3 > 0):
            text += "+{d}🛡".format(d=defensa3)
        text += " /off_{id}".format(id=p3)
    if(player["guantes"] != "None"):
        p4 = int(player["guantes"])
        nombre4 = str(BolsoJG[p4]["nombre"])
        ataque4 = int(BolsoJG[p4]["atributos"]["ataque"])
        defensa4 = int(BolsoJG[p4]["atributos"]["defensa"])
        text += "\n{n} ".format(n=nombre4)
        if(ataque4 > 0):
            text += "+{d}⚔️".format(d=ataque4)
        if(defensa4 > 0):
            text += "+{d}🛡".format(d=defensa4)
        text += " /off_{id}".format(id=p4)
    if(player["armadura"] != "None"):
        p5 = int(player["armadura"])
        nombre5 = str(BolsoJG[p5]["nombre"])
        ataque5 = int(BolsoJG[p5]["atributos"]["ataque"])
        defensa5 = int(BolsoJG[p5]["atributos"]["defensa"])
        text += "\n{n} ".format(n=nombre5)
        if(ataque5 > 0):
            text += "+{d}⚔️".format(d=ataque5)
        if(defensa5 > 0):
            text += "+{d}🛡".format(d=defensa5)
        text += " /off_{id}".format(id=p5)
    if(player["botas"] != "None"):
        p6 = int(player["botas"])
        nombre6 = str(BolsoJG[p6]["nombre"])
        ataque6 = int(BolsoJG[p6]["atributos"]["ataque"])
        defensa6 = int(BolsoJG[p6]["atributos"]["defensa"])
        text += "\n{n} ".format(n=nombre6)
        if(ataque6 > 0):
            text += "+{d}⚔️".format(d=ataque6)
        if(defensa6 > 0):
            text += "+{d}🛡".format(d=defensa6)
        text += " /off_{id}".format(id=p6)
    if(player["especial"] != "None"):
        p7 = int(player["especial"])
        nombre7 = str(BolsoJG[p7]["nombre"])
        ataque7 = int(BolsoJG[p7]["atributos"]["ataque"])
        defensa7 = int(BolsoJG[p7]["atributos"]["defensa"])
        text += "\n{n} ".format(n=nombre7)
        if(ataque7 > 0):
            text += "+{d}⚔️".format(d=ataque7)
        if(defensa7 > 0):
            text += "+{d}🛡".format(d=defensa7)
        text += " /off_{id}".format(id=p7)
    if(player["anillo"] != "None"):
        p8 = int(player["anillo"])
        nombre8 = str(BolsoJG[p8]["nombre"])
        ataque8 = int(BolsoJG[p8]["atributos"]["ataque"])
        defensa8 = int(BolsoJG[p8]["atributos"]["defensa"])
        text += "\n{n} ".format(n=nombre8)
        if(ataque8 > 0):
            text += "+{d}⚔️".format(d=ataque8)
        if(defensa8 > 0):
            text += "+{d}🛡".format(d=defensa8)
        text += " /off_{id}".format(id=p8)
    if(player["collar"] != "None"):
        p9 = int(player["collar"])
        nombre9 = str(BolsoJG[p9]["nombre"])
        ataque9 = int(BolsoJG[p9]["atributos"]["ataque"])
        defensa9 = int(BolsoJG[p9]["atributos"]["defensa"])
        text += "\n{n} ".format(n=nombre9)
        if(ataque9 > 0):
            text += "+{d}⚔️".format(d=ataque9)
        if(defensa9 > 0):
            text += "+{d}🛡".format(d=defensa9)
        text += " /off_{id}".format(id=p9)

    text += "\n\n🎒Balso: {total}".format(
        total="0" if bolso_arm == 0 else bolso_arm)
    text += "/{bolso} ".format(bolso=player["bolso"])
    text += "/almc"
    text += "\n\n📦Almacen: {total} /stock".format(total=alma_re)

    reply_markup = ReplyKeyboardMarkup(kb.ini_kb(level), resize_keyboard=True)

    update.message.reply_text(
        text=text,
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML
    )
    return


def inventario(update: Update, context: CallbackContext):
    global PlayerDB
    user = update.message.from_user
    player = PlayerDB[str(user.id)]
    BolsoJG = player["bolso_arm"]
    level = player["level"]
    bolso_arm = len(player["bolso_arm"])-1
    Total_ataque,Total_defensa,Suma = equipamiento_heroe(user)

    
    text = "\n\n🎽Euipamiento:"
    if(Suma == 0):
            text += "[-]"
    else:
        if(Total_ataque > 0):
            text += "+{t}⚔️".format(t=Total_ataque)
        if(Total_defensa > 0):
            text += "+{td}🛡".format(td=Total_defensa)
    
    
    if(player["manoPrincipal"] != "None"):
        p = player["manoPrincipal"]
        nombre = str(BolsoJG[p]["nombre"])
        ataque = int(BolsoJG[p]["atributos"]["ataque"])
        defensa = int(BolsoJG[p]["atributos"]["defensa"])
        text += "\n{n} ".format(n=nombre)
        if(ataque > 0):
            text += "+{d}⚔️".format(d=ataque)
        if(defensa > 0):
            text += "+{d}🛡".format(d=defensa)
        text += " /off_{id}".format(id=p)
    if(player["mano"] != "None"):
        p2 = int(player["mano"])
        nombre2 = str(BolsoJG[p2]["nombre"])
        ataque2 = int(BolsoJG[p2]["atributos"]["ataque"])
        defensa2 = int(BolsoJG[p2]["atributos"]["defensa"])
        text += "\n{n} ".format(n=nombre2)
        if(ataque2 > 0):
            text += "+{d}⚔️".format(d=ataque2)
        if(defensa2 > 0):
            text += "+{d}🛡".format(d=defensa2)
        text += " /off_{id}".format(id=p2)
    if(player["casco"] != "None"):
        p3 = int(player["casco"])
        nombre3 = str(BolsoJG[p3]["nombre"])
        ataque3 = int(BolsoJG[p3]["atributos"]["ataque"])
        defensa3 = int(BolsoJG[p3]["atributos"]["defensa"])
        text += "\n{n} ".format(n=nombre3)
        if(ataque3 > 0):
            text += "+{d}⚔️".format(d=ataque3)
        if(defensa3 > 0):
            text += "+{d}🛡".format(d=defensa3)
        text += " /off_{id}".format(id=p3)
    if(player["guantes"] != "None"):
        p4 = int(player["guantes"])
        nombre4 = str(BolsoJG[p4]["nombre"])
        ataque4 = int(BolsoJG[p4]["atributos"]["ataque"])
        defensa4 = int(BolsoJG[p4]["atributos"]["defensa"])
        text += "\n{n} ".format(n=nombre4)
        if(ataque4 > 0):
            text += "+{d}⚔️".format(d=ataque4)
        if(defensa4 > 0):
            text += "+{d}🛡".format(d=defensa4)
        text += " /off_{id}".format(id=p4)
    if(player["armadura"] != "None"):
        p5 = int(player["armadura"])
        nombre5 = str(BolsoJG[p5]["nombre"])
        ataque5 = int(BolsoJG[p5]["atributos"]["ataque"])
        defensa5 = int(BolsoJG[p5]["atributos"]["defensa"])
        text += "\n{n} ".format(n=nombre5)
        if(ataque5 > 0):
            text += "+{d}⚔️".format(d=ataque5)
        if(defensa5 > 0):
            text += "+{d}🛡".format(d=defensa5)
        text += " /off_{id}".format(id=p5)
    if(player["botas"] != "None"):
        p6 = int(player["botas"])
        nombre6 = str(BolsoJG[p6]["nombre"])
        ataque6 = int(BolsoJG[p6]["atributos"]["ataque"])
        defensa6 = int(BolsoJG[p6]["atributos"]["defensa"])
        text += "\n{n} ".format(n=nombre6)
        if(ataque6 > 0):
            text += "+{d}⚔️".format(d=ataque6)
        if(defensa6 > 0):
            text += "+{d}🛡".format(d=defensa6)
        text += " /off_{id}".format(id=p6)
    if(player["especial"] != "None"):
        p7 = int(player["especial"])
        nombre7 = str(BolsoJG[p7]["nombre"])
        ataque7 = int(BolsoJG[p7]["atributos"]["ataque"])
        defensa7 = int(BolsoJG[p7]["atributos"]["defensa"])
        text += "\n{n} ".format(n=nombre7)
        if(ataque7 > 0):
            text += "+{d}⚔️".format(d=ataque7)
        if(defensa7 > 0):
            text += "+{d}🛡".format(d=defensa7)
        text += " /off_{id}".format(id=p7)
    if(player["anillo"] != "None"):
        p8 = int(player["anillo"])
        nombre8 = str(BolsoJG[p8]["nombre"])
        ataque8 = int(BolsoJG[p8]["atributos"]["ataque"])
        defensa8 = int(BolsoJG[p8]["atributos"]["defensa"])
        text += "\n{n} ".format(n=nombre8)
        if(ataque8 > 0):
            text += "+{d}⚔️".format(d=ataque8)
        if(defensa8 > 0):
            text += "+{d}🛡".format(d=defensa8)
        text += " /off_{id}".format(id=p8)
    if(player["collar"] != "None"):
        p9 = int(player["collar"])
        nombre9 = str(BolsoJG[p9]["nombre"])
        ataque9 = int(BolsoJG[p9]["atributos"]["ataque"])
        defensa9 = int(BolsoJG[p9]["atributos"]["defensa"])
        text += "\n{n} ".format(n=nombre9)
        if(ataque9 > 0):
            text += "+{d}⚔️".format(d=ataque9)
        if(defensa9 > 0):
            text += "+{d}🛡".format(d=defensa9)
        text += " /off_{id}".format(id=p9)

    text += "\n🎒Balso: ({total}".format(total="0" if bolso_arm ==
                                        0 else bolso_arm)
    text += "/{bolso})".format(bolso=player["bolso"])
    p = 1
    n = bolso_arm + 1
    for i in BolsoJG[p:n]:
        if(BolsoJG[p]["estatus"] != 1):
            text += "\n<b>{name}</b> ".format(name=BolsoJG[p]["nombre"])
            if(BolsoJG[p]["atributos"]["ataque"] > 0):
                text += "<b>+{actaque}</b>⚔️".format(
                    actaque=BolsoJG[p]["atributos"]["ataque"])
            if(BolsoJG[p]["atributos"]["defensa"] > 0):
                text += "<b>+{defensa}</b>🛡".format(
                    defensa=BolsoJG[p]["atributos"]["defensa"])
            text += " /on_{id}".format(id=p)

        p = p+1

    reply_markup = ReplyKeyboardMarkup(kb.ini_kb(level), resize_keyboard=True)

    update.message.reply_text(
        text=text,
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML
    )
    return

def equipamiento_heroe(user):
    global PlayerDB
    player = PlayerDB[str(user.id)]
    BolsoJG = player["bolso_arm"]

    a = 0   
    a2 = 0   
    a3 = 0   
    a4 = 0   
    a5 = 0   
    a6 = 0   
    a7 = 0   
    a8 = 0   
    a9 = 0   
    d1 = 0
    d2 = 0
    d3 = 0
    d4 = 0
    d5 = 0
    d6 = 0
    d7 = 0
    d8 = 0
    d9 = 0
    Total_ataque = 0
    Total_defensa = 0

    if(player["manoPrincipal"]!="None"):
        a =int(BolsoJG[player["manoPrincipal"]]["atributos"]["ataque"])
        d1 =int(BolsoJG[player["manoPrincipal"]]["atributos"]["defensa"])
    if(player["mano"]!="None"):        
        a2 =int(BolsoJG[player["mano"]]["atributos"]["ataque"])
        d2 =int(BolsoJG[player["mano"]]["atributos"]["defensa"])
    if(player["casco"]!="None"):    
        a3 =int(BolsoJG[player["casco"]]["atributos"]["ataque"])
        d3 =int(BolsoJG[player["casco"]]["atributos"]["defensa"])
    if(player["guantes"]!="None"):    
        a4 =int(BolsoJG[player["guantes"]]["atributos"]["ataque"])
        d4 =int(BolsoJG[player["guantes"]]["atributos"]["defensa"])
    if(player["armadura"]!="None"):    
        a5 =int(BolsoJG[player["armadura"]]["atributos"]["ataque"])
        d5 =int(BolsoJG[player["armadura"]]["atributos"]["defensa"])
    if(player["botas"]!="None"):    
        a6 =int(BolsoJG[player["botas"]]["atributos"]["ataque"])
        d6 =int(BolsoJG[player["botas"]]["atributos"]["defensa"])
    if(player["especial"]!="None"):    
        a7 =int(BolsoJG[player["especial"]]["atributos"]["ataque"])
        d7 =int(BolsoJG[player["especial"]]["atributos"]["defensa"])
    if(player["anillo"]!="None"):    
        a8 =int(BolsoJG[player["anillo"]]["atributos"]["ataque"])
        d8 =int(BolsoJG[player["anillo"]]["atributos"]["defensa"])
    if(player["collar"]!="None"):    
        a9 =int(BolsoJG[player["collar"]]["atributos"]["ataque"])
        d9 =int(BolsoJG[player["collar"]]["atributos"]["defensa"])



    Total_ataque = a + a2 + a3 + a4 + a5 + a6 + a7 + a8 + a9 
    Total_defensa = d1 + d2 + d3 + d4 + d5 + d6 + d7 + d8 + d9 
    Suma = Total_ataque + Total_defensa
    
    return Total_ataque,Total_defensa,Suma

def veri_lvl(user, suma, context: CallbackContext):
    global PlayerDB
    Jugador = PlayerDB[str(user.id)]
    Nivel = int(Jugador["level"])
    NuevoLvl = int(int(Jugador["level"]) + int(1))
    BaseExp = NivelesBD[Nivel]
    id_stiker = "CAACAgIAAxkBAAECq25hBsf94hWfsIYFTtjlY1ZW2JjVNAACiQAD6st5AuZbw2Z4SeORIAQ"
    if suma >= BaseExp:
        upload(player=str(user.id), concept=("level"), value=(NuevoLvl))
        context.bot.send_sticker(chat_id=user.id, sticker=id_stiker)

    return

def obtener_estadisticas_hero(user):
    global PlayerDB
    player = PlayerDB[str(user.id)]
    BolsoJG = player["bolso_arm"]
    d_max = player["defensa"]
    a_min = player["ataque"]
    lvl = player["level"]
    exp_base = NivelesBD[lvl+1]

    return (d_max, a_min, exp_base, lvl)


def winfo(update: Update, context: CallbackContext):
    global TiendaDB
    try:
        weapon = TiendaDB[update.message.text.replace("/info_", "")]
        # print(str(weapon))
        text = str(
            "<b>⚜️ {name} ⚜️</b>".format(name=weapon["nombre"])
            + "\n\n<i>“{lore}”</i>\n".format(lore=weapon["historia"])
            + "\n"+"\t"*4 +
            " Ataque: <code>{atk}</code>".format(
                atk=str(int(weapon["atributos"]["ataque"])))
            + "\n"+"\t"*4 +
            " Defensa: <code>{df}</code>".format(
                df=str(int(weapon["atributos"]["defensa"])))
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


def owned(update: Update, context: CallbackContext):
    try:
        user = update.message.from_user
        data = {"op": "owned|na", "d1": "sword", "d2": "null"}
    except:
        user = update.callback_query.from_user
        data = json.loads(update.callback_query.data)

    player = PlayerDB[str(user.id)]
    text = "<b>{name}'s {type} tipo de armas:</b>\n".format(
        name=user.first_name, type=data["d1"])
    weapons = False
    for w in [*player["bolso_arm"]]:
        try:
            if(TiendaDB[w]["g_type"] == data["d1"]):
                text += "\n"+"\t"*4 + \
                    "► {name} /info_{id} \n\t\t\t\t\t\t\t\tEquip: /on_{id}".format(
                        name=TiendaDB[w]["nombre"], id=w)
                weapons = True
        except:
            player["bolso_arm"].remove(None)
            continue

    if(weapons == False):
        text += "\n"+"\t"*4+"<b>((Vacio))</b>"
    reply_markup = InlineKeyboardMarkup(
        kb.kb(op="wtypes", args=("owned|na", "null")))
    try:
        update.message.reply_text(
            text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )
    except Exception as e:
        context.bot.edit_message_text(
            text=text,
            chat_id=user.id,
            message_id=update.callback_query.message.message_id,
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )
    return


def equip(update: Update, context: CallbackContext):
    user = update.message.from_user
    Jugador = PlayerDB[str(user.id)]
    BolsoJG = Jugador["bolso_arm"]
    weapon = update.message.text.replace("/on_", "")

    # if(weapon not in BolsoJG):
   #     return
   # else:
    #    if(weapon not in list(BolsoJG[weapon])):
    # text = "¡No eres el dueño de esta arma!"
    # else:
    wpassign(int(weapon), user)
    text = "<b>{weapon}</b> equipado con éxito!".format(
        weapon=BolsoJG[int(weapon)]["nombre"])

    update.message.reply_text(
        text=text,
        parse_mode=ParseMode.HTML
    )
    return


def equipoff(update: Update, context: CallbackContext):
    user = update.message.from_user
    Jugador = PlayerDB[str(user.id)]
    BolsoJG = Jugador["bolso_arm"]
    weapon = update.message.text.replace("/off_", "")

    if(BolsoJG[int(weapon)]["estatus"] == 0):
        text = "<b>[Acción Inválida]</b>"
    elif(int(weapon) == Jugador["manoPrincipal"]):
        """"Desactivar Arma"""
        uploadwp(player=str(user.id), w=(int(weapon)),
                 concept=("estatus"), value=(0))
        upload(player=str(user.id), concept=("manoPrincipal"), value=("None"))
        text = "<b>{weapon}</b> Quitado con éxito!".format(
            weapon=BolsoJG[int(weapon)]["nombre"])
    elif(int(weapon) == Jugador["mano"]):
        """"Desactivar Arma"""
        uploadwp(player=str(user.id), w=(int(weapon)),
                 concept=("estatus"), value=(0))
        upload(player=str(user.id), concept=("mano"), value=("None"))
        text = "<b>{weapon}</b> Quitado con éxito!".format(
            weapon=BolsoJG[int(weapon)]["nombre"])
    elif(int(weapon) == Jugador["casco"]):
        """"Desactivar Arma"""
        uploadwp(player=str(user.id), w=(int(weapon)),
                 concept=("estatus"), value=(0))
        upload(player=str(user.id), concept=("casco"), value=("None"))
        text = "<b>{weapon}</b> Quitado con éxito!".format(
            weapon=BolsoJG[int(weapon)]["nombre"])
    elif(int(weapon) == Jugador["guantes"]):
        """"Desactivar Arma"""
        uploadwp(player=str(user.id), w=(int(weapon)),
                 concept=("estatus"), value=(0))
        upload(player=str(user.id), concept=("guantes"), value=("None"))
        text = "<b>{weapon}</b> Quitado con éxito!".format(
            weapon=BolsoJG[int(weapon)]["nombre"])
    elif(int(weapon) == Jugador["armadura"]):
        """"Desactivar Arma"""
        uploadwp(player=str(user.id), w=(int(weapon)),
                 concept=("estatus"), value=(0))
        upload(player=str(user.id), concept=("armadura"), value=("None"))
        text = "<b>{weapon}</b> Quitado con éxito!".format(
            weapon=BolsoJG[int(weapon)]["nombre"])
    elif(int(weapon) == Jugador["botas"]):
        """"Desactivar Arma"""
        uploadwp(player=str(user.id), w=(int(weapon)),
                 concept=("estatus"), value=(0))
        upload(player=str(user.id), concept=("botas"), value=("None"))
        text = "<b>{weapon}</b> Quitado con éxito!".format(
            weapon=BolsoJG[int(weapon)]["nombre"])
    elif(int(weapon) == Jugador["especial"]):
        """"Desactivar Arma"""
        uploadwp(player=str(user.id), w=(int(weapon)),
                 concept=("estatus"), value=(0))
        upload(player=str(user.id), concept=("especial"), value=("None"))
        text = "<b>{weapon}</b> Quitado con éxito!".format(
            weapon=BolsoJG[int(weapon)]["nombre"])
    elif(int(weapon) == Jugador["anillo"]):
        """"Desactivar Arma"""
        uploadwp(player=str(user.id), w=(int(weapon)),
                 concept=("estatus"), value=(0))
        upload(player=str(user.id), concept=("anillo"), value=("None"))
        text = "<b>{weapon}</b> Quitado con éxito!".format(
            weapon=BolsoJG[int(weapon)]["nombre"])
    elif(int(weapon) == Jugador["collar"]):
        """"Desactivar Arma"""
        uploadwp(player=str(user.id), w=(int(weapon)),
                 concept=("estatus"), value=(0))
        upload(player=str(user.id), concept=("collar"), value=("None"))
        text = "<b>{weapon}</b> Quitado con éxito!".format(
            weapon=BolsoJG[int(weapon)]["nombre"])

    update.message.reply_text(
        text=text,
        parse_mode=ParseMode.HTML
    )
    return


def wpassign(weapon, user):
    Jugador = PlayerDB[str(user.id)]
    BolsoJG = Jugador["bolso_arm"]
    WpAc = Jugador["manoPrincipal"]
    WpAc2 = Jugador["mano"]
    slot = ""
    if(BolsoJG[weapon]["g_type"] in ["espadas", "lanzas", "arcos", "desafilados"]):
        slot = "manoPrincipal"
    elif(BolsoJG[weapon]["g_type"] in ["dagas", "escudos", "flechas", "antorcha"]):
        slot = "mano"
    elif(BolsoJG[weapon]["g_type"] == "cascos"):
        slot = "casco"
    elif(BolsoJG[weapon]["g_type"] == "guantes"):
        slot = "guantes"
    elif(BolsoJG[weapon]["g_type"] == "armaduras"):
        slot = "armadura"
    elif(BolsoJG[weapon]["g_type"] == "botas"):
        slot = "botas"
    elif(BolsoJG[weapon]["g_type"] == "especiales"):
        slot = "especial"
    elif(BolsoJG[weapon]["g_type"] == "anillos"):
        slot = "anillo"
    elif(BolsoJG[weapon]["g_type"] == "collares"):
        slot = "collar"

    if(slot == "manoPrincipal"):
        if(Jugador["manoPrincipal"] == "None"):
            """"Colocar Arma Nueva"""
            uploadwp(player=str(user.id), w=(weapon),
                     concept=("estatus"), value=(1))
            upload(player=str(user.id), concept=(
                "manoPrincipal"), value=(weapon))

        else:

            """Desactivar armar puesta y cambiar estatus del arma puesta"""
            uploadwp(player=str(user.id), w=(WpAc),
                     concept=("estatus"), value=(0))
            """"Colocar Arma Nueva"""
            uploadwp(player=str(user.id), w=(weapon),
                     concept=("estatus"), value=(1))
            upload(player=str(user.id), concept=(
                "manoPrincipal"), value=(weapon))

    elif(slot == "mano"):
        if(Jugador["mano"] == "None"):
            """Cambia normalmente"""
            uploadwp(player=str(user.id), w=(weapon),
                     concept=("estatus"), value=(1))
            upload(player=str(user.id), concept=("mano"), value=(weapon))
        else:

            """Desactivar armar puesta y cambiar estatus del arma puesta"""
            uploadwp(player=str(user.id), w=(
                Jugador["mano"]), concept=("estatus"), value=(0))
            """"Colocar Arma Nueva"""
            uploadwp(player=str(user.id), w=(weapon),
                     concept=("estatus"), value=(1))
            upload(player=str(user.id), concept=("mano"), value=(weapon))
    elif(slot == "casco"):
        if(Jugador["casco"] == "None"):
            """Cambia normalmente"""
            uploadwp(player=str(user.id), w=(weapon),
                     concept=("estatus"), value=(1))
            upload(player=str(user.id), concept=("casco"), value=(weapon))
        else:

            """Desactivar armar puesta y cambiar estatus del arma puesta"""
            uploadwp(player=str(user.id), w=(
                Jugador["casco"]), concept=("estatus"), value=(0))
            """"Colocar Arma Nueva"""
            uploadwp(player=str(user.id), w=(weapon),
                     concept=("estatus"), value=(1))
            upload(player=str(user.id), concept=("casco"), value=(weapon))
    elif(slot == "guantes"):
        if(Jugador["guantes"] == "None"):
            """Cambia normalmente"""
            uploadwp(player=str(user.id), w=(weapon),
                     concept=("estatus"), value=(1))
            upload(player=str(user.id), concept=("guantes"), value=(weapon))
        else:

            """Desactivar armar puesta y cambiar estatus del arma puesta"""
            uploadwp(player=str(user.id), w=(
                Jugador["guantes"]), concept=("estatus"), value=(0))
            """"Colocar Arma Nueva"""
            uploadwp(player=str(user.id), w=(weapon),
                     concept=("estatus"), value=(1))
            upload(player=str(user.id), concept=("guantes"), value=(weapon))
    elif(slot == "armadura"):
        if(Jugador["armadura"] == "None"):
            """Cambia normalmente"""
            uploadwp(player=str(user.id), w=(weapon),
                     concept=("estatus"), value=(1))
            upload(player=str(user.id), concept=("armadura"), value=(weapon))
        else:

            """Desactivar armar puesta y cambiar estatus del arma puesta"""
            uploadwp(player=str(user.id), w=(
                Jugador["armadura"]), concept=("estatus"), value=(0))
            """"Colocar Arma Nueva"""
            uploadwp(player=str(user.id), w=(weapon),
                     concept=("estatus"), value=(1))
            upload(player=str(user.id), concept=("armadura"), value=(weapon))
    elif(slot == "botas"):
        if(Jugador["botas"] == "None"):
            """Cambia normalmente"""
            uploadwp(player=str(user.id), w=(weapon),
                     concept=("estatus"), value=(1))
            upload(player=str(user.id), concept=("botas"), value=(weapon))
        else:

            """Desactivar armar puesta y cambiar estatus del arma puesta"""
            uploadwp(player=str(user.id), w=(
                Jugador["botas"]), concept=("estatus"), value=(0))
            """"Colocar Arma Nueva"""
            uploadwp(player=str(user.id), w=(weapon),
                     concept=("estatus"), value=(1))
            upload(player=str(user.id), concept=("botas"), value=(weapon))
    elif(slot == "especial"):
        if(Jugador["especial"] == "None"):
            """Cambia normalmente"""
            uploadwp(player=str(user.id), w=(weapon),
                     concept=("estatus"), value=(1))
            upload(player=str(user.id), concept=("especial"), value=(weapon))
        else:

            """Desactivar armar puesta y cambiar estatus del arma puesta"""
            uploadwp(player=str(user.id), w=(
                Jugador["especial"]), concept=("estatus"), value=(0))
            """"Colocar Arma Nueva"""
            uploadwp(player=str(user.id), w=(weapon),
                     concept=("estatus"), value=(1))
            upload(player=str(user.id), concept=("especial"), value=(weapon))
    elif(slot == "anillo"):
        if(Jugador["anillo"] == "None"):
            """Cambia normalmente"""
            uploadwp(player=str(user.id), w=(weapon),
                     concept=("estatus"), value=(1))
            upload(player=str(user.id), concept=("mano"), value=(weapon))
        else:

            """Desactivar armar puesta y cambiar estatus del arma puesta"""
            uploadwp(player=str(user.id), w=(
                Jugador["anillo"]), concept=("estatus"), value=(0))
            """"Colocar Arma Nueva"""
            uploadwp(player=str(user.id), w=(weapon),
                     concept=("estatus"), value=(1))
            upload(player=str(user.id), concept=("anillo"), value=(weapon))
    elif(slot == "collar"):
        if(Jugador["collar"] == "None"):
            """Cambia normalmente"""
            uploadwp(player=str(user.id), w=(weapon),
                     concept=("estatus"), value=(1))
            upload(player=str(user.id), concept=("collar"), value=(weapon))
        else:

            """Desactivar armar puesta y cambiar estatus del arma puesta"""
            uploadwp(player=str(user.id), w=(
                Jugador["collar"]), concept=("estatus"), value=(0))
            """"Colocar Arma Nueva"""
            uploadwp(player=str(user.id), w=(weapon),
                     concept=("estatus"), value=(1))
            upload(player=str(user.id), concept=("collar"), value=(weapon))

    return

# Clima y tiempo
def tiempo(update: Update, context: CallbackContext):
    hora = datetime.hour    # Fecha y hora actual
    anno = datetime.year
    m = datetime.month
    dia =datetime.day
    min = datetime.minute

    text = "<b>En el mundo de Chat Wars ahora</b>"

    # if  m == 01:
    #     mes = "Wintar "
    #     #    Invierno 31"
    # if  m == 02:
    #     mes = "Hornung "
    #     #   Invierno 28"
    # if  m == 03:
    #     mes = "estrellas"
    #     #  Primavera 30"
    # if m == 05:
    #     mes = " Winni "
    #     # Primavera 31"
    # if m == 06:
    #     mes = "Brāh "
    #     # Verano 30"
    # if m == 07:
    #     mes = "Hewi "
    #     #  Verano 31"
    # if m == 08:
    #     m = "Aran "
    #     # Verano 31"
    # if m == 09:
    #     mes = "Witu "
    #     # Otoño 30"
    # if m == 10:
    #     mes = "Wīndume "
    #     # Otoño 31"
    # if m == 11:
    #     mes = "Herbista "
    #     # Otoño 30"
    # if m == 12:
    #     mes = " Hailag "
    #     # Invierno 31"

    # if(hora == 00):
    #     text += "\n🌤Mañana"
    # elif(hora == 01):
    #     text += "\n🌞Día"
    # elif(hora == 02):
    #     text += "\n🌞Día"
    # elif(hora == 03):
    #     text += "\n⛅️Tarde"
    # elif(hora == 04):
    #     text += "\n⛅️Tarde"
    # elif(hora == 05):
    #     text += "\n🌙Noche"
    # elif(hora == 06):
    #     text += "\n🌙Noche"
    # elif(hora == 07):
    #     text += "\n🌤Mañana"
    # elif(hora == 08):
    #     text += "\n🌤Mañana"
    # elif(hora == 09):
    #     text += "\n🌞Día"
    # elif(hora == 10):
    #     text += "\n🌞Día"
    # elif(hora == 11):
    #     text += "\n⛅️Tarde"
    # elif(hora == 12):
    #     text += "\n⛅️Tarde"
    # elif(hora == 13):
    #     text += "\n🌙Noche"
    # elif(hora == 14):
    #     text += "\n🌙Noche"
    # elif(hora == 15):
    #     text += "\n🌤Mañana"
    # elif(hora == 16):
    #     text += "\n🌤Mañana"
    # elif(hora == 17):
    #     text += "\n🌞Día"
    # elif(hora == 18):
    #     text += "\n🌞Día"
    # elif(hora == 19):
    #     text += "\n⛅️Tarde"
    # elif(hora == 20):
    #     text += "\n⛅️Tarde"
    # elif(hora == 21):
    #     text += "\n🌙Noche"
    # elif(hora == 22):
    #     text += "\n🌙Noche"
    # elif(hora == 23):
    #     text += "\n🌤Mañana"

    # text += "\n{h}:{m}".format(h=hora, m=min)

    # text += "\n{d} {m} {a}".format(d=dia, m=mes, a=anno)

    text += "\n\n<b>Pronóstico del tiempo</b>"
    text += "\n[{clima}] No funciona xd".format(clima=climas())

    reply_markup = ReplyKeyboardMarkup(kb.kb("start"), resize_keyboard=True)

    update.message.reply_text(
        text=text,
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML
    )
    return

# Castillo
def castillo(update: Update, context: CallbackContext):
    global PlayerDB
    user = update.message.from_user
    player = PlayerDB[str(user.id)]
    level = player["level"]
    hora = str(datetime.hour)
    text = "El Castillo \n"

    if(hora == "00"):
        text += "🌤Mañana"
    elif (hora == "01"):
        text += "🌞Día"
    elif (hora == "02"):
        text += "🌞Día"
    elif (hora == "03"):
        text += "⛅️Tarde"
    elif (hora == "04"):
        text += "⛅️Tarde"
    elif (hora == "05"):
        text += "🌙Noche"
    elif (hora == "06"):
        text += "🌙Noche"
    elif(hora == "07"):
        text += "🌤Mañana"
    elif(hora == "08"):
        text += "🌤Mañana"
    elif (hora == "09"):
        text += "🌞Día"
    elif (hora == "10"):
        text += "🌞Día"
    elif (hora == "11"):
        text += "⛅️Tarde"
    elif (hora == "12"):
        text += "⛅️Tarde"
    elif (hora == "13"):
        text += "🌙Noche"
    elif (hora == "14"):
        text += "🌙Noche"
    elif(hora == "15"):
        text += "🌤Mañana"
    elif(hora == "16"):
        text += "🌤Mañana"
    elif (hora == "17"):
        text += "🌞Día"
    elif (hora == "18"):
        text += "🌞Día"
    elif (hora == "19"):
        text += "⛅️Tarde"
    elif (hora == "20"):
        text += "⛅️Tarde"
    elif (hora == 21):
        text += "🌙Noche"
    elif (hora == "22"):
        text += "🌙Noche"
    elif(hora == "23"):
        text += "🌤Mañana"

    # text+="[-→-]"
    text += "\n\n💬Castle Chat del castillo: "
    text += "\nLos demás: /otros"
    text += "\n\n🍺La taberna abre por la noche"

    reply_markup = ReplyKeyboardMarkup(
        kb.castillo_kb(level), resize_keyboard=True)

    update.message.reply_text(
        text=text,
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML
    )
    return

def shop(update: Update, context: CallbackContext):
    text = str("¡Mira esto, hombre! Aquí tenemos suficientes armas para cazar un dragón, o para atacar un templo maldito!"
               + "\nEcha un vistazo a lo que quieras, y si algo te interesa, no dudes en preguntar!")
    reply_markup = InlineKeyboardMarkup(kb.kb("wtypes", ("bsmith|na", "null")))
    update.message.reply_text(
        text=text,
        reply_markup=reply_markup,
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
        text = "<b>Aquí, algunas mercancías:</b>\n"
        for w in list(set(TiendaDB.keys())):
            if(int(w) < 100):
                # print(str(TiendaDB[w]["g_type"]))
                if(TiendaDB[w]["g_type"] == data["d1"]):
                    text += "\n\n<b>{name}</b> ".format(
                        name=TiendaDB[w]["nombre"], id=TiendaDB[w]["id"])
                    if(TiendaDB[w]["atributos"]["ataque"] > 0):
                        text += "<b>+{actaque}</b>⚔️".format(
                            actaque=TiendaDB[w]["atributos"]["ataque"])
                    if(TiendaDB[w]["atributos"]["defensa"] > 0):
                        text += "<b>+{defensa}</b>🛡".format(
                            defensa=TiendaDB[w]["atributos"]["defensa"])
                    if(TiendaDB[w]["tier"] == 1):
                        text += "\nRequerido: 📕"
                    text += "\n{precio}💰 \n/buy_{id}".format(
                        precio=TiendaDB[w]["precio"], id=w)
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

def buy(update: Update, context: CallbackContext):
    global PlayerDB
    user = update.message.from_user
    player = PlayerDB[str(user.id)]
    weapon = update.message.text.replace("/buy_", "")
    try:
        if(weapon not in player["bolso_arm"]):
            if(int(player["oro"]) >= int(TiendaDB[weapon]["precio"])):
                # player["bolso_arm"].append(weapon)
                Newcompra(user=user.id, items=weapon)
                wps = player["bolso_arm"]
                oro = str(int(PlayerDB[str(user.id)]["oro"]
                              ) - int(TiendaDB[weapon]["precio"]))
                upload(player=str(user.id), concept=(
                    "bolso_arm", "oro"), value=(wps, oro))
                text = "Ja, ja! Este <b>{weapon}</b> te queda muy bien, amigo! \nUtilizar sabiamente!".format(
                    weapon=TiendaDB[weapon]["nombre"])
            else:
                text = "Lo siento amigo, pero parece que no puedes permitirte este artículo."

            update.message.reply_text(
                text=text,
                parse_mode=ParseMode.HTML
            )
    except Exception as e:
        error(update, e)
    else:
        return
    return

def Newcompra(user, items):
    global PlayerDB, TiendaDB
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


def Newrecursos(user, items, cantidad):
    global PlayerDB, RecursosDB
    Jugador = PlayerDB[str(user)]


    info = {       
            "id": RecursosDB[items]["id"],
            "elaboracion": RecursosDB[items]["elaboracion"],
            "peso": RecursosDB[items]["peso"],
            "tipo": RecursosDB[items]["tipo"],
            "nombre": RecursosDB[items]["nombre"],
            "cantidad": cantidad,
            "costo": 0                
            }

    Fire.put("/players/"+str(user)+"/almacen_re",items,info)
 
    return

# def casino(update: Update, context: CallbackContext):

#     if message.text == '🤑 Casino':
#         bot.send_message(message.chat.id, "Bienvenido al casino! No te olvides de elegir una apuesta! (original 20 $)\n"
#                          + "Tu cuenta corriente " + str(slot_machine.credit) + " $!\n" +
#                          "¡Es hora de comenzar el juego! - >¡Tira de la palanca!", reply_markup=markup_casino)
#     if message.text == "¡Tire de la palanca! 💰":
#         if slot_machine.cash >= slot_machine.credit:
#             bot.send_message(message.chat.id, "¡La apuesta es demasiado alta!\ npóngase en una apuesta para continuar el juego.",
#                              reply_markup=markup_casino)
#         elif slot_machine.credit >= 15 and slot_machine.credit - slot_machine.cash > 0:
#             bot.send_message(message.chat.id, "Tu apuesta " + str(slot_machine.cash) + " $!\n" +
#                              slot_machine.play_game() + "\n"
#                              + "Tu cuenta corriente " + str(slot_machine.credit) + " $\n"
#                              , reply_markup=markup_casino)
#             if slot_machine.flag:
#                 bot.send_message(message.chat.id, "Felicidades, has ganado " + str(slot_machine.total_won) + " $!",
#                                  reply_markup=markup_casino)
#         else:
#             bot.send_message(message.chat.id, "No hay fondos suficientes para continuar el juego.\n" +
#                              "Por desgracia, viajero, este es tu juego. ¡Entra la próxima vez!",
#                              reply_markup=markup_casino)
#     elif message.text == "Cambiar la apuesta":
#         bot.send_message(message.chat.id, "Introduzca una nueva apuesta (no menos de 15)!", reply_markup=markup_casino)
#     elif message.text == "Leyes del juego 📝":
#         bot.send_message(message.chat.id, "¡Saludos, jugador! El juego es muy simple, cada movimiento del juego pasa"
#                                           " en 4 etapas:\n"
#                          + "1) Pulsando El botón para tirar de la palanca! 💰 inicia la máquina.\ n se Cancela la apuesta, se muestra"
#                          + " campo de juego 3x3 y por suerte (random honesto) el dinero o se pierde"
#                          + " o se multiplican.\n2) Si el jugador quiere cambiar la apuesta, sólo tiene que hacer clic "
#                          + "en el Botón cambiar apuesta o marcar el número deseado en la ubicación para el conjunto de mensajes.\n" +
#                          "3) los Ganadores son filas de 3 elementos individuales ubicados:\nen horizontal\n 🍒🍒 🍒\n"
#                          + "vertical\n🍏\n🍏\n🍏\nen diagonal\n7️⃣\n    7️⃣\n         7️⃣\n"
#                          + "4) las Ganancias se calculan a partir del cálculo de la apuesta * factor de categoría:\n" +
#                          " 7️⃣ - 5, 🍒 - 3, 🍏 - 1.5, 🔔- 1\nSi la tasa excede la cantidad de fondos disponibles,"
#                          + " la notificación apropiada se mostrará en la pantalla de diálogo.\ n ¡Buen juego!",
#                          reply_markup=markup_casino)
#     elif message.text == "Salir del casino":
#         bot.send_message(message.chat.id, "¡Nos vemos, viajero!\n¿Pero a dónde voy ahora?",
#                          reply_markup=main_menu_keyboard)
#     elif int(message.text) % 1 == 0 and int(message.text) >= 15:
#         if int(message.text) < slot_machine.credit:
#             slot_machine.cash = int(message.text)
#             bot.send_message(message.chat.id, "Nueva apuesta " + message.text + "$ ¡aceptada!", reply_markup=markup_casino)
#         else:
#             bot.send_message(message.chat.id, "No se acepta la apuesta. Fondos insuficientes: " +
#                              str(slot_machine.credit), reply_markup=markup_casino)
#     else:
#         bot.send_message(message.chat.id, "Viajero, aparentemente eres de tierras muy lejanas. No entendí nada.",
#                          reply_markup=markup_casino)

def ata_castillo(update: Update, context: CallbackContext):
    text = 'No esta Disponible'
    update.message.reply_text(text=text)
    return

def def_castillo(update: Update, context: CallbackContext):
    text = 'No esta Disponible'
    update.message.reply_text(text=text)
    return

def cominicacion(update: Update, context: CallbackContext):
    text = "📯Comunicación con otros castillos\n Únete a @TorreDeDiosRPG y empieza a hablar con los ciudadanos de los siete castillos.\n\n"
    text += "📢Nuevas Noticias del juego\n Únase a @TorreDeDiosRPG para mantenerse al día con las últimas actualizaciones.\n\n"
    text += "📊Ranking\n Jugadores: /top\n Castillos: /worldtop\n Gremios: /guildtop\n"
    text += "✏️Nombre del juego\n Para cambiar tu nombre en el bot del juego, escribe / name seguido de tu nuevo nombre\n"
    text += "Ejemplo:\n /nombre Jon Snow\n\n 🚹Masculino. Género en el juego. \n"
    text += "No hay manera de cambiar los textos y menciones en el mundo del juego severo. Pero puede cambiar todos los gráficos disponibles.\n"
    text += "Comando: /gender_change\n"
    text += "Advertencia! Solo el primer intento es gratis. Siguiente le costará 💎15"

    IKB = KeyboardButton
    reply_markup = ReplyKeyboardMarkup(kb.kb("start"), resize_keyboard=True)

    update.message.reply_text(
        text=text,
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML
    )
    return

# Taller

def taller(update: Update, context: CallbackContext):
    text = "Your recipes:"
    IKB = KeyboardButton

    reply_markup = ReplyKeyboardMarkup(
        [

            [
                IKB("⚒Mesa de trabajo"),
                IKB("📖Fórmulas")

            ],
            [
                IKB("🏷Envolver"),
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

def mesa_trabajo(update: Update, context: CallbackContext):
    text = "⚒En su banco de trabajo puede encontrar:"
    text += "[vacio]"
    text += "Su stock:"
    text += "[vacio]"

    IKB = KeyboardButton

    reply_markup = ReplyKeyboardMarkup(
        [

            [
                IKB("⚒Artesanía"),
                IKB("📖Fórmulas")

            ],
            [
                IKB("❌Reiniciar"),
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

def craf(update: Update, context: CallbackContext):
    text = "No esta disponible"
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
    text = "Your recipes:"
    IKB = KeyboardButton

    reply_markup = ReplyKeyboardMarkup(
        [

            [
                IKB("⚒Mesa de trabajo"),
                IKB("📖Fórmulas")

            ],
            [
                IKB("🏷Envolver"),
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

def envolver(update: Update, context: CallbackContext):
    text = "Puedes envolver:"
    text += "Espada de madera (1)"
    text += "Requiere 1🏷"
    text += "Wrap: / wrap_w01"
    IKB = KeyboardButton

    reply_markup = ReplyKeyboardMarkup(
        [

            [
                IKB("⚒Mesa de trabajo"),
                IKB("📖Fórmulas")

            ],
            [
                IKB("🏷Envolver"),
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

# Taberna
def taberna(update: Update, context: CallbackContext):
    text = "Entras en la vieja Taberna de mofetas, ruidosa y abarrotada como siempre. Al lado de la barra se ven algunos "
    text = "soldados presumiendo de las últimas noticias de las líneas de batalla. En la parte de atrás de la taberna algunos"
    text = "granjeros están jugando a los dados."
    text += "Usted puede comprar una pinta de cerveza y sentarse al lado de los soldados: tomar un descanso, "
    text = "escuchar algunos chismes. Si tienes suerte, es posible que escuches algo interesante."
    text += "Precio de una pinta: 3 p"
    text += "O usted puede sentarse al lado de los jugadores y probar suerte en los dados."
    text += "Cuota de inscripción: 10💰"

    IKB = KeyboardButton

    reply_markup = ReplyKeyboardMarkup(
        [

            [
                IKB("🍺Tomar"),
                IKB("🎲Jugar a los dados")

            ],
            [
                IKB("Hablar con el extraño"),
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

def beber_cerveza(update: Update, context: CallbackContext):
    text = "Tomaste una cerveza fría. Ahora puedes sentarte"
    text += "y escuchar lo que la gente tiene que decir. Terminarás tu bebida en 5 minutos."

    IKB = KeyboardButton

    reply_markup = ReplyKeyboardMarkup(
        [

            [
                IKB("🍺Tomar"),
                IKB("📖Fórmulas")

            ],
            [
                IKB("🏷Envolver"),
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


def juagar_dados(update: Update, context: CallbackContext):
    text = "Tomaste una cerveza fría. Ahora puedes sentarte"
    text += "y escuchar lo que la gente tiene que decir. Terminarás tu bebida en 5 minutos."

    IKB = KeyboardButton

    reply_markup = ReplyKeyboardMarkup(
        [

            [
                IKB("🍺Tomar"),
                IKB("📖Fórmulas")

            ],
            [
                IKB("🏷Envolver"),
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


def habalar_pasaporte(update: Update, context: CallbackContext):
    text = "Cuando te acercaste al extraño, instantáneamente lo reconociste - era Contrabandista, "
    text += " un criminal conocido y peligroso, buscado por la guardia en cada castillo."
    text += "¿Qué estás haciendo, cambiando tu lealtad?  Entonces este es mi precio. Si no - lárgate de aquí y no me hagas perder el tiempo"
    text += "🦌Pasaporte Deerhorn 💎 25"
    text += "🐺Pasaporte Wolfpack 💎 35"
    text += "🦈Sharkteeth pasaporte 💎 60"
    text += "🌑Pasaporte a la luz de la luna 💎 84"
    text += "🦅Pasaporte a la luz de la luna 💎 84"
    text += "🥔Pasaporte de papa 💎 10"
    text += "🐉 Pasaporte Dragonscale 💎 21"

    IKB = KeyboardButton

    reply_markup = ReplyKeyboardMarkup(
        [

            [
                IKB("🐉Pasaporte"),
                IKB("🌑Pasaporte"),
                IKB("🥔Pasaporte")

            ],
            [
                IKB("🐺Pasaporte"),
                IKB("🦌Pasaporte"),
                IKB("🦅Pasaporte"),
                IKB("🦈Pasaporte"),
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


def subastas(update: Update, context: CallbackContext):
    text = "No esta disponible"
    IKB = KeyboardButton

    reply_markup = ReplyKeyboardMarkup(
        [

            [
                IKB("⚒Mesa de trabajo"),
                IKB("📖Fórmulas")

            ],
            [
                IKB("🏷Envolver"),
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


def inetercambio(update: Update, context: CallbackContext):
    text = "No esta disponible"
    IKB = KeyboardButton

    reply_markup = ReplyKeyboardMarkup(
        [

            [
                IKB("⚒Mesa de trabajo"),
                IKB("📖Fórmulas")

            ],
            [
                IKB("🏷Envolver"),
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


def diamantes(update: Update, context: CallbackContext):
    text = "No esta disponible"
    IKB = KeyboardButton

    reply_markup = ReplyKeyboardMarkup(
        [

            [
                IKB("⚒Mesa de trabajo"),
                IKB("📖Fórmulas")

            ],
            [
                IKB("🏷Envolver"),
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


def vender(update: Update, context: CallbackContext):
    text = "No esta disponible"
    IKB = KeyboardButton

    reply_markup = ReplyKeyboardMarkup(
        [

            [
                IKB("⚒Mesa de trabajo"),
                IKB("📖Fórmulas")

            ],
            [
                IKB("🏷Envolver"),
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


def casa_pet(update: Update, context: CallbackContext):
    text = "No esta disponible"
    IKB = KeyboardButton

    reply_markup = ReplyKeyboardMarkup(
        [

            [
                IKB("⚒Mesa de trabajo"),
                IKB("📖Fórmulas")

            ],
            [
                IKB("🏷Envolver"),
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


def get_mascotas(update: Update, context: CallbackContext):
    text = "No esta disponible"
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
    text = "No esta disponible"
    IKB = KeyboardButton

    reply_markup = ReplyKeyboardMarkup(
        [

            [
                IKB("⚒Mesa de trabajo"),
                IKB("📖Fórmulas")

            ],
            [
                IKB("🏷Envolver"),
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


def bodega(update: Update, context: CallbackContext):
    text = "No esta disponible"
    IKB = KeyboardButton

    reply_markup = ReplyKeyboardMarkup(
        [

            [
                IKB("⚒Mesa de trabajo"),
                IKB("📖Fórmulas")

            ],
            [
                IKB("🏷Envolver"),
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

#  Clan


def clan(update: Update, context: CallbackContext):
    text = "🦅[SA] Sao Alternative"
    text += "Commander: Artas1"
    text += "🏅Level: 5 🎖Glory: 1905"
    text += "💎Diamonds: 0"
    text += "👥 14/15"

    IKB = KeyboardButton

    reply_markup = ReplyKeyboardMarkup(
        [

            [
                IKB("📦Almacen"),
                IKB("📋Lista"),
                IKB("ℹ️Otros")
            ],
            [
                IKB("🤝Alianza"),
                IKB("🏕Misiones"),
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


def alam_clan(update: Update, context: CallbackContext):
    text = "Guild Warehouse: 4424/28000"
    text += "/g_stock_res - resources"
    text += "/g_stock_alch - alchemist herbs"
    text += "/g_stock_misc - miscellaneous stuff"
    text += "/g_stock_rec - items recipes"
    text += "/g_stock_parts - items parts"
    text += "/g_stock_other - everything else"

    IKB = KeyboardButton

    reply_markup = ReplyKeyboardMarkup(
        [

            [
                IKB("📦Almacen"),
                IKB("📋Lista"),
                IKB("ℹ️Otros")
            ],
            [
                IKB("🤝Alianza"),
                IKB("🏕Misiones"),
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


def lista_clan(update: Update, context: CallbackContext):
    text = "🦅Sao Alternative"
    text += "#1 🛡⚗️69 [🛡] StormBlessed"
    text += "#2 ⚔️40 [🛌] Carlos"
    text += "#3 🏹36 [🛌] SuperGirl"
    text += "#4 🛡34 [💤] Artas1"
    text += "#5 ⚒29 [🛌] JuanShotLC"
    text += "#6 ⚒28 [🛌] Lordaeron"
    text += "#7 🛡25 [🛌] CARONTE"
    text += "#8 🛡22 [🗡] Astharot"
    text += "#9 ⚗️22 [🛌] Adianys"
    text += "#10 ⚗️21 [🛌] Satoru Gojo"
    text += "#11 ⚗️20 [🛌] Albus Dumbledore"
    text += "#12 🐣19 [🛌] Ozymandias"
    text += "#13 🐣18 [🌲] ItaliaFacista"
    text += "#14 🐣18 [🛌] Tanos_King"

    IKB = KeyboardButton

    reply_markup = ReplyKeyboardMarkup(
        [

            [
                IKB("📦Almacen"),
                IKB("📋Lista"),
                IKB("ℹ️Otros")
            ],
            [
                IKB("🤝Alianza"),
                IKB("🏕Misiones"),
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


def otros_clan(update: Update, context: CallbackContext):
    text = "/g_atk {guildTag} para atacarlo en la próxima guerra. Esto le costará a tu gremio algo without sin declaración de guerras"
    text += "/g_atklist para ver las estadísticas de guild atk"
    text += "/g_def {guildTag} para defenderlo en la próxima guerra"
    text += "/g_deflist para ver guild def stat"
    text += "/g_deposit {item code} {qty} para depositar artículos en el gremio"
    text += "/g_deposit_dmd {qty} para donar diamantes al gremio"
    text += "/g_emoji {emoji} para establecer emj de gremio"
    text += "/g_emoji_confirm Emoji de confirmación del líder del gremio"
    text += "/g_emoji_list Ver todos los emojis disponibles"
    text += "/g_emoji_prolong Prolongación del emoji del líder del gremio"
    text += "/g_i {código del artículo} para inspeccionar el artículo único"
    text += "/g_inspect {código del elemento} para inspeccionar el elemento único"
    text += "/g_leave para dejar el gremio. Esto le costará a tu gremio 🎖"
    text += "/g_list para ver miembros"
    text += "/g_q_view Vista de búsqueda"
    text += "/g_quests Mostrar misiones"
    text += "/g_roles para ver los roles de tu gremio"
    text += "/g_stock para ver el stock"
    text += "/g_stock_mod para ver los modificadores de stock"
    IKB = KeyboardButton

    reply_markup = ReplyKeyboardMarkup(
        [

            [
                IKB("📦Almacen"),
                IKB("📋Lista"),
                IKB("ℹ️Otros")
            ],
            [
                IKB("🤝Alianza"),
                IKB("🏕Misiones"),
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


def alianza_clan(update: Update, context: CallbackContext):
    text = "Your guild is not in alliance."
    IKB = KeyboardButton

    reply_markup = ReplyKeyboardMarkup(
        [

            [
                IKB("📦Almacen"),
                IKB("📋Lista"),
                IKB("ℹ️Otros")
            ],
            [
                IKB("🤝Alianza"),
                IKB("🏕Misiones"),
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


def misiones_clan(update: Update, context: CallbackContext):
    text = "🏕Lista de misiones:"
    text += "Caza de campeones prohibidos /g_q_view_a10"
    IKB = KeyboardButton

    reply_markup = ReplyKeyboardMarkup(
        [

            [
                IKB("📦Almacen"),
                IKB("📋Lista"),
                IKB("ℹ️Otros")
            ],
            [
                IKB("🤝Alianza"),
                IKB("🏕Misiones"),
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

# Almacen


def almc(update: Update, context: CallbackContext):
    global PlayerDB,RecursosDB
    user = update.message.from_user
    player = PlayerDB[str(user.id)]
    AlmaceJG = player["almacen_re"]
    bolso_arm = player["stock"]

    text = "\n📦Almacen: ({total}".format(total="0" if bolso_arm == 0 else bolso_arm)
    text += "/{bolso})".format(bolso=bolso_arm)
    for w in list(set(AlmaceJG.keys()) - set(AlmaceJG["00"])):
                text+="\n{name} ({cant})".format(name=AlmaceJG[w]["nombre"],cant=AlmaceJG[w]["cantidad"])


    IKB = KeyboardButton

    reply_markup = ReplyKeyboardMarkup(
        [

            [
                IKB("🎒Bolso"),
                IKB("📦Recursos"),
                IKB("🗃Varios")
            ],

            [
                IKB("⚗️Alquimia"),
                IKB("⚒Elaboración")
            ],
            [
                IKB("🏷Equipo"),
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


def recursos(update: Update, context: CallbackContext):
    text = "Almacenamiento: (1218/8000):"
    IKB = KeyboardButton

    reply_markup = ReplyKeyboardMarkup(
        [

            [
                IKB("🎒Bolso"),
                IKB("📦Recursos"),
                IKB("🗃Varios")
            ],

            [
                IKB("⚗️Alquimia"),
                IKB("⚒Elaboración")
            ],
            [
                IKB("🏷Equipo"),
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


def varios(update: Update, context: CallbackContext):
    text = "[empty]"

    IKB = KeyboardButton

    reply_markup = ReplyKeyboardMarkup(
        [

            [
                IKB("🎒Bolso"),
                IKB("📦Recursos"),
                IKB("🗃Varios")
            ],

            [
                IKB("⚗️Alquimia"),
                IKB("⚒Elaboración")
            ],
            [
                IKB("🏷Equipo"),
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


def alquimia(update: Update, context: CallbackContext):
    text = "[empty]"

    IKB = KeyboardButton

    reply_markup = ReplyKeyboardMarkup(
        [

            [
                IKB("🎒Bolso"),
                IKB("📦Recursos"),
                IKB("🗃Varios")
            ],

            [
                IKB("⚗️Alquimia"),
                IKB("⚒Elaboración")
            ],
            [
                IKB("🏷Equipo"),
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


def elaboracion(update: Update, context: CallbackContext):
    text = "[empty]"

    IKB = KeyboardButton

    reply_markup = ReplyKeyboardMarkup(
        [

            [
                IKB("🎒Bolso"),
                IKB("📦Recursos"),
                IKB("🗃Varios")
            ],

            [
                IKB("⚗️Alquimia"),
                IKB("⚒Elaboración")
            ],
            [
                IKB("🏷Equipo"),
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


def bolso(update: Update, context: CallbackContext):
    global PlayerDB
    user = update.message.from_user
    player = PlayerDB[str(user.id)]
    BolsoJG = player["bolso_arm"]
    level = player["level"]
    bolso_arm = len(player["bolso_arm"])-1
    a = 0
    a2 = 0
    a3 = 0
    a4 = 0
    a5 = 0
    a6 = 0
    a7 = 0
    a8 = 0
    a9 = 0
    d1 = 0
    d2 = 0
    d3 = 0
    d4 = 0
    d5 = 0
    d6 = 0
    d7 = 0
    d8 = 0
    d9 = 0
    Total_ataque = 0
    Total_defensa = 0

    if(player["manoPrincipal"] != "None"):
        a = int(BolsoJG[player["manoPrincipal"]]["atributos"]["ataque"])
        d1 = int(BolsoJG[player["manoPrincipal"]]["atributos"]["defensa"])
    if(player["mano"] != "None"):
        a2 = int(BolsoJG[player["mano"]]["atributos"]["ataque"])
        d2 = int(BolsoJG[player["mano"]]["atributos"]["defensa"])
    if(player["casco"] != "None"):
        a3 = int(BolsoJG[player["casco"]]["atributos"]["ataque"])
        d3 = int(BolsoJG[player["casco"]]["atributos"]["defensa"])
    if(player["guantes"] != "None"):
        a4 = int(BolsoJG[player["guantes"]]["atributos"]["ataque"])
        d4 = int(BolsoJG[player["guantes"]]["atributos"]["defensa"])
    if(player["armadura"] != "None"):
        a5 = int(BolsoJG[player["armadura"]]["atributos"]["ataque"])
        d5 = int(BolsoJG[player["armadura"]]["atributos"]["defensa"])
    if(player["botas"] != "None"):
        a6 = int(BolsoJG[player["botas"]]["atributos"]["ataque"])
        d6 = int(BolsoJG[player["botas"]]["atributos"]["defensa"])
    if(player["especial"] != "None"):
        a7 = int(BolsoJG[player["especial"]]["atributos"]["ataque"])
        d7 = int(BolsoJG[player["especial"]]["atributos"]["defensa"])
    if(player["anillo"] != "None"):
        a8 = int(BolsoJG[player["anillo"]]["atributos"]["ataque"])
        d8 = int(BolsoJG[player["anillo"]]["atributos"]["defensa"])
    if(player["collar"] != "None"):
        a9 = int(BolsoJG[player["collar"]]["atributos"]["ataque"])
        d9 = int(BolsoJG[player["collar"]]["atributos"]["defensa"])

    Total_ataque = a + a2 + a3 + a4 + a5 + a6 + a7 + a8 + a9
    Total_defensa = d1 + d2 + d3 + d4 + d5 + d6 + d7 + d8 + d9
    Suma = Total_ataque + Total_defensa

    text = "\n\n🎽Euipamiento:"
    if(Suma == 0):
        text += "[-]"
    else:
        if(Total_ataque > 0):
            text += "+{t}⚔️".format(t=Total_ataque)
        if(Total_defensa > 0):
            text += "+{td}🛡".format(td=Total_defensa)

    if(player["manoPrincipal"] != "None"):
        p = player["manoPrincipal"]
        nombre = str(BolsoJG[p]["nombre"])
        ataque = int(BolsoJG[p]["atributos"]["ataque"])
        defensa = int(BolsoJG[p]["atributos"]["defensa"])
        text += "\n{n} ".format(n=nombre)
        if(ataque > 0):
            text += "+{d}⚔️".format(d=ataque)
        if(defensa > 0):
            text += "+{d}🛡".format(d=defensa)
        text += " /off_{id}".format(id=p)
    if(player["mano"] != "None"):
        p2 = int(player["mano"])
        nombre2 = str(BolsoJG[p2]["nombre"])
        ataque2 = int(BolsoJG[p2]["atributos"]["ataque"])
        defensa2 = int(BolsoJG[p2]["atributos"]["defensa"])
        text += "\n{n} ".format(n=nombre2)
        if(ataque2 > 0):
            text += "+{d}⚔️".format(d=ataque2)
        if(defensa2 > 0):
            text += "+{d}🛡".format(d=defensa2)
        text += " /off_{id}".format(id=p2)
    if(player["casco"] != "None"):
        p3 = int(player["casco"])
        nombre3 = str(BolsoJG[p3]["nombre"])
        ataque3 = int(BolsoJG[p3]["atributos"]["ataque"])
        defensa3 = int(BolsoJG[p3]["atributos"]["defensa"])
        text += "\n{n} ".format(n=nombre3)
        if(ataque3 > 0):
            text += "+{d}⚔️".format(d=ataque3)
        if(defensa3 > 0):
            text += "+{d}🛡".format(d=defensa3)
        text += " /off_{id}".format(id=p3)
    if(player["guantes"] != "None"):
        p4 = int(player["guantes"])
        nombre4 = str(BolsoJG[p4]["nombre"])
        ataque4 = int(BolsoJG[p4]["atributos"]["ataque"])
        defensa4 = int(BolsoJG[p4]["atributos"]["defensa"])
        text += "\n{n} ".format(n=nombre4)
        if(ataque4 > 0):
            text += "+{d}⚔️".format(d=ataque4)
        if(defensa4 > 0):
            text += "+{d}🛡".format(d=defensa4)
        text += " /off_{id}".format(id=p4)
    if(player["armadura"] != "None"):
        p5 = int(player["armadura"])
        nombre5 = str(BolsoJG[p5]["nombre"])
        ataque5 = int(BolsoJG[p5]["atributos"]["ataque"])
        defensa5 = int(BolsoJG[p5]["atributos"]["defensa"])
        text += "\n{n} ".format(n=nombre5)
        if(ataque5 > 0):
            text += "+{d}⚔️".format(d=ataque5)
        if(defensa5 > 0):
            text += "+{d}🛡".format(d=defensa5)
        text += " /off_{id}".format(id=p5)
    if(player["botas"] != "None"):
        p6 = int(player["botas"])
        nombre6 = str(BolsoJG[p6]["nombre"])
        ataque6 = int(BolsoJG[p6]["atributos"]["ataque"])
        defensa6 = int(BolsoJG[p6]["atributos"]["defensa"])
        text += "\n{n} ".format(n=nombre6)
        if(ataque6 > 0):
            text += "+{d}⚔️".format(d=ataque6)
        if(defensa6 > 0):
            text += "+{d}🛡".format(d=defensa6)
        text += " /off_{id}".format(id=p6)
    if(player["especial"] != "None"):
        p7 = int(player["especial"])
        nombre7 = str(BolsoJG[p7]["nombre"])
        ataque7 = int(BolsoJG[p7]["atributos"]["ataque"])
        defensa7 = int(BolsoJG[p7]["atributos"]["defensa"])
        text += "\n{n} ".format(n=nombre7)
        if(ataque7 > 0):
            text += "+{d}⚔️".format(d=ataque7)
        if(defensa7 > 0):
            text += "+{d}🛡".format(d=defensa7)
        text += " /off_{id}".format(id=p7)
    if(player["anillo"] != "None"):
        p8 = int(player["anillo"])
        nombre8 = str(BolsoJG[p8]["nombre"])
        ataque8 = int(BolsoJG[p8]["atributos"]["ataque"])
        defensa8 = int(BolsoJG[p8]["atributos"]["defensa"])
        text += "\n{n} ".format(n=nombre8)
        if(ataque8 > 0):
            text += "+{d}⚔️".format(d=ataque8)
        if(defensa8 > 0):
            text += "+{d}🛡".format(d=defensa8)
        text += " /off_{id}".format(id=p8)
    if(player["collar"] != "None"):
        p9 = int(player["collar"])
        nombre9 = str(BolsoJG[p9]["nombre"])
        ataque9 = int(BolsoJG[p9]["atributos"]["ataque"])
        defensa9 = int(BolsoJG[p9]["atributos"]["defensa"])
        text += "\n{n} ".format(n=nombre9)
        if(ataque9 > 0):
            text += "+{d}⚔️".format(d=ataque9)
        if(defensa9 > 0):
            text += "+{d}🛡".format(d=defensa9)
        text += " /off_{id}".format(id=p9)

    text += "\n🎒Balso: ({total}".format(total="0" if bolso_arm ==
                                        0 else bolso_arm)
    text += "/{bolso})".format(bolso=player["bolso"])
    p = 1
    n = bolso_arm + 1
    for i in BolsoJG[p:n]:
        if(BolsoJG[p]["estatus"] != 1):
            text += "\n<b>{name}</b> ".format(name=BolsoJG[p]["nombre"])
            if(BolsoJG[p]["atributos"]["ataque"] > 0):
                text += "<b>+{actaque}</b>⚔️".format(
                    actaque=BolsoJG[p]["atributos"]["ataque"])
            if(BolsoJG[p]["atributos"]["defensa"] > 0):
                text += "<b>+{defensa}</b>🛡".format(
                    defensa=BolsoJG[p]["atributos"]["defensa"])
            text += " /on_{id}".format(id=p)

        p = p+1

    IKB = KeyboardButton
    reply_markup = ReplyKeyboardMarkup(
        [

            [
                IKB("🎒Bolso"),
                IKB("📦Recursos"),
                IKB("🗃Varios")
            ],

            [
                IKB("⚗️Alquimia"),
                IKB("⚒Elaboración")
            ],
            [
                IKB("🏷Equipo"),
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


def equipo_envuelto(update: Update, context: CallbackContext):
    text = "[empty]"

    IKB = KeyboardButton

    reply_markup = ReplyKeyboardMarkup(
        [

            [
                IKB("🎒Bolso"),
                IKB("📦Recursos"),
                IKB("🗃Varios")
            ],

            [
                IKB("⚗️Alquimia"),
                IKB("⚒Elaboración")
            ],
            [
                IKB("🏷Equipo"),
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


# Informacion para el servidor
def lastrestart(signum, frame):
    data = {
        "signum": str(signum),
        "hora": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    }
    Fire.put("/", "Last_server_restart", data)
    Fire.put("/", "players", PlayerDB)
    print("Datos guardados con éxito!")
    return


def error(update, error="Unexpected Error!"):
    """Log Errors caused by Updates."""
    global updater
    bot = updater.bot
    Mickey = 622952731
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    try:
        update = update.to_dict()
    except:
        update = str(update)
    # print(str(fname))
    message = "Actualizar: \n{} \n...Error causado : \n\n<code>{}:{}</code> en <code>{}</code> en la linea <code>{}</code>\n\nNotas: {}".format(
        tree(update, HTML=True),
        escape(str(exc_type)),
        escape(str(exc_obj)),
        escape(str(fname)),
        escape(str(exc_tb.tb_lineno)),
        escape(str(error)))
    bot.send_message(Mickey, message, parse_mode=ParseMode.HTML)
    message = message.replace("<code>", "")
    message = message.replace("</code>", "")
    logger.warning(message)
    return


def fallback(update: Update, context: CallbackContext):
    context.update_queue.put(update)
    return ConversationHandler.END


def connect(update: Update, context: CallbackContext):
    user = update.message.from_user
    context.bot.send_message(
        chat_id=user.id,
        text="Conectado!",
        parse_mode=ParseMode.HTML
    )
    return


def updateUser(user):
    global PlayerDB
    Fire.put("/players/"+str(user.id), "username", user.username)
    Fire.put("/players/"+str(user.id), "lastlog",
             datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    PlayerDB[str(user.id)]["username"] = user.username
    PlayerDB[str(user.id)]["lastlog"] = datetime.now().strftime(
        "%d/%m/%Y %H:%M:%S")
    # print(PlayerDB[str(user.id)])
    return


def reload(update: Update, context: CallbackContext):
    user = update.message.from_user
    if(user.id == 622952731):
        def reloadTask():
            global PlayerDB, NivelesBD, TiendaDB
            PlayerDB = Fire.get("/players", None)
            NivelesBD = Fire.get("/niveles_exp", None)
            TiendaDB = Fire.get("/tienda", None)
            context.bot.send_message(
                chat_id=user.id,
                text="<code>¡Recargado!</code>",
                parse_mode=ParseMode.HTML
            )
            return
        threading.Thread(target=reloadTask).start()
    return


def upload(player, concept, value):
    threading.Thread(target=manualupload, args=(
        "/players/{id}".format(id=player), concept, value,)).start()
    return


def uploadwp(player, w, concept, value):
    threading.Thread(target=manualuploadwp, args=(
        "/players/{id}/bolso_arm/{p}".format(id=player, p=w), concept, value,)).start()
    return


def manualuploadwp(player, concept, value):
    global PlayerDB
    if(type(concept) in [list, tuple]):
        for c in range(len(concept)):
            try:
                Fire.put(player, concept[c], value[c])
            except:
                e = "{}/{} = {}".format(player, concept[c], value[c])
                error("En la carga manual", e)
    else:
        Fire.put(player, concept, value)
    PlayerDB = Fire.get("/players", None)
    return

def manualupload(player, concept, value):
    global PlayerDB
    if(type(concept) in [list, tuple]):
        for c in range(len(concept)):
            try:
                Fire.put(player, concept[c], value[c])
            except:
                e = "{}/{} = {}".format(player, concept[c], value[c])
                error("En la carga manual", e)
    else:
        Fire.put(player, concept, value)
    PlayerDB = Fire.get("/players", None)
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
            MessageHandler(Filters.regex(
                "^(⚒Mesa de trabajo)$"), mesa_trabajo),
            MessageHandler(Filters.regex("^(⚒Artesanía)$"), craf),
            MessageHandler(Filters.regex("^(📖Fórmulas)$"), formulas),
            MessageHandler(Filters.regex("^(🏷Envolver)$"), envolver),

            MessageHandler(Filters.regex("^(🍺Taberna)$"), taberna),
            MessageHandler(Filters.regex("^(🛎Subastas)$"), subastas),
            MessageHandler(Filters.regex("^(⚖️Instercambios)$"), inetercambio),
            MessageHandler(Filters.regex("^(🏚Tienda)$"), shop),
            MessageHandler(Filters.regex("^(💎Lujo)$"), diamantes),
            MessageHandler(Filters.regex("^(💰Vender)$"), vender),
            MessageHandler(Filters.regex("^(🐾Casa de fieras)$"), casa_pet),
            MessageHandler(Filters.regex(
                "^(🎟Consigue una mascota)$"), get_mascotas),
            MessageHandler(Filters.regex("^(💁Refugio)$"), refugio),
            MessageHandler(Filters.regex("^(⚰️Bodega)$"), bodega),

            MessageHandler(Filters.regex("^(👥Clanes)$"), clan),
            MessageHandler(Filters.regex("^(📦Almacen)$"), alam_clan),
            MessageHandler(Filters.regex("^(📋Lista)$"), lista_clan),
            MessageHandler(Filters.regex("^(ℹ️Otros)$"), otros_clan),
            MessageHandler(Filters.regex("^(🤝Alianza)$"), alianza_clan),
            MessageHandler(Filters.regex("^(🏕Misiones)$"), misiones_clan),

            MessageHandler(Filters.regex("🎒Bolso"), bolso),
            MessageHandler(Filters.regex("📦Recursos"), recursos),
            MessageHandler(Filters.regex("🗃Varios"), varios),
            MessageHandler(Filters.regex("⚗️Alquimia"), alquimia),
            MessageHandler(Filters.regex("⚒Elaboración"), elaboracion),
            MessageHandler(Filters.regex("🏷Equipo"), equipo_envuelto),
            # MessageHandler(Filters.regex("^(🎲Dados)$"), dados),
            MessageHandler(Filters.regex(r"^\/info_\d+$"), winfo),
            MessageHandler(Filters.regex(r"^\/on_\d+$"), equip),
            MessageHandler(Filters.regex(r"^\/off_\d+$"), equipoff),
            MessageHandler(Filters.regex(r"^\/buy_\d+$"), buy),
            CommandHandler('r', reload),
            CommandHandler('heroe', heroe),
            CommandHandler('tiempo', tiempo),
            CommandHandler('inv', inventario),
            CommandHandler('almc', almc),
            MessageHandler(Filters.text, register)
        ],

        states={
            # ME: []

            # BR: [MessageHandler(Filters.regex("^(👥 Talk)$"), connect)],

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
    updater.dispatcher.add_handler(InlineQueryHandler(
        inlinequery, pass_user_data=True, pass_chat_data=True))
    updater.user_sig_handler = lastrestart
    updater.start_polling(poll_interval=0.1, clean=True, read_latency=1.0)

    updater.idle()
    return


if __name__ == '__main__':
    main()
