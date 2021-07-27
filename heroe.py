#Librerías para interactuar con la API de Telegram
from telegram import *
from telegram.ext import *
from funciones import  *
from kb import *

def me(update: Update, context: CallbackContext):
    global PlayerDB
    user = update.message.from_user
    player = PlayerDB[str(user.id)]
    level = player["level"] 
    habilidad = player["puntos_habili"]
    exp_niveles = NivelesBD[level+1]      
    bolso_arm = len(player["bolso_arm"])-1  
    text=""
    if(int(habilidad) > 0):
        text+="\n🌟Congratulations Felicitaciones! Nuevo nivel!🌟"
        text+="\n\nAsignar puntos /level_up"
        # text+="\nBatlla"
        # text+="\n\n"

    text+="{fla}".format(fla=player["flag_casti"])
    #text+="[LSD]"
    text+="{name}".format(name=user.first_name)
    text+=" Del Castillo {castillo}".format(castillo=player["castillo"])
    
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
    text+="\n🎒Balso: {total}".format(total="0" if bolso_arm == 0 else bolso_arm)
    text+="/{bolso} ".format(bolso=player["bolso"])
    text+="/inv"
    # +"Mascota:{money}".format(money=player["money"])
    text+="\n\nEstado:\n{estado}".format(estado=player["estado"])
    text+="\n\nMás: /heroe"

    reply_markup = ReplyKeyboardMarkup(kb.ini_kb(level),resize_keyboard=True)

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
    exp_niveles = NivelesBD[level+1]       
    bolso_arm = len(player["bolso_arm"])-1
    alma_re = len(player["almacen_re"])-1
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
    text="{fla}".format(fla=player["flag_casti"])
    #text+="[LSD]"
    text+="{name}".format(name=user.first_name)
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
        
    text+="\n📚Especializaciónes:"
    if(level <= 14):
        text+="-"
    if(level >= 15):
    
        text+="📕"
    if(level >= 25):
        
        text+="📗"
    if(level >= 35):
        
        text+="📘"
    if(level >= 45):
        
        text+="📙"
    if(level >= 60):
        
        text+="📒"

    text+="\n🎉Logro: /ach"
    if(level >= 20):
        text+="\n⚒Clase Info: /class"
    else:
        text+="\n🏛Clase Info: /class"
        
    if(level >= 20):
        text+="\n🚹Male"
        
    #text+="\n\n✨Efectos: /effects"
    # +"Mascota:{money}".format(money=player["money"])      
        
    text+="\n\n🎽Euipamiento:"
    if(Suma == 0):
        text+="[-]"
    else:
        if(Total_ataque > 0):
            text+="+{t}⚔️".format(t=Total_ataque)
        if(Total_defensa > 0):
            text+="+{td}🛡".format(td=Total_defensa)

    
    if(player["manoPrincipal"]!="None"):  
        p=player["manoPrincipal"]
        nombre =str(BolsoJG[p]["nombre"])  
        ataque =int(BolsoJG[p]["atributos"]["ataque"])
        defensa= int(BolsoJG[p]["atributos"]["defensa"]) 
        text+="\n{n} ".format(n=nombre)           
        if(ataque > 0):           
            text+="+{d}⚔️".format(d=ataque)            
        if(defensa > 0):          
            text+="+{d}🛡".format(d=defensa)
        text+=" /off_{id}".format(id=p)
    if(player["mano"]!="None"):
        p2=int(player["mano"])
        nombre2 =str(BolsoJG[p2]["nombre"])
        ataque2 =int(BolsoJG[p2]["atributos"]["ataque"])
        defensa2= int(BolsoJG[p2]["atributos"]["defensa"])
        text+="\n{n} ".format(n=nombre2)
        if(ataque2 > 0):            
            text+="+{d}⚔️".format(d=ataque2)            
        if(defensa2 > 0):                      
            text+="+{d}🛡".format(d=defensa2)
        text+=" /off_{id}".format(id=p2)        
    if(player["casco"]!="None"):
        p3=int(player["casco"])
        nombre3 =str(BolsoJG[p3]["nombre"])
        ataque3 =int(BolsoJG[p3]["atributos"]["ataque"])
        defensa3= int(BolsoJG[p3]["atributos"]["defensa"])
        text+="\n{n} ".format(n=nombre3)
        if(ataque3 > 0):            
            text+="+{d}⚔️".format(d=ataque3)            
        if(defensa3 > 0):                      
            text+="+{d}🛡".format(d=defensa3)
        text+=" /off_{id}".format(id=p3)
    if(player["guantes"]!="None"):
        p4=int(player["guantes"])
        nombre4 =str(BolsoJG[p4]["nombre"])
        ataque4 =int(BolsoJG[p4]["atributos"]["ataque"])
        defensa4= int(BolsoJG[p4]["atributos"]["defensa"])
        text+="\n{n} ".format(n=nombre4)
        if(ataque4 > 0):            
            text+="+{d}⚔️".format(d=ataque4)            
        if(defensa4 > 0):                      
            text+="+{d}🛡".format(d=defensa4)
        text+=" /off_{id}".format(id=p4)
    if(player["armadura"]!="None"):
        p5=int(player["armadura"])
        nombre5 =str(BolsoJG[p5]["nombre"])
        ataque5 =int(BolsoJG[p5]["atributos"]["ataque"])
        defensa5= int(BolsoJG[p5]["atributos"]["defensa"])
        text+="\n{n} ".format(n=nombre5)
        if(ataque5 > 0):            
            text+="+{d}⚔️".format(d=ataque5)            
        if(defensa5 > 0):                      
            text+="+{d}🛡".format(d=defensa5)
        text+=" /off_{id}".format(id=p5)
    if(player["botas"]!="None"):
        p6=int(player["botas"])
        nombre6 =str(BolsoJG[p6]["nombre"])
        ataque6 =int(BolsoJG[p6]["atributos"]["ataque"])
        defensa6= int(BolsoJG[p6]["atributos"]["defensa"])
        text+="\n{n} ".format(n=nombre6)
        if(ataque6 > 0):            
            text+="+{d}⚔️".format(d=ataque6)            
        if(defensa6 > 0):                      
            text+="+{d}🛡".format(d=defensa6)
        text+=" /off_{id}".format(id=p6)
    if(player["especial"]!="None"):
        p7=int(player["especial"])
        nombre7 =str(BolsoJG[p7]["nombre"])
        ataque7 =int(BolsoJG[p7]["atributos"]["ataque"])
        defensa7= int(BolsoJG[p7]["atributos"]["defensa"])
        text+="\n{n} ".format(n=nombre7)
        if(ataque7 > 0):            
            text+="+{d}⚔️".format(d=ataque7)            
        if(defensa7 > 0):                      
            text+="+{d}🛡".format(d=defensa7)
        text+=" /off_{id}".format(id=p7)
    if(player["anillo"]!="None"):
        p8=int(player["anillo"])
        nombre8 =str(BolsoJG[p8]["nombre"])
        ataque8 =int(BolsoJG[p8]["atributos"]["ataque"])
        defensa8= int(BolsoJG[p8]["atributos"]["defensa"])
        text+="\n{n} ".format(n=nombre8)
        if(ataque8 > 0):            
            text+="+{d}⚔️".format(d=ataque8)            
        if(defensa8 > 0):                      
            text+="+{d}🛡".format(d=defensa8)
        text+=" /off_{id}".format(id=p8)
    if(player["collar"]!="None"):
        p9=int(player["collar"])
        nombre9 =str(BolsoJG[p9]["nombre"])
        ataque9 =int(BolsoJG[p9]["atributos"]["ataque"])
        defensa9= int(BolsoJG[p9]["atributos"]["defensa"])
        text+="\n{n} ".format(n=nombre9)
        if(ataque9 > 0):            
            text+="+{d}⚔️".format(d=ataque9)            
        if(defensa9 > 0):                      
            text+="+{d}🛡".format(d=defensa9)
        text+=" /off_{id}".format(id=p9)
            
    text+="\n\n🎒Balso: {total}".format(total="0" if bolso_arm == 0 else bolso_arm)
    text+="/{bolso} ".format(bolso=player["bolso"])
    text+="/inv"
    text+="\n\n📦Almacen: {total} /stock".format(total=alma_re)

    reply_markup = ReplyKeyboardMarkup(kb.ini_kb(level),resize_keyboard=True)

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
    
    text="\n\n🎽Euipamiento:"
    if(Suma == 0):
        text+="[-]"
    else:
        if(Total_ataque > 0):
            text+="+{t}⚔️".format(t=Total_ataque)
        if(Total_defensa > 0):
            text+="+{td}🛡".format(td=Total_defensa)
            
    if(player["manoPrincipal"]!="None"):  
        p=player["manoPrincipal"]
        nombre =str(BolsoJG[p]["nombre"])  
        ataque =int(BolsoJG[p]["atributos"]["ataque"])
        defensa= int(BolsoJG[p]["atributos"]["defensa"]) 
        text+="\n{n} ".format(n=nombre)           
        if(ataque > 0):           
            text+="+{d}⚔️".format(d=ataque)            
        if(defensa > 0):          
            text+="+{d}🛡".format(d=defensa)
        text+=" /off_{id}".format(id=p)
    if(player["mano"]!="None"):
        p2=int(player["mano"])
        nombre2 =str(BolsoJG[p2]["nombre"])
        ataque2 =int(BolsoJG[p2]["atributos"]["ataque"])
        defensa2= int(BolsoJG[p2]["atributos"]["defensa"])
        text+="\n{n} ".format(n=nombre2)
        if(ataque2 > 0):            
            text+="+{d}⚔️".format(d=ataque2)            
        if(defensa2 > 0):                      
            text+="+{d}🛡".format(d=defensa2)
        text+=" /off_{id}".format(id=p2)        
    if(player["casco"]!="None"):
        p3=int(player["casco"])
        nombre3 =str(BolsoJG[p3]["nombre"])
        ataque3 =int(BolsoJG[p3]["atributos"]["ataque"])
        defensa3= int(BolsoJG[p3]["atributos"]["defensa"])
        text+="\n{n} ".format(n=nombre3)
        if(ataque3 > 0):            
            text+="+{d}⚔️".format(d=ataque3)            
        if(defensa3 > 0):                      
            text+="+{d}🛡".format(d=defensa3)
        text+=" /off_{id}".format(id=p3)       
    if(player["guantes"]!="None"):
        p4=int(player["guantes"])
        nombre4 =str(BolsoJG[p4]["nombre"])
        ataque4 =int(BolsoJG[p4]["atributos"]["ataque"])
        defensa4= int(BolsoJG[p4]["atributos"]["defensa"])
        text+="\n{n} ".format(n=nombre4)
        if(ataque4 > 0):            
            text+="+{d}⚔️".format(d=ataque4)            
        if(defensa4 > 0):                      
            text+="+{d}🛡".format(d=defensa4)
        text+=" /off_{id}".format(id=p4)
    if(player["armadura"]!="None"):
        p5=int(player["armadura"])
        nombre5 =str(BolsoJG[p5]["nombre"])
        ataque5 =int(BolsoJG[p5]["atributos"]["ataque"])
        defensa5= int(BolsoJG[p5]["atributos"]["defensa"])
        text+="\n{n} ".format(n=nombre5)
        if(ataque5 > 0):            
            text+="+{d}⚔️".format(d=ataque5)            
        if(defensa5 > 0):                      
            text+="+{d}🛡".format(d=defensa5)
        text+=" /off_{id}".format(id=p5)
    if(player["botas"]!="None"):
        p6=int(player["botas"])
        nombre6 =str(BolsoJG[p6]["nombre"])
        ataque6 =int(BolsoJG[p6]["atributos"]["ataque"])
        defensa6= int(BolsoJG[p6]["atributos"]["defensa"])
        text+="\n{n} ".format(n=nombre6)
        if(ataque6 > 0):            
            text+="+{d}⚔️".format(d=ataque6)            
        if(defensa6 > 0):                      
            text+="+{d}🛡".format(d=defensa6)
        text+=" /off_{id}".format(id=p6)
    if(player["especial"]!="None"):
        p7=int(player["especial"])
        nombre7 =str(BolsoJG[p7]["nombre"])
        ataque7 =int(BolsoJG[p7]["atributos"]["ataque"])
        defensa7= int(BolsoJG[p7]["atributos"]["defensa"])
        text+="\n{n} ".format(n=nombre7)
        if(ataque7 > 0):            
            text+="+{d}⚔️".format(d=ataque7)            
        if(defensa7 > 0):                      
            text+="+{d}🛡".format(d=defensa7)
        text+=" /off_{id}".format(id=p7)
    if(player["anillo"]!="None"):
        p8=int(player["anillo"])
        nombre8 =str(BolsoJG[p8]["nombre"])
        ataque8 =int(BolsoJG[p8]["atributos"]["ataque"])
        defensa8= int(BolsoJG[p8]["atributos"]["defensa"])
        text+="\n{n} ".format(n=nombre8)
        if(ataque8 > 0):            
            text+="+{d}⚔️".format(d=ataque8)            
        if(defensa8 > 0):                      
            text+="+{d}🛡".format(d=defensa8)
        text+=" /off_{id}".format(id=p8)
    if(player["collar"]!="None"):
        p9=int(player["collar"])
        nombre9 =str(BolsoJG[p9]["nombre"])
        ataque9 =int(BolsoJG[p9]["atributos"]["ataque"])
        defensa9= int(BolsoJG[p9]["atributos"]["defensa"])
        text+="\n{n} ".format(n=nombre9)
        if(ataque9 > 0):            
            text+="+{d}⚔️".format(d=ataque9)            
        if(defensa9 > 0):                      
            text+="+{d}🛡".format(d=defensa9)
        text+=" /off_{id}".format(id=p9)

    
    text+="\n🎒Balso: ({total}".format(total="0" if bolso_arm == 0 else bolso_arm)
    text+="/{bolso})".format(bolso=player["bolso"])
    p = 1
    n = bolso_arm + 1
        
    for i in BolsoJG[p:n]: 
        if(BolsoJG[p]["estatus"] != 1 ):
            text+="\n<b>{name}</b> ".format(name=BolsoJG[p]["nombre"])
            if(BolsoJG[p]["atributos"]["ataque"] > 0):
                    text+="<b>+{actaque}</b>⚔️".format(actaque=BolsoJG[p]["atributos"]["ataque"])    
            if(BolsoJG[p]["atributos"]["defensa"] > 0):
                    text+="<b>+{defensa}</b>🛡".format(defensa=BolsoJG[p]["atributos"]["defensa"])
            text+=" /on_{id}".format(id=p)

        p=p+1
            
    reply_markup = ReplyKeyboardMarkup(kb.ini_kb(level),resize_keyboard=True)

    update.message.reply_text(
        text=text,
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML
    )
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
    Jugador = PlayerDB[str(user.id)]
    BolsoJG = Jugador["bolso_arm"]
    weapon = update.message.text.replace("/on_","")
    
    #if(weapon not in BolsoJG):
   #     return
   # else:
    #    if(weapon not in list(BolsoJG[weapon])):
           # text = "¡No eres el dueño de esta arma!"
       # else:        
    wpassign(int(weapon),user)   
    text = "<b>{weapon}</b> equipado con éxito!".format(weapon=BolsoJG[int(weapon)]["nombre"])
            
    update.message.reply_text(
                                    text=text,
                                    parse_mode=ParseMode.HTML
                                )
    return

