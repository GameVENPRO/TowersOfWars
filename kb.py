 #Librerías para interactuar con la API de Telegram
from telegram import *
from telegram.ext import *

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
                    IKB("Espadas",    callback_data="{\"op\":\"%s\",\"d1\":\"espadas\",\"d2\":\"%s\"}"%(args)),
                    IKB("Dagas",   callback_data="{\"op\":\"%s\",\"d1\":\"dagas\",\"d2\":\"%s\"}"%(args)),
                    IKB("Desafilados",      callback_data="{\"op\":\"%s\",\"d1\":\"desafilados\",\"d2\":\"%s\"}"%(args))
                ],
                [
                    IKB("Arcos",  callback_data="{\"op\":\"%s\",\"d1\":\"arcos\",\"d2\":\"%s\"}"%(args)),
                    IKB("Botas",   callback_data="{\"op\":\"%s\",\"d1\":\"botas\",\"d2\":\"%s\"}"%(args)),
                    IKB("Armaduras",     callback_data="{\"op\":\"%s\",\"d1\":\"armaduras\",\"d2\":\"%s\"}"%(args))
                ],
                [
                    IKB("Guantes",   callback_data="{\"op\":\"%s\",\"d1\":\"guantes\",\"d2\":\"%s\"}"%(args)),
                    IKB("Lanzas",    callback_data="{\"op\":\"%s\",\"d1\":\"lanzas\",\"d2\":\"%s\"}"%(args)),
                    IKB("Escudos",   callback_data="{\"op\":\"%s\",\"d1\":\"escudos\",\"d2\":\"%s\"}"%(args))
                ],                
                [
                    IKB("Cascos",   callback_data="{\"op\":\"%s\",\"d1\":\"cascos\",\"d2\":\"%s\"}"%(args))
                ],
            ]
        else:
            keyboard = [[IKB("╔"),IKB("╗")],[IKB("╚"),IKB("╝")]]
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
