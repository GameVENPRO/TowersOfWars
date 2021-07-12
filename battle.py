from telegram import *
from telegram.ext import *
import json
from html import escape
from random import randint as rng,choice




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