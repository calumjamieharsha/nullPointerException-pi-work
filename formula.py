#Import classes we need
from sense_hat import SenseHat

from CPUTemp import temp_calc

#Set instance of classes to a variable
sense = SenseHat()





#Pressure at sea level - Value is assumed to be constant
P_SEALEVEL = 102400 #Pa


p_current = sense.get_pressure()*100#*100 is to convert millibars to Pascals 
print (p_current)

pressure = P_SEALEVEL/p_current

temp = round(temp_calc,2)

numerator = ((pressure ** (1/5.257)) - 1) * (10 + 273.15)

h = numerator/0.0065

print("height is %d" %h)