def equipoff(update: Update, context: CallbackContext):
    user = update.message.from_user
    Jugador = PlayerDB[str(user.id)]
    BolsoJG = Jugador["bolso_arm"]
    weapon = update.message.text.replace("/off_","")   
    
    if(BolsoJG[int(weapon)]["estatus"] == 0):
        text = "<b>[Acción Inválida]</b>"
    elif(int(weapon) == Jugador["manoPrincipal"]):
            """"Desactivar Arma"""
            uploadwp(player=str(user.id),w=(int(weapon)),concept=("estatus"),value=(0))   
            upload(player=str(user.id),concept=("manoPrincipal"),value=("None"))  
            text = "<b>{weapon}</b> Quitado con éxito!".format(weapon=BolsoJG[int(weapon)]["nombre"]) 
    elif(int(weapon) == Jugador["mano"]):
            """"Desactivar Arma"""
            uploadwp(player=str(user.id),w=(int(weapon)),concept=("estatus"),value=(0))   
            upload(player=str(user.id),concept=("mano"),value=("None")) 
            text = "<b>{weapon}</b> Quitado con éxito!".format(weapon=BolsoJG[int(weapon)]["nombre"])  
    elif(int(weapon) == Jugador["casco"]):
            """"Desactivar Arma"""
            uploadwp(player=str(user.id),w=(int(weapon)),concept=("estatus"),value=(0))   
            upload(player=str(user.id),concept=("casco"),value=("None")) 
            text = "<b>{weapon}</b> Quitado con éxito!".format(weapon=BolsoJG[int(weapon)]["nombre"])  
    elif(int(weapon) == Jugador["guantes"]):
            """"Desactivar Arma"""
            uploadwp(player=str(user.id),w=(int(weapon)),concept=("estatus"),value=(0))   
            upload(player=str(user.id),concept=("guantes"),value=("None"))
            text = "<b>{weapon}</b> Quitado con éxito!".format(weapon=BolsoJG[int(weapon)]["nombre"])   
    elif(int(weapon) == Jugador["armadura"]):
            """"Desactivar Arma"""
            uploadwp(player=str(user.id),w=(int(weapon)),concept=("estatus"),value=(0))   
            upload(player=str(user.id),concept=("armadura"),value=("None")) 
            text = "<b>{weapon}</b> Quitado con éxito!".format(weapon=BolsoJG[int(weapon)]["nombre"])  
    elif(int(weapon) == Jugador["botas"]):
            """"Desactivar Arma"""
            uploadwp(player=str(user.id),w=(int(weapon)),concept=("estatus"),value=(0))   
            upload(player=str(user.id),concept=("botas"),value=("None"))
            text = "<b>{weapon}</b> Quitado con éxito!".format(weapon=BolsoJG[int(weapon)]["nombre"])   
    elif(int(weapon) == Jugador["especial"]):
            """"Desactivar Arma"""
            uploadwp(player=str(user.id),w=(int(weapon)),concept=("estatus"),value=(0))   
            upload(player=str(user.id),concept=("especial"),value=("None"))
            text = "<b>{weapon}</b> Quitado con éxito!".format(weapon=BolsoJG[int(weapon)]["nombre"])   
    elif(int(weapon) == Jugador["anillo"]):
            """"Desactivar Arma"""
            uploadwp(player=str(user.id),w=(int(weapon)),concept=("estatus"),value=(0))   
            upload(player=str(user.id),concept=("anillo"),value=("None"))
            text = "<b>{weapon}</b> Quitado con éxito!".format(weapon=BolsoJG[int(weapon)]["nombre"])
    elif(int(weapon) == Jugador["collar"]):
            """"Desactivar Arma"""
            uploadwp(player=str(user.id),w=(int(weapon)),concept=("estatus"),value=(0))   
            upload(player=str(user.id),concept=("collar"),value=("None"))
            text = "<b>{weapon}</b> Quitado con éxito!".format(weapon=BolsoJG[int(weapon)]["nombre"])
                                            
    update.message.reply_text(
                                    text=text,
                                    parse_mode=ParseMode.HTML
                                )
    return

