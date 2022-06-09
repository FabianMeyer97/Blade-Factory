from mcculw import ul

def initialize_board_one():
    #Gets board Number, Channel and Scale for 
    board_num = 0 
    channel = 1
    scale = 0 #0 for Celsius,  2 for Kelvin
    return board_num, channel, scale

def get_temp():   
    board_num, channel, scale = initialize_board_one() 
    return ul.t_in(board_num, channel, scale)

def filtered_temp():
    avg10 = []
    for i in range(10):
        avg10.append(get_temp())
    avg10.remove(max(avg10))
    avg10.remove(min(avg10))
    #Might need additional einschränkungen:
        #MEdian Einbauen
    avg_temp = 0
    for i in range(len(avg10)):     
        avg_temp += avg10[i]
    avg_temp /= len(avg10)
    
    """
    for el in avg10:
        if el > 1.5*avg_temp or el < 0.5*avg_temp:
            avg10.remove(el)
    """
    return avg_temp


while True:
    input("Get Temp")    
    print(filtered_temp())
