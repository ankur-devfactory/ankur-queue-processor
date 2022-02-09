# ankur-queue-processor
This applications takes a SQS message as an Input and if there are some banned words present in the Input, it triggers a notification to email.

# Banned Words
```
"apple", "banana", "cherry", "mango", "strawberry"
```

# To deploy the application run the following in the AWS CLI:
```
aws cloudformation deploy \
--template-file cloudformation/template.yaml \
--stack-name tpm-2015 \
--parameter-overrides SubscriptionEmail="replace_me_with@your.email" \
--capabilities CAPABILITY_NAMED_IAM
```
**Note:** Please replace 'replace_me_with@your.email' with your email and subscibe to the SNS Notification on your email.

# To test the application run the following in the AWS CLI:

###### Case With Banned Words:
```
aws sqs send-message \
--queue-url "https://sqs.us-east-1.amazonaws.com/162174280605/Ankur-SQS-Queue" \
--message-body '{"productID": "xyzzy420","textFields": {"title": "How to use Cloud apple","description": "apple orange Test apple."}}'
```

###### Case Without Banned Words:
```
aws sqs send-message \
--queue-url "https://sqs.us-east-1.amazonaws.com/162174280605/Ankur-SQS-Queue" \
--message-body '{"productID": "xyzzy420","textFields": {"title": "abcd defgh"}}'
```
