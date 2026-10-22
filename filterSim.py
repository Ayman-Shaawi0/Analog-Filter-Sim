import math
import matplotlib.pyplot as plt
import sys

import os
os.environ["QT_QPA_PLATFORMTHEME"] = "generic"

from PyQt6.QtWidgets import(
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QComboBox
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

#Function when the run button is pressed
def run_button(resistance, hpCapacitor, lpCapacitor):
    #Take values from the text boxes
    R = float(resistance.text())
    Chp = float(hpCapacitor.text())
    Clp = float(lpCapacitor.text())

    return





#This code will be used to simulate the response of an RC filter

def calc_resp():
    #Function to calculate the frequency response
    
    #Give option for LP or HP filter
    filtType = input("Please Return what type of filter: ")
    print(filtType)
    
    #Create frequencies array 1 Hz to 1.5kHz
    freq = range(1,500)
    
    #Equation for impedance is X_c = 1/(2*pi*f*C)
    x_c = [1/(2*math.pi*float(f)*C) for f in freq]    


    #Get component values
    R = input("Please input value for resistor in ohms: ")
    Vin = input("Please input value for input voltage in V: ")

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

    elif filtType == "BP":
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
app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("Analog Filter Sim")
window.resize(800, 500)
window.show()

#Layout
layout = QHBoxLayout()
col2 = QVBoxLayout()
col1 = QVBoxLayout()

#########################
#Left Column
########################

#Create dropdown
filterDropDn = QComboBox()
filterDropDn.addItem("Frequency Cutoff Calculate")
filterDropDn.addItem("Component Calculate")

#Adding component values
resistanceBox = QLineEdit()
resistanceBox.setPlaceholderText("Enter Resistance in Ohms")

hpCapacitorBox = QLineEdit()
hpCapacitorBox.setPlaceholderText("Enter High Pass Capacitance in uF")

lpCapacitorBox = QLineEdit()
lpCapacitorBox.setPlaceholderText("Enter low Pass Capacitance in uF")

#Create Calculate button
calcButton = QPushButton("Calculate")
calcButton.clicked.connect(lambda: run_button(resistanceBox, hpCapacitorBox, lpCapacitorBox))


#Resise column
col1.addWidget(filterDropDn)
col1.addStretch()
col1.addWidget(resistanceBox)
col1.addWidget(hpCapacitorBox)
col1.addWidget(lpCapacitorBox)
col1.addWidget(calcButton)


#########################
#Right Column
########################

#Picture on right
image = QPixmap("fil85.webp")

if image.isNull():
    print("Error: Image could not be loaded")

image_label = QLabel()

image_label.setPixmap(image)
image_label.setMinimumSize(400,500)

col2.addWidget(image_label)



layout.addLayout(col1,30)
layout.addLayout(col2,70)
window.setLayout(layout)



sys.exit(app.exec())
#calc_resp()

