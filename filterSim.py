import math
import matplotlib.pyplot as plt

#This code will be used to simulate the response of an RC filter

def calc_resp():
    #Function to calculate the frequency response
    
    #Give option for LP or HP filter
    filtType = input("Please Return what type of filter: ")
    print(filtType)
    
    #Find the Resistor value and capacitance value
    R = float(input("Please enter resistance in terms of ohms: "))
    C = float(input("Please enter capacitance in terms of uF: "))
    C = C*1e-6
    Vin = float(input("Please enter input voltage in terms of V: "))
    
    #Create frequencies array (1 Hz to 10kHz
    freq = range(1,10000)
    
    #Equation for impedance is X_c = 1/(2*pi*f*C)
    x_c = [1/(2*math.pi*float(f)*C) for f in freq]    

    if filtType == "LP":
        #Low Pass mode
        #Vout = Vin*X_c/sqrt(R^2+X_c)
        Vout = [(Vin*x)/(math.sqrt(R*R+x*x)) for x in x_c]
    


        print("Yay")
    elif filtType == "HP":
        print("yay2")
    else:
        print("Bruh")
        

    #Display the output of Vout
    plt.plot(freq, Vout)
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Vout (V)")
    plt.show()
    
    return True




#Start of main code
calc_resp()

