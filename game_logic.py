from datetime import datetime
import random
import json
import math
from time import sleep, time

def get_xp(lvl):
    """
    Returns total XP according to gain level
    """
    total_xp = int((lvl * 10) ** 2.1)
    return total_xp * lvl

def drop_recuros(tiempo):
            
    Res_man=["01","02","03","04","05","09","07","10","21","31"]
    Res_med=["01","03","04","07","09","20","22","23"]
    Res_tar=["01","02","03","04","05","07","09","20","21","22","23"]
    Res_noc=["01","02","03","05","06","07","08","13","22","23"]
        
    if tiempo == "🌤":
        rango = random.randint(1, 4)
        
        for i in range(rango):
            drps = Res_man[random.randint(0, 9)]
            cantida = random.randint(0, 3)
            items_d=drps
            itm_c = cantida 
            print(items_d ,itm_c) 
    elif tiempo =="🌞":
        rango = random.randint(1, 4)
        
        for i in range(rango):
            drps = Res_med[random.randint(0, 8)]
            cantida = random.randint(0, 3)
            items_d="Rercursos Ganados",drps,"Catidad:" ,cantida 
    elif tiempo == "⛅️":
        rango = random.randint(1, 4)
        
        for i in range(rango):
            drps = Res_tar[random.randint(0, 10)]
            cantida = random.randint(0, 3)
            items_d="Rercursos Ganados",drps,"Catidad:" ,cantida 
    elif  tiempo == "🌙":
        rango = random.randint(1, 4)
        
        for i in range(rango):
            drps = Res_noc[random.randint(0, 9)]
            cantida = random.randint(0, 3)
            items_d="Rercursos Ganados",drps,"Catidad:" ,cantida
        
        
    return items_d,itm_c

def item_drop(chance):
    """
    :param chance: Mob's chance of drop
    :return: True/False
    """
    c = random.randint(1, 100)
    if c >= chance:
        return True
    return False

def round_down(n, decimals=0):
    """
    Rounds a number down to a specified number of digits.

    :param decimals: Specified number of digits
    :param n: Float
    """
    multiplier = 5 ** decimals
    return math.floor(n * multiplier) / multiplier


def enemy_calc(u_attack, u_health, u_defence, lvl):
    enemy, result = [], []
    if lvl != 1:
        multiplier = round_down(random.uniform(0.4, 1.1), 1) 
    else:
        multiplier = 0.4
    print(multiplier)
    for stat in (u_attack, u_health, u_defence):
        enemy.append(round(stat*multiplier) if stat != 0 else 0)
        
    e_power = enemy[0]*(enemy[1]+enemy[2])
    formulae = int((e_power/(lvl**1.45))*2)
    result = [enemy, formulae if formulae > 1 else 2]
    
    return result

def exp_bosque(Nivel,ExpBase):

    Aleaorio = random.randint(1, Nivel)
    Aleaorio2 = random.randint(1, 100)
    exp =int(round(((ExpBase/Aleaorio2)*0.04+Aleaorio)/2))
    return exp


def recuperar(v_max,v_min):
         
    if v_min < v_max:
        v_min += 1
        print(v_min)
    sleep(0.3)


def climas_1():

    climas= ["Soleado☀️ ","Nublado🌤 ","Lluvioso🌧 " ,"Nieblina🌫 "]
    clima1 = climas[random.randint(0, 3)]
    
    return clima1

