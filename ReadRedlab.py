from mcculw import ul
import statistics

class rlabDAQInput:
    board_num = 0 
    scale = 0 #0 for Celsius,  2 for Kelvin

    def __init__(self, channel):
        self.channel = channel    # instance variable unique to each instance
        
    def get_temp(self):   
        return ul.t_in(self.board_num, self.channel, self.scale)
    def get_temp_ch(self,channel):   
        return ul.t_in(self.board_num, channel, self.scale)
    
    def filtered_temp(self, **kwargs):
        # number of measurements defined?
        if "n" in kwargs:
            n=kwargs["n"]
        else:
            n = 10
        # channel defined?
        localchannel = self.channel
        if "channel" in kwargs:
            self.channel=kwargs["channel"]
            localchannel = kwargs["channel"]
        
        avg10 = []
        for i in range(n):
            avg10.append(self.get_temp_ch(localchannel))
        avg10.remove(max(avg10))
        avg10.remove(min(avg10))
        avg10.remove(max(avg10))
        avg10.remove(min(avg10))
        avg_temp = 0
        for i in range(len(avg10)):     
            avg_temp += avg10[i]
        avg_temp /= len(avg10)
        # use Median instead?
        #med_temp = statistics.median(avg10)
        return avg_temp


# def initialize_board_one():
#     #Gets board Number, Channel and Scale for 
#     board_num = 0 
#     channel = 1
#     scale = 0 #0 for Celsius,  2 for Kelvin
#     return board_num, channel, scale

# def get_temp():   
#     board_num, channel, scale = initialize_board_one() 
#     return ul.t_in(board_num, channel, scale)

# def filtered_temp():
#     avg10 = []
#     for i in range(10):
#         avg10.append(get_temp())
#     avg10.remove(max(avg10))
#     avg10.remove(min(avg10))
#     #Might need additional einschränkungen:
#         #MEdian Einbauen
#     avg_temp = 0
#     for i in range(len(avg10)):     
#         avg_temp += avg10[i]
#     avg_temp /= len(avg10)
    
#     med_temp = statistics.median(avg10)
  
#     return avg_temp

if __name__ == "__main__":
    channel1 = rlabDAQInput(channel=0)
    while input("Get Temp (enter 'q' to quit):") != "q" :
        print(channel1.filtered_temp())
