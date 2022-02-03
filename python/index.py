from __future__ import print_function
import json
import boto3
import os

def lambda_handler(event, context):
    # List of Hard Coded Banned Words
    bannedWords = ["apple", "banana", "cherry", "mango", "strawberry"]
    
    
    for record in event['Records']:
        payload = record["body"]
        
        #Validate Input format to be JSON 
        try:
            json.loads(payload)
        except ValueError as e:
            print("Error! The Reuest format was not correct.")
            print("Request:")
            print(payload)
            return {
                    'statusCode': 200,
                    'body': json.dumps('Request format is not correct!')
            }
        
        #Convert received message into Dict
        final_payload = eval(payload)
        bannedWordFlag = False
        
        
        #Check atleast productID and textfields is present in Request
        if "textFields" in final_payload and "productID" in final_payload:
            #Get the textFields to check the Banned Words
            textFields = final_payload.get('textFields')
        else:
            print("Error! The Request format was not correct.")
            print("Request:")
            print(final_payload)
            return {
                    'statusCode': 200,
                    'body': json.dumps('Request format is not correct!')
            }
        #Use set as only one occurunce of banned word is needed if found
        bannedWordFound = set([])
        
        #Iterate for each banned word
        for bannedWord in bannedWords:
            #Iterate for all the elements in textFields
            for i in textFields:
                #Convert to lowercase so that only lowercase comparison is required
                textfieldLowerCase = textFields[i].lower()
                
                #Check if banned word exist
                if(textfieldLowerCase.find(bannedWord) != -1):
                    bannedWordFlag = True
                    bannedWordFound.add(bannedWord)
        
        if (bannedWordFlag):
            bannedWordSNSDict = dict([('productID', final_payload['productID']), ('flaggedWords', list(bannedWordFound))])
            topicArn = os.environ['snsARN']
            snsClient = boto3.client('sns')
            
            #Publish message to SNS
            snsClient.publish(TopicArn=topicArn, Message=json.dumps(bannedWordSNSDict), Subject="Banned Words in message!")
        return {
                    'statusCode': 200,
                    'body': json.dumps('Message Processed')
            }