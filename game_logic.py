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

def drop_recuros():
    madruga = 16
    dia = 5
    tarde = 11
    noche = 19
    
    c = random.randint(1, 81)
    
    return c

def item_drop(chance):
    """
    :param chance: Mob's chance of drop
    :return: True/False
    """
    c = random.randint(1, 100)
    if c >= chance:
        return True
    return True

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

def exp_bosque(d_max ,a_min , lvl):
    
    Ataque_bosque = random.randint(0, lvl)
    Defensa_bosque = random.randint(0, lvl)
    
    exp =int(round((d_max + a_min) -  ( Defensa_bosque + Ataque_bosque) ) * (lvl**0.04))
    
    return exp


def recuperar(v_max,v_min):
         
    if v_min < v_max:
        v_min += 1
        print(v_min)
    sleep(0.3)
        
    