##Run this script after the Arduino sketch has finished uploading (otherwise there will be errors uploading the sketch)

import serial

serial_port='COM7' ##type in your serial port
baud_rate=9600 ##must match baud in Serial.begin of Arduino sketch 
output="Output_test.csv" ##Adjust to desired filename 
ser=serial.Serial(serial_port,baud_rate)
print("Connection established")
##remember to open output file 
output_file = open(output, "w+");

headerstring = "Time,Sensor1,Sensor2,Sensor3" #Adjust headerstring to match number of sensors and use appropriate muscle names for each EMG sensor
print(headerstring, file = output_file)

while True:
    try: 
        line=ser.readline()
        line=line.decode("utf-8")
        line = line.strip() #removes extra newlines 
        print(line) ##prints to python terminal 
        print(line, file = output_file) #writes to output file
    except KeyboardInterrupt: #added to end the program after it runs for long enough
        print("\nYou have finished recording")
        output_file.close()
        ser.close()
        break
    except Exception as ex:
        print("\nAn alternate error has occurred")
        print(ex)
        output_file.close()
        ser.close()
        raise 
        

