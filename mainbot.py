from os import environ
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from LUIS_functions import LUIS

load_dotenv()
SLACK_BOT_TOKEN = environ['SLACK_BOT_TOKEN']
SLACK_APP_TOKEN = environ['SLACK_APP_TOKEN']
# get secrets
clu_endpoint = environ["AZURE_CONVERSATIONS_ENDPOINT"]
clu_key = environ["AZURE_CONVERSATIONS_KEY"]
project_name = environ["AZURE_CONVERSATIONS_PROJECT_NAME"]
deployment_name = environ["AZURE_CONVERSATIONS_DEPLOYMENT_NAME"]

app = App(token = SLACK_BOT_TOKEN)
luis = LUIS(clu_endpoint, clu_key, project_name, deployment_name)

def addCourse():
	return "Adding Course"
	
def dropCourse():
	return "Dropping Course"

def findCourse():
	return "Finding Course"

def switch(action, categories, values):
	if action == "AddCourse":
		# then go through entity categorys to see if there is a course number, if not request it
		res = luis.addCourse(12345)
	elif action == "DropCourse":
		# then go through entity categorys to see if there is a course number, if not request it
		res = luis.dropCourse(12345)
	elif action == "FindCourse":
		# go through entities and find a topic or something to pass on to LUIS
		res = luis.findCourse("Just something to test here")
	elif action == "ViewSchedule":
		res = luis.viewSchedule
	return res

@app.event("app_mention")
def mention_handler(body, say):
	event = body['event'] # pulls the part of the body dictionary that contains the user message
	text = event['text'] 
	message = text[15:] # this is just the user input message without the bot name
	# the above is the full uterance
	print(message)

	result = luis.getLuisResults(message)
	luis.displayResults(message)

	action = result["result"]["prediction"]["topIntent"]
	entity_cats = []
	entity_vals = []
	for entity in result["result"]["prediction"]["entities"]:
		entity_cats.append(entity["category"])
		entity_vals.append(entity["text"])
        
	bot_response = switch(action, entity_cats, entity_vals)
	say(bot_response)

	#say("So you want me to " + result["result"]["prediction"]["topIntent"] + "?")

if __name__ == "__main__":
	handler = SocketModeHandler(app, SLACK_APP_TOKEN)
	handler.start()

"""
The intro to the following tutorial was not working out:
https://www.analyticsvidhya.com/blog/2018/03/how-to-build-an-intelligent-chatbot-for-slack-using-dialogflow-api/
so the above code was found and modified from the following tutorial:
https://www.twilio.com/blog/how-to-build-a-slackbot-in-socket-mode-with-python#:~:text=To%20enable%20Socket%20Mode%2C%20navigate,your%20app%20is%20used%20in.
*note: the first tutorial had info on dialog flow that may be useful continuing on
"""