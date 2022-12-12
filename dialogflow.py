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
    print( params)
    print("retrieved necessary info, starting switch statement")
    # pull the user ID from the original slack payload
    user = ''
    slack_og = req.get('originalDetectIntentRequest')
    slack_payload = slack_og.get('payload')
    slack_data = slack_payload.get('data')
    slack_event = slack_data.get('event')
    user = slack_event['user'] 
    #print(user)
    fulfillmentText = switch(action, message, user, params)


    return {
        "fulfillmentText": fulfillmentText,
        "source": "webhookdata"
    }
    

def switch(action, message, user, params):
    print("started switch statment. responding based on action: " + action)
    df_response ="Sorry, I didn't quite get that"
    if action == "AddCourse":
        if len(params['course-number'])>0:
            courses_string = ""
            for course in params['course-number']:
                database_functions.addCourse(user, course)
                courses_string += str(course) + " "
            df_response = gpt3.gpt_response(message)
        elif params['topic'] != "":
            poss_course = database_functions.findCourse(params['topic'])
            df_response = "Are any of these the course you want? \n" + poss_course + "\n" + "If so, please try to add by course number"
        else:
            df_response = "I can't tell what course you would like to add. Please try again with a more specific course topic or course number."
    elif action == "DropCourse":
        if len(params['course-number'])>0:
            courses_string=''
            for course in params['course-number']:
                database_functions.dropCourse(user, course)
                courses_string += str(course) + " "
            df_response = gpt3.gpt_response(message)
        elif params['topic'] != "":
            poss_course = database_functions.findCourse(params['topic'])
            df_response = "Are any of these the course you want to drop? \n" + poss_course + "\n" + "If so, please try to drop by course number"
        else:
            df_response = "I can't tell what course you would like to drop. Please try again with a more specific course topic or course number."
    elif action == "FindCourse":
        if len(params['course-number'])>0:
            courses_string = ""
            for course in params['course-number']:
                courses_string += database_functions.findCourse(course) + "\n"
            df_response = gpt3.gpt_response(message) + "\n" + courses_string 
        elif params['topic'] != "":
            courses_string = database_functions.findCourse(params['topic'])
            df_response =  gpt3.gpt_response(message) + "\n" + courses_string
        else:
            df_response = "I can't tell what course you are looking for. Please try again with a more specific course topic or course number."        
    elif action == "ViewSchedule":
        schedule = database_functions.viewSchedule(user)
        df_response = "This is what your schedule looks like: " + "\n" + schedule
    else: 
        df_response = gpt3.gpt_response(message)
    return df_response

if __name__ == '__main__':
    app.run()