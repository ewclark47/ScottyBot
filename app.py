import dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import os
from dotenv import load_dotenv
import openai

dotenv.load_dotenv()
SLACK_BOT_TOKEN = os.environ['SLACK_BOT_TOKEN']
SLACK_APP_TOKEN = os.environ['SLACK_APP_TOKEN']

app = App(token = SLACK_BOT_TOKEN)


def gpt3(stext):
        openai.api_key = os.environ['OPENAI_API_KEY']
        response = openai.Completion.create(
                engine="text-davinci-002",
                prompt=stext,
                temperature=0.7,
                max_tokens=1000,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0
        )
        content = response.choices[0].text.split('.')
        return response.choices[0].text


@app.event("app_mention")
def mention_handler(body, say):
       event = body['event']  # pulls the part of the body dictionary that contains the user message
       text = event['text']
       message = text[15:]
       response = gpt3(message)
       say(response)


if __name__ == "__main__":
        handler = SocketModeHandler(app, SLACK_APP_TOKEN)
        handler.start()