import math
import matplotlib.pyplot as plt

#This code will be used to simulate the response of an RC filter

def calc_resp():
    #Function to calculate the frequency response
    
    #Give option for LP or HP filter
    filtType = input("Please Return what type of filter: ")
    print(filtType)
    
    #Create frequencies array (1 Hz to 10kHz
    freq = range(1,500)
    
    #Equation for impedance is X_c = 1/(2*pi*f*C)
    x_c = [1/(2*math.pi*float(f)*C) for f in freq]    


    #Get component values
    R = input("Please input value for resistor in ohms: ")
    

    if filtType == "LP":
        #Low Pass mode
        C = input("Please input low pass Capacitor Value in uF: ")
        #Vout = Vin*X_c/sqrt(R^2+X_c^2)
        Vout = [(Vin*x)/(math.sqrt(R*R+x*x)) for x in x_c]
        
    elif filtType == "HP":
        #High Pass mode
        C = input("Please input high pass Capacitor Value in uF: ")
        #Vout = Win*R/sqrt(R^2+X_c^2)
        Vout = [(Vin*R)/(math.sqrt(R*R+x*x)) for x in x_c]

    elif filterType == "BP":
        #Bandpass mode
        Cl = input("Please input low pass Capacitor Value in uF: ")
        Ch = input("Please input high pass Capacitor Value in uF: ")
        
        #Vout = Vin*X_hp/sqrt(X_lp^2+X_hp^2+R^2)

    else:
        print("Bruh")
        
    

    #Calculate logarithmic value
    VoutdB = [20*math.log10(v/Vin) for v in Vout]

    #Display the output of Vout
    #Figure 1, actual voltage
    plt.figure(1)
    plt.plot(freq, Vout)
    plt.title(filtType + " Filter frequency Response" + "R=" + str(R) + " C=" + str(C))
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("voltage (V)")


    #Figure 2 gain in dB
    plt.figure(2)
    plt.plot(freq, VoutdB)
    plt.title(filtType + " Filter frequency Response" + "R=" + str(R) + " C=" + str(C))
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("gain (dB)")
    plt.show()

    
    return True




#Start of main code
calc_resp()

