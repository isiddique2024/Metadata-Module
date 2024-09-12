import socket
import bson
import hashlib
import datetime
import json
import random
#-----------------------------------SEKAI--------------------------------------------#
#this function will create messages for the DEMO, we will modify this to have other functions call it.
# jobID:
# contentID
# Status: Sent to GraphDB
# timestamp:
# details:


class statusFeed:
    #@staticmethod
    def messageBuilder(content_ID):
        contentID = content_ID #other functions will pass this parameter
        messageID = str(random.random())
        #status = input
        #timestamp current
        #other inputs/variables as necessary 

        #build BSON Builder
        job = { 
            "JobID": messageID,  
            "contentID": contentID,
            "Status": 1,
            "timestamp": 2,
            "details": 1
        } # send back to messageSender (return)
        print(job)




#This sends to our rabbitMQ publisher .. Like their parse.py Choose a port and have our publisher listen on that port
#def messageSender(bsonObj):
 #   port = '1234'
    #send to port



#if __name__ == '__main__':
#    print("Enter a contetnID")
    #asks for input 
    
    #call function - pass input
user_input = input("contenID")
print("Hello, " + user_input + "!")

result = statusFeed.messageBuilder(user_input)
print(result)
#-----------------------------------Isaam--------------------------------------------#

#-----------------------------------Akeno--------------------------------------------#
#your code here
#-----------------------------------Dylan--------------------------------------------#
#your code here
#-----------------------------------BigDawg--------------------------------------------#
#your code here
