import socket
import bson
import hashlib
import datetime
import json
import random
#-----------------------------------SEKAI--------------------------------------------#
#this function will create messages for the DEMO, we will modify this to have other functions call it.



class statusFeed:
    @staticmethod
    def messageBuilder(content_ID):
        contentID = content_ID #other functions will pass this parameter
        messageID = str(random.random())
        print("Type a status")
        #status = input
        #timestamp
        #other inputs/variables as necessary 

        #build BSON Builder





#This sends to our rabbitMQ publisher .. Like their parse.py Choose a port and have our publisher listen on that port
def messageSender(bsonObj):
    port = '1234'
    #send to port



if __name__ == '__main__':
    print("Enter a contetnID")
    #asks for input 
    
    #call function - pass input
    
#-----------------------------------Isaam--------------------------------------------#

#-----------------------------------Akeno--------------------------------------------#
#your code here
#-----------------------------------Dylan--------------------------------------------#
#your code here
#-----------------------------------BigDawg--------------------------------------------#
#your code here
