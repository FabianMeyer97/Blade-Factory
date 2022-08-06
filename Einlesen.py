#import nidaqmx
import random
import mcculw
from mcculw import ul
from mcculw.enums import ULRange
import mcculw.ul 
import ReadRedlab

activeDAQ = ReadRedlab.rlabDAQInput(1)

def readRED():
    board_num = 0
    channel = 0
    ai_range = mcculw.enums.ULRange.BIP5VOLTS

    
        # Get a value from the device
    value = mcculw.a_in(board_num, channel, ai_range)
        # Convert the raw value to engineering units
        #eng_units_value = mcculw.ul.to_eng_units(board_num, ai_range, value)
    
        # Display the raw value
    print("Raw Value: " + str(value))
        # Display the engineering value
        #print("Engineering Value: " + '{:.3f}'.format(eng_units_value))
    #except ULError as e:
        # Display the error
     #   print("A UL error occurred. Code: " + str(e.errorcode)
      #    + " Message: " + e.message)

#readRED()


def readTemp():
    with nidaqmx.Task() as task:
        task.ai_channels.add_ai_voltage_chan("Dev1/ai0")
        volt = task.read()
    return volt

def buildAVG(NumberofMeasurements):
    voltAVG = 0
    k = 0
    for i in range(NumberofMeasurements):
        volt = readTemp()
        if volt > 0:
            voltAVG += volt
            k +=1       
    voltAVG /= k        
    return voltAVG
                       
#voltAVG = buildAVG(20)


def VoltToCelsius():
    voltAVG = buildAVG(20)
    tempAVG = voltAVG*10000    
    return tempAVG
#tempAVG = VoltToCelsius()



def getTemperature(NumberOfMeasurements, **kwargs):
    """  
    with nidaqmx.Task() as task:
        task.ai_channels.add_ai_voltage_chan("Dev1/ai0")
        volt = task.read()
        
    voltAVG = 0
    k = 0
    
    for i in range(NumberOfMeasurements):
        volt = readTemp()
        if volt > 0:
            voltAVG += volt
            k +=1       
    voltAVG /= k 
    
    tempAVG = (voltAVG*10000)+20 
    """
    """
    tempAVG = random.randint(40,41)
    return tempAVG+273.15
    """
    channel = 1
    if "channel" in kwargs:
        channel=kwargs["channel"]
    #board_num = 0
    #channel = 0
    value = activeDAQ.filtered_temp(n=NumberOfMeasurements, channel=channel) #ReadRedlab.filtered_temp()
    #ai_range = mcculw.enums.ULRange.BIP5VOLTS    
    # Get a value from the device
    #value = ul.a_in(board_num, channel, ai_range)
    #value = ul.t_in(board_num, channel, 0)
    # Convert the raw value to engineering units
    #eng_units_value = mcculw.ul.to_eng_units(board_num, ai_range, value)
    # Display the raw value
    #print("Raw Value: " + str(value))
    # Display the engineering value
    #print("Engineering Value: " + '{:.3f}'.format(eng_units_value))
    #except ULError as e:
    # Display the error
    #   print("A UL error occurred. Code: " + str(e.errorcode)
    #    + " Message: " + e.message)
    return value




#print(getTemperature(10))


"""
def readTempAVG(NumberofMeasurements):
    with nidaqmx.Task() as task:
        volt = 0
        k = 0
        for i in range(NumberofMeasurements):
            task.ai_channels.add_ai_voltage_chan("Dev1/ai0")
            measuredVoltage = task.read()
            if measuredVoltage > 0:
                volt += task.read()   
                k += 1
    volt /= k           
    return volt
"""