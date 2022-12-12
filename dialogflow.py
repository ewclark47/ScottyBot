from flask import Flask, request
from os import environ
from dotenv import load_dotenv
import database_functions
import openai
from gpt3 import gpt3

load_dotenv()

openai.api_key = environ["OPENAI_API_KEY"]

gpt3 = gpt3(openai.api_key)
app = Flask(__name__) # used ngrok to listen to port 5000 so that 
# the dialogflow webhook works with flask
# command for command line: ngrok http 5000


@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    print("Received request from df")
    req = request.get_json(silent = True, force=True)
    print(req)
    fulfillmentText = ''
    df_query = req.get('queryResult') 
    df_intent = df_query.get('intent')
    action = ''
    if "displayName" in df_intent.keys():
        action = df_intent['displayName']
    message = df_query.get('queryText')
    params = df_query.get('parameters') # this is a dictionary
    print("retrieved necessary info, starting switch statement")
    # pull the user ID from the original slack payload
    user = ''
    slack_og = req.get('originalDetectIntentRequest')
    slack_payload = slack_og.get('payload')
    slack_data = slack_payload.get('data')
    slack_event = slack_data.get('event')
    user = slack_event['user'] 
    #print(user)
    fulfillmentText = switch(action, message, user)


    return {
        "fulfillmentText": fulfillmentText,
        "source": "webhookdata"
    }
    

def switch(action, message, user):
    print("started switch statment. responding based on action: " + action)
    df_response ="Sorry, I didn't quite get that"
    if action == "AddCourse":
        # input the database function here with the user
        df_response = "Dialogflow says adding course stuff here"

    elif action == "DropCourse":
        # input the database function here with the user
        df_response = "Dialogflow says dropping course stuff here"
    elif action == "FindCourse":
        # input the database function here with the user
        df_response = "Dialogflow says finding course stuff here"
    elif action == "ViewSchedule":
        # input the database function here with the user
        df_response = "Dialogflow says viewing schedule stuff here"
    else: 
        df_response = gpt3.gpt_response(message)
    return df_response

if __name__ == '__main__':
    app.run()