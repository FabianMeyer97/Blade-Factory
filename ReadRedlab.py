from mcculw import ul
from mcculw.enums import ULRange
from mcculw.ul import ULError
import numpy as np


def initialize_board_one():
    board_num = 0
    channel = 0
    ai_range = ULRange.BIP5VOLTS
    scale = 0 #Celsius
    #scale = 2 #Kelvin
    return board_num, channel, ai_range, scale

def get_temp():   
    board_num, channel, ai_range, scale = initialize_board_one() 
    return ul.t_in(board_num, channel, scale)

def filter_temp():
    avg10 = []
    for i in range(10):
        avg10.append(get_temp())
    avg10.remove(max(avg10)) #Testen ob mehr als eine stelle entfernt wird!!! In dem Fall ändern
    avg10.remove(min(avg10))
    #Build in additional Einschränkungen, 
    avg_temp = 0
    for i in range(len(avg10)):     
        avg_temp += avg10[i]
    avg_temp /= len(avg10)
    return avg_temp
    
filter_temp()

"""
cool = True
while cool:
    val = input("1 für Temp, 2 für beenden")

    if int(val) == 1:
        print(get_temp())
    else:
        cool = False
"""