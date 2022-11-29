from os import environ
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

load_dotenv()
SLACK_BOT_TOKEN = environ['SLACK_BOT_TOKEN']
SLACK_APP_TOKEN = environ['SLACK_APP_TOKEN']

app = App(token = SLACK_BOT_TOKEN)

@app.event("app_mention")
def mention_handler(body, say):
	say("Hello World!")

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