from __future__ import print_function
import json
import boto3
import os

def lambda_handler(event, context):
    # List of Hard Coded Banned Words
    bannedWords = ["apple", "banana", "cherry", "mango", "strawberry"]
    
    
    for record in event['Records']:
        payload = record["body"]
        #Convert received message into Dict
        final_payload = eval(payload)
        
        #Get the textFields to check the Banned Words
        textFields = final_payload.get('textFields')
        bannedWordFlag = False
        if "textFields" in final_payload:
            textFields = final_payload.get('textFields')
        else:
            return {
                    'statusCode': 200,
                    'body': json.dumps('textFields doesnt exists')
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
