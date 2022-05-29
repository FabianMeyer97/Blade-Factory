from mcculw import ul
from mcculw.enums import ULRange
from mcculw.ul import ULError
import time

board_num = 0
channel = 0
ai_range = ULRange.BIP5VOLTS
scale = 0 #Celsius
#scale = 2 #Kelvin

print(ul.get_board_name(board_num))

def get_temp():
    return ul.t_in(board_num, channel, scale)


cool = True
while cool:
    val = input("1 für Temp, 2 für beenden")

    if int(val) == 1:
        print(get_temp())
    else:
        cool = False


































