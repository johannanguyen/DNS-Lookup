"""
Johanna Nguyen
UCID: jn354
Section: 002
"""

#! /usr/bin/env python3
# DNS Server
import sys
import socket
import random
import struct

#Read server IP address and port from command-line arguments
serverIP = sys.argv[1]
serverPort = int(sys.argv[2])

#Create a UDP socket. Notice the use of SOCK_DGRAM for UDP packets
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#Assign server IP address and port number to socket
serverSocket.bind((serverIP, serverPort))

print("The server is ready to receive on port:", str(serverPort), ":\n")

#Receive data from client
packed, address = serverSocket.recvfrom(1024)

unpacked = struct.unpack_from("!hhihhs", packed)
formatLength = unpacked[3]

unpacked = struct.unpack_from("!hhihh{}s".format(formatLength), packed)


#Specify MESSAGE TYPE and IDENTIFIER
msgType = 2
identifier = unpacked[2]

#Adjust HOST NAME
packedHostName = str(unpacked[5])
hostName = packedHostName[2:-1]

#Lookup HOST NAME in database
f = open('dns-master.txt', 'r')
getLine = f.readline()
while(getLine != ''):
    contents = getLine.split()

    #Default the lookup to fail
    answer = "host-not-exist.student.test A IN"
    question = answer
    answerLength = len(answer)
    questionLength = len(question)
    returnCode = 1
    bytesA = bytes(answer, "utf-8")
    bytesQ = bytes(question, "utf-8")
    byteStrLen = len(bytesA)

    #Adjust QUESTION and ANSWER properly if match is found
    if contents[0] == hostName:
        question = hostName + " A IN"
        answer = question + " " + contents[3] + " " + contents[4]
        returnCode = 0
        bytesA = bytes(answer, "utf-8")
        bytesQ = bytes(question, "utf-8")
        answerLength = len(bytesA)
        questionLength = len(bytesQ)
        byteStrLen = len(bytesA) 
        break
    getLine = f.readline()
    
#Pack and send information to client
packed = struct.pack("!hhihh{}s{}s".format(questionLength, byteStrLen), msgType, returnCode, identifier, questionLength, answerLength, bytesQ, bytesA)
serverSocket.sendto(packed, address)


