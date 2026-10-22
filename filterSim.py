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

#Function to display and plot the output responses
def plot_freqResp(freq, Vout, VoutdB, filterType, Rlp, Rhp, Clp, Chp, cutoffLp, cutoffHp):
    if filterType == "Low Pass RC":
        #Plot the actual voltage
        print(cutoffLp)
        plt.figure(1)
        plt.plot(freq, Vout)
        plt.axvline(x=cutoffLp, color='red', linestyle='--')
        plt.title("Low Pass RC Circuit")
        componentVal = (
            "Rlp = " + str(Rlp) + "Ω\n"
            "Clp = " + str(Clp) + "F\n"
            "fc = " + str(cutoffLp) + "Hz\n"
        )
        plt.legend(plt.gca().lines, [componentVal], loc="upper right")
        #Plot the gain in dB
        plt.figure(2)
        plt.plot(freq, VoutdB)
        plt.axvline(x=cutoffLp, color='red', linestyle='--')
        plt.title("Low Pass RC Circuit Gain")
        componentVal = (
            "Rlp = " + str(Rlp) + "Ω\n"
            "Clp = " + str(Clp) + "F\n"
            "fc = " + str(cutoffLp) + "Hz\n"
        )
        plt.legend(plt.gca().lines, [componentVal], loc="upper right")
    elif filterType == "High Pass RC":
        #Plot the actual voltage
        plt.figure(1)
        plt.plot(freq, Vout)
        plt.axvline(x=cutoffHp, color='red', linestyle='--')
        plt.title("High Pass RC Circuit")
        componentVal = (
            "Rlp = " + str(Rhp) + "Ω\n"
            "Clp = " + str(Chp) + "F\n"
            "fc = " + str(cutoffHp) + "Hz\n"
        )
        plt.legend(plt.gca().lines, [componentVal], loc="upper left")
        #Plot the gain in dB
        plt.figure(2)
        plt.plot(freq, VoutdB)
        plt.axvline(x=cutoffHp, color='red', linestyle='--')
        plt.title("High Pass RC Circuit Gain")
        componentVal = (
            "Rlp = " + str(Rhp) + "Ω\n"
            "Clp = " + str(Chp) + "F\n"
            "fc = " + str(cutoffHp) + "Hz\n"
        )
        plt.legend(plt.gca().lines, [componentVal], loc="upper left")
    elif filterType == "RC Unbuffered Bandpass":
        pass

    plt.show()

#Function to change the layout when the dropdown is selected
def change_circuit(filterType, rlp, rhp, clp, chp, RCLP, RCHP, RCBP):
    if filterType == "Low Pass RC":
        print("Show low-pass layout")
        RCLP.show()
        RCHP.hide()
        RCBP.hide()
        chp.hide()
        clp.show()
        rhp.hide()
        rlp.show()
    elif filterType == "High Pass RC":
        print("Show high-pass layout")
        RCLP.hide()
        RCHP.show()
        RCBP.hide()
        chp.show()
        clp.hide()
        rhp.show()
        rlp.hide()
    elif filterType == "RC Unbuffered Bandpass":
        print("Show RC band-pass layout")
        RCLP.hide()
        RCHP.hide()
        RCBP.show()
        chp.show()
        clp.show()
        rhp.show()
        rlp.show()
    elif filterType == "----":
        print("No Circuit Chosen")
        RCLP.hide()
        RCHP.hide()
        RCBP.hide()
        chp.hide()
        clp.hide()
        rhp.hide()
        rlp.hide()
    else:
        print("Later")
    pass


#Function when the run button is pressed
def run_button(resistance1, resistance2, hpCapacitor, lpCapacitor, circuitType, freqStart, freqEnd, Vin):
    #Take values from the text boxes
    filtType = circuitType.currentText()
    freqStart = int(freqStart.text())
    freqEnd = int(freqEnd.text())
    Vin = float(Vin.text())
    calc_resp(resistance1, resistance2, hpCapacitor, lpCapacitor, filtType, freqStart, freqEnd, Vin)

    return

#This code will be used to simulate the response of an RC filter
def calc_resp(Rlp, Rhp, Chp, Clp, filtType, freqStart, freqEnd, Vin):    
    #Function to calculate the frequency response
    #Create frequency range. Error checking
    #Set default to 1 Hz to 1kHz
    if freqStart < 1:
        freqStart = 1
    if freqEnd <= freqStart:
        freqEnd = freqStart + 1000

    freq = range(freqStart,freqEnd)
    
    if filtType == "Low Pass RC":
        #Low Pass mode
        Rlp = float(Rlp.text())
        Clp = float(Clp.text())*1e-6
        #Vout = Vin*X_c/sqrt(R^2+X_c^2)
        #Equation for impedance is X_c = 1/(2*pi*f*C)
        x_c = [1/(2*math.pi*float(f)*Clp) for f in freq]    
        Vout = [(Vin*x)/(math.sqrt(Rlp*Rlp+x*x)) for x in x_c]
        
    elif filtType == "High Pass RC":
        #High Pass mode
        Rhp = float(Rhp.text())
        Chp = float(Chp.text())*1e-6
        #Equation for impedance is X_c = 1/(2*pi*f*C)
        x_c = [1/(2*math.pi*float(f)*Chp) for f in freq]    
        #Vout = Win*R/sqrt(R^2+X_c^2)
        Vout = [(Vin*Rhp)/(math.sqrt(Rhp*Rhp+x*x)) for x in x_c]
    else:
        print("Add other circuits later")
        
    
    #Calculate logarithmic value
    VoutdB = [20*math.log10(v/Vin) for v in Vout]

    #Calculate the cutoff frequency
    if filtType == "Low Pass RC":
        cutoffLp = 1/(2*math.pi*Rlp*Clp) #1/2piRC
        cutoffHp = 0
    elif filtType == "High Pass RC":
        cutoffLp = 0
        cutoffHp = 1/(2*math.pi*Rhp*Chp) #1/2piRC


    #Display output function
    plot_freqResp(freq, Vout, VoutdB, filtType, Rlp, Rhp, Clp, Chp, cutoffLp, cutoffHp)


    return True

