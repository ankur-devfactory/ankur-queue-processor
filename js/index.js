const AWS = require('aws-sdk');
const sns = new AWS.SNS();

exports.handler = async (event) => {
    
    const records = event.Records;
    // define flagged words
    const flaggedWords = ["apple", "banana", "orange", "strawberry", "cherry"];
    const promises = [];
    records.forEach(record => {
        // Check the SQS Message in JSON format
        try{
            JSON.parse(record.body);
        } catch{
            console.log("error!");
            console.log("Please check the request format");
            const err_text = {
                    statusCode: 400,
                    body: JSON.stringify('Bad Request!'),
             };
            return err_text;
        }
        // Get the SQS Message 
        const message = JSON.parse(record.body);
        // Get the productID
        const productID = message.productID;
        // Get the Text Fields
        const textFields = message.textFields;
        
        // Mandatory fields if they don't exist then return as nothing else to do
        if (typeof textFields === 'undefined' ||  productID === 'undefined') {
            console.log("error!");
            console.log("Please check the request forma");
            const err_text = {
                    statusCode: 400,
                    body: JSON.stringify('Bad Request!'),
             };
            return err_text;
        }
        
        // Create Set to store the flagged words
        let flaggedWordsFound = new Set();
        
        // Flag to determine is any flagged word exist in the message
        let flaggedWordFlag = false;
        
        for (const textField_key in textFields) {
            let textFieldsLowerCase = textFields[textField_key].toLowerCase();
            flaggedWords.forEach(flaggedWord => {
                if (textFieldsLowerCase.includes(flaggedWord)) {
                    // Flagged Word Found
                    flaggedWordsFound.add(flaggedWord);
                    flaggedWordFlag = true;
                }
            });
        }
        
        if (flaggedWordFlag){
            // Create the message to be send back
            const response_text = {
                productID: productID,
                flaggedWords: Array.from(flaggedWordsFound)
            };
            console.log(JSON.stringify(response_text));
            
            // Create the JSON parameters which are required
            const params = {
                Message: JSON.stringify(response_text),
                TopicArn: process.env.snsARN
            };
            
            // Publish the message to SNS
            const response = sns.publish(params);
            
            
            promises.push(response.promise());
            
        }
        
    }) 
    // Wait until the message is publis to the SNS
    await Promise.all(promises);
};