def wpassign(weapon,user):
    Jugador = PlayerDB[str(user.id)]
    BolsoJG = Jugador["bolso_arm"]
    WpAc = Jugador["manoPrincipal"]
    WpAc2 = Jugador["mano"]
    slot = ""
    if(BolsoJG[weapon]["g_type"] in ["espadas","lanzas","arcos","desafilados"]):
        slot = "manoPrincipal"
    elif(BolsoJG[weapon]["g_type"] in ["dagas","escudos","flechas","antorcha"] ):
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
        if(Jugador["manoPrincipal"]=="None"):
                """"Colocar Arma Nueva"""
                uploadwp(player=str(user.id),w=(weapon),concept=("estatus"),value=(1))
                upload(player=str(user.id),concept=("manoPrincipal"),value=(weapon)) 
               
        else:  

            """Desactivar armar puesta y cambiar estatus del arma puesta"""
            uploadwp(player=str(user.id),w=(WpAc),concept=("estatus"),value=(0))
            """"Colocar Arma Nueva"""
            uploadwp(player=str(user.id),w=(weapon),concept=("estatus"),value=(1))
            upload(player=str(user.id),concept=("manoPrincipal"),value=(weapon))    
                         
    elif(slot == "mano"):
        if(Jugador["mano"]=="None"):
            """Cambia normalmente"""
            uploadwp(player=str(user.id),w=(weapon),concept=("estatus"),value=(1))
            upload(player=str(user.id),concept=("mano"),value=(weapon))  
        else:        
           
                """Desactivar armar puesta y cambiar estatus del arma puesta"""
                uploadwp(player=str(user.id),w=(Jugador["mano"]),concept=("estatus"),value=(0))
                """"Colocar Arma Nueva"""
                uploadwp(player=str(user.id),w=(weapon),concept=("estatus"),value=(1))
                upload(player=str(user.id),concept=("mano"),value=(weapon))                         
    elif(slot == "casco"):
        if(Jugador["casco"]=="None"):
            """Cambia normalmente"""
            uploadwp(player=str(user.id),w=(weapon),concept=("estatus"),value=(1))
            upload(player=str(user.id),concept=("casco"),value=(weapon))  
        else:        

                """Desactivar armar puesta y cambiar estatus del arma puesta"""
                uploadwp(player=str(user.id),w=(Jugador["casco"]),concept=("estatus"),value=(0))
                """"Colocar Arma Nueva"""
                uploadwp(player=str(user.id),w=(weapon),concept=("estatus"),value=(1))
                upload(player=str(user.id),concept=("casco"),value=(weapon))       
    elif(slot == "guantes"):
        if(Jugador["guantes"]=="None"):
            """Cambia normalmente"""
            uploadwp(player=str(user.id),w=(weapon),concept=("estatus"),value=(1))
            upload(player=str(user.id),concept=("guantes"),value=(weapon))  
        else:        

                """Desactivar armar puesta y cambiar estatus del arma puesta"""
                uploadwp(player=str(user.id),w=(Jugador["guantes"]),concept=("estatus"),value=(0))
                """"Colocar Arma Nueva"""
                uploadwp(player=str(user.id),w=(weapon),concept=("estatus"),value=(1))
                upload(player=str(user.id),concept=("guantes"),value=(weapon)) 
    elif(slot == "armadura"):
        if(Jugador["armadura"]=="None"):
            """Cambia normalmente"""
            uploadwp(player=str(user.id),w=(weapon),concept=("estatus"),value=(1))
            upload(player=str(user.id),concept=("armadura"),value=(weapon))  
        else:        

                """Desactivar armar puesta y cambiar estatus del arma puesta"""
                uploadwp(player=str(user.id),w=(Jugador["armadura"]),concept=("estatus"),value=(0))
                """"Colocar Arma Nueva"""
                uploadwp(player=str(user.id),w=(weapon),concept=("estatus"),value=(1))
                upload(player=str(user.id),concept=("armadura"),value=(weapon)) 
    elif(slot == "botas"):
        if(Jugador["botas"]=="None"):
            """Cambia normalmente"""
            uploadwp(player=str(user.id),w=(weapon),concept=("estatus"),value=(1))
            upload(player=str(user.id),concept=("botas"),value=(weapon))  
        else:        

                """Desactivar armar puesta y cambiar estatus del arma puesta"""
                uploadwp(player=str(user.id),w=(Jugador["botas"]),concept=("estatus"),value=(0))
                """"Colocar Arma Nueva"""
                uploadwp(player=str(user.id),w=(weapon),concept=("estatus"),value=(1))
                upload(player=str(user.id),concept=("botas"),value=(weapon)) 
    elif(slot == "especial"):
        if(Jugador["especial"]=="None"):
            """Cambia normalmente"""
            uploadwp(player=str(user.id),w=(weapon),concept=("estatus"),value=(1))
            upload(player=str(user.id),concept=("especial"),value=(weapon))  
        else:        

                """Desactivar armar puesta y cambiar estatus del arma puesta"""
                uploadwp(player=str(user.id),w=(Jugador["especial"]),concept=("estatus"),value=(0))
                """"Colocar Arma Nueva"""
                uploadwp(player=str(user.id),w=(weapon),concept=("estatus"),value=(1))
                upload(player=str(user.id),concept=("especial"),value=(weapon)) 
    elif(slot == "anillo"):
        if(Jugador["anillo"]=="None"):
            """Cambia normalmente"""
            uploadwp(player=str(user.id),w=(weapon),concept=("estatus"),value=(1))
            upload(player=str(user.id),concept=("mano"),value=(weapon))  
        else:        

                """Desactivar armar puesta y cambiar estatus del arma puesta"""
                uploadwp(player=str(user.id),w=(Jugador["anillo"]),concept=("estatus"),value=(0))
                """"Colocar Arma Nueva"""
                uploadwp(player=str(user.id),w=(weapon),concept=("estatus"),value=(1))
                upload(player=str(user.id),concept=("anillo"),value=(weapon)) 
    elif(slot == "collar"):
        if(Jugador["collar"]=="None"):
            """Cambia normalmente"""
            uploadwp(player=str(user.id),w=(weapon),concept=("estatus"),value=(1))
            upload(player=str(user.id),concept=("collar"),value=(weapon))  
        else:        

                """Desactivar armar puesta y cambiar estatus del arma puesta"""
                uploadwp(player=str(user.id),w=(Jugador["collar"]),concept=("estatus"),value=(0))
                """"Colocar Arma Nueva"""
                uploadwp(player=str(user.id),w=(weapon),concept=("estatus"),value=(1))
                upload(player=str(user.id),concept=("collar"),value=(weapon)) 
        


            
    return
