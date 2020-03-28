"""
Johanna Nguyen
UCID: jn354
Section: 002
"""

#! /usr/bin/env python3
# Ping Client
import sys
import socket
import time
import struct
import random

#Get the server hostname, port and data length as command line arguments
host = sys.argv[1]
port = int(sys.argv[2])
hostName = sys.argv[3]

#Specify MESSAGE TYPE and IDENTIFIER; HOST NAME length used for packing format
msgType = 1
identifier = random.randint(1, 100)
clientH = hostName + " A IN"
bytesH = bytes(hostName, 'utf-8')
hLength = len(bytesH)

#Create UDP client socket. Note the use of SOCK_DGRAM
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientsocket.settimeout(1)


try:
    #Send data to server
    packed = struct.pack("!hhihh{}s".format(hLength), msgType, 0, identifier, hLength, 0, bytesH)
    clientsocket.sendto(packed, (host, port))

    #Receive the server response, save unpacked data as variables
    dataEcho, address = clientsocket.recvfrom(1024)
    received = struct.unpack_from("!hhihhss", dataEcho)

    #Specify QUESTION and ANSWER length from packed data, used as unpacking format
    qLength = received[3]
    aLength = received[4]

    #Unpack data from server
    received2 = struct.unpack_from("!hhihh{}s{}s".format(qLength, aLength), dataEcho)

    #Create variables for each unpacked data entry
    returnCode = received2[1]
        
    question = str(received2[5])
    question = question[2:-1]

    answer = str(received2[6])
    answer = answer[2:-1]

    #Print the results
    print("\nSending request to:", str(host), ",", str(port))
    print("Message ID:\t\t", identifier)
    print("Question Length:\t", str(qLength), "bytes")
    print("Answer Length:\t\t 0 bytes")
    print("Question:\t\t", question)

    #Print the results strictly received from server
    print("\nReceived Response from:", str(host),",", str(port))

    #Different RETURN CODE prints if question is found or not
    if(received[1] == 1):
        aLength = 0
        print("Return Code:\t\t", returnCode, "(Name does not exist)")
    else:
        print("Return Code:\t\t", returnCode, "(No errors)")
            
    print("Message ID:\t\t", identifier)
    print("Question Length:\t", qLength, "bytes")
    print("Answer Length:\t\t", aLength, "bytes")
    print("Question:\t\t", question)

    #Only print ANSWER if question is found
    if(returnCode == 0):
        print("Answer:\t\t\t", answer)

#Print results for when server does not respond
except socket.timeout:
    question = hostName + " A IN"
    qLength = len(question)
    aLength = 0

    print("\nSending request to:", str(host), ",", str(port))
    print("Message ID:\t\t", identifier)
    print("Question Length:\t", qLength, "bytes")
    print("Answer Length:\t\t 0 bytes")
    print("Question:\t\t", question)
    print("\nRequest timed out...")
    
    for i in range(2):
        print("Sending request to:", str(host), ",", str(port))
        print("\nRequest timed out...")
    print("Exiting program...")

#Close the client socket
clientsocket.close()

