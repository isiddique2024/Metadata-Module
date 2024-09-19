import socket
import bson
import hashlib
import datetime
import json
import random
from publisher import publish_to_rabbitmq # to make messageSender functional

class statusFeed:
    @staticmethod
    def messageBuilder(content_ID):
        messageID = str(random.random())
        contentID = content_ID # other functions will pass this parameter        
        #status = from other modules       
        cts = datetime.datetime.now() # current timestamp
        format_cts = cts.strftime('%Y-%m-%d %H:%M:%S') # formatting
        #details = from other modules

        #other inputs/variables as necessary 

        #build BSON Builder
        job = { 
            "JobID": messageID,  
            "contentID": contentID,
            "Status": 1,
            "timestamp": format_cts,
            "details": 1
        }
        print(job)
        # send back to messageSender
        messageSender(job)

#This sends to our rabbitMQ publisher .. Like their parse.py Choose a port and have our publisher listen on that port
def messageSender(bsonObj):
    #sending to port
    port = '1234'
    publish_to_rabbitmq(port, bsonObj)
    
# main function
if __name__ == '__main__':
    user_input = input("Enter contentID: ")
    statusFeed.messageBuilder(user_input)