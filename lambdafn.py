import json
import boto3
import openai  # Use Meta LLaMA 3 API if needed
import os

# AWS DynamoDB client
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("ChatbotConversations")

# OpenAI API Key (or Meta LLaMA 3)
openai.api_key = os.getenv("OPENAI_API_KEY")

def lambda_handler(event, context):
    body = json.loads(event["body"])
    session_id = body["session_id"]
    user_input = body["message"]

    # Generate AI response
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": user_input}]
    )

    bot_reply = response["choices"][0]["message"]["content"]

    # Store in DynamoDB
    table.put_item(
        Item={"SessionID": session_id, "UserMessage": user_input, "BotReply": bot_reply}
    )

    return {"statusCode": 200, "body": json.dumps({"reply": bot_reply})}
