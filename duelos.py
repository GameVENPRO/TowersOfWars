#Librerías para interactuar con la API de Telegram
from telegram import *
from telegram.ext import *
from funciones import  *
from kb import *
from castillo import *
from registro import *


ArenaList = {'0':'null'}
tmpPlayers = {'0':'null'}

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
            'el':{
                'nomin':'el',
                'object':'él',
                'possAdj':'su',
                'possPro':'su',
                'reflex':'suyo'
            },
            'ella':{
                'nomin':'ella',
                'object':'ella',
                'possAdj':'ella',
                'possPro':'suyo',
                'reflex':'ella misma'
            },
            'se':{
                'nomin':'se',
                'object':'se',
                'possAdj':'su',
                'possPro':'su',
                'reflex':'sí mismo'
            },
            'nos':{
                'nomin':'nos',
                'object':'nos',
                'possAdj':'nuestro',
                'possPro':'nosotros',
                'reflex':'nosotros mismos'
            },            
            'le':{
                'nomin':'le',
                'object':'ellos',
                'possAdj':'su',
                'possPro':'suyo',
                'reflex':'ellos mismos'
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
        part = {'h':'En la Cabeza','b':'En el Cuerpo','l':' En la Pierna'}
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
                text += "\n%s Atacó a %s - %s con %s %s"%(
                    self.Players[prs[0]].name,
                    self.Players[prs[1]].name,
                    part[atk].lower(),
                    self.Players[prs[0]].pron['possAdj'],
                    self.Players[prs[0]].mainW["nombre"]
                    )

                if(dam > 0):
                    text += ', trato %s%s daño.'%(
                        str(dam),
                        critxt
                    )

                else:
                    text += ', pero %s logró defender %s utilizando %s %s.'%(
                        self.Players[prs[1]].name,
                        self.Players[prs[1]].pron['reflex'],
                        self.Players[prs[1]].pron['possAdj'],
                        self.Players[prs[1]].offHW['nombre']
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
                    text += "\n%s Atacó a %s - %s con %s %s"%(
                        self.Players[prs[1]].name,
                        self.Players[prs[0]].name,
                        part[atk].lower(),
                        self.Players[prs[1]].pron['possAdj'],
                        self.Players[prs[1]].mainW["nombre"]
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
                            self.Players[prs[0]].offHW['nombre']
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
                                            title="🎲Dados",
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