#Define GUI function
def start_GUI():
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


    #Adding component values
    lpResistanceBox = QLineEdit()
    lpResistanceBox.setPlaceholderText("Enter Resistance in Ohms For LP")
    hpResistanceBox = QLineEdit()
    hpResistanceBox.setPlaceholderText("Enter Resistance in Ohms For HP")

    lpCapacitorBox = QLineEdit()
    lpCapacitorBox.setPlaceholderText("Enter low Pass Capacitance in uF")

    hpCapacitorBox = QLineEdit()
    hpCapacitorBox.setPlaceholderText("Enter High Pass Capacitance in uF")

    #Create dropdown
    filterDropDn = QComboBox()
    filterDropDn.addItem("----")
    filterDropDn.addItem("Low Pass RC")
    filterDropDn.addItem("High Pass RC")
    filterDropDn.addItem("RC Unbuffered Bandpass")
    filterDropDn.addItem("RC Buffered Bandpass")
    filterDropDn.addItem("RLC Series Bandpass")
    filterDropDn.addItem("RLC Parallel Bandpass")

    #Create Calculate button
    calcButton = QPushButton("Calculate")
 
    #Add input voltage
    vinBox = QLineEdit()
    vinBox.setPlaceholderText("Enter the input voltage in V")

    #Add frequency range
    #horizontal box
    freqRange = QHBoxLayout()
    freqStart = QLineEdit()
    freqStart.setPlaceholderText("Enter start frequency in Hz")
    freqEnd = QLineEdit()
    freqEnd.setPlaceholderText("Enter end frequency in Hz")
    freqRange.addWidget(freqStart)
    freqRange.addWidget(freqEnd)

    #Resise column
    col1.addWidget(filterDropDn)
    col1.addStretch()
    col1.addWidget(vinBox)
    col1.addLayout(freqRange)
    col1.addWidget(lpResistanceBox)
    col1.addWidget(hpResistanceBox)
    col1.addWidget(lpCapacitorBox)
    col1.addWidget(hpCapacitorBox)
    col1.addWidget(calcButton)


    #########################
    #Right Column
    ########################

    #Pictures of each circuit
    RCLowPassImg = QPixmap("RCLP.webp")
    RCHighPassImg = QPixmap("RCHP.webp")
    RCBandPassImg = QPixmap("fil85.webp")

    #Check if image loaded properly
    if RCLowPassImg.isNull():
        print("Error: RC low pass image could not be loaded")
    if RCHighPassImg.isNull():
        print("Error: RC high pass image could not be loaded")
    if RCBandPassImg.isNull():
        print("Error: Image could not be loaded")


    #Image scaling
    RCLowPassLabel = QLabel()
    RCHighPassLabel = QLabel()
    RCBandPassLabel = QLabel()

    RCLowPassLabel.setPixmap(RCLowPassImg)
    RCLowPassLabel.setMinimumSize(400,150)

    RCHighPassLabel.setPixmap(RCHighPassImg)
    RCHighPassLabel.setMinimumSize(400,150)

    RCBandPassLabel.setPixmap(RCBandPassImg)
    RCBandPassLabel.setMinimumSize(400,150)

    col2.addWidget(RCLowPassLabel)
    col2.addWidget(RCHighPassLabel)
    col2.addWidget(RCBandPassLabel)
    


    layout.addLayout(col1,30)
    layout.addLayout(col2,70)
    window.setLayout(layout)

    #Button or dropdown pressed
    filterDropDn.currentTextChanged.connect(lambda filter_type: change_circuit(filter_type, lpResistanceBox, hpResistanceBox, lpCapacitorBox, hpCapacitorBox, RCLowPassLabel, RCHighPassLabel, RCBandPassLabel))
    calcButton.clicked.connect(lambda: run_button(lpResistanceBox, hpResistanceBox, hpCapacitorBox, lpCapacitorBox, filterDropDn, freqStart, freqEnd, vinBox))
    


    #Hide initial widgets, Keep only drop down and calculate button
    RCLowPassLabel.hide()
    RCHighPassLabel.hide()
    RCBandPassLabel.hide()
    lpResistanceBox.hide()
    hpResistanceBox.hide()
    hpCapacitorBox.hide()
    lpCapacitorBox.hide()
    sys.exit(app.exec())


#Start of main code
start_GUI()


#calc_resp()


    # #Display the output of Vout
    # #Figure 1, actual voltage
    # plt.figure(1)
    # plt.plot(freq, Vout)
    # plt.title(filtType + " Filter frequency Response" + "R=" + str(Rlp) + " C=" + str(Clp))
    # plt.xlabel("Frequency (Hz)")
    # plt.ylabel("voltage (V)")


    # #Figure 2 gain in dB
    # plt.figure(2)
    # plt.plot(freq, VoutdB)
    # plt.title(filtType + " Filter frequency Response" + "R=" + str(Rlp) + " C=" + str(Clp))
    # plt.xlabel("Frequency (Hz)")
    # plt.ylabel("gain (dB)")
    # plt.show()
