from os import environ
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from azure.core.credentials import AzureKeyCredential
from azure.ai.language.conversations import ConversationAnalysisClient
"""
help with integration into bot at: https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/cognitivelanguage/azure-ai-language-conversations/samples/sample_analyze_conversation_app.py
"""

load_dotenv()
SLACK_BOT_TOKEN = environ['SLACK_BOT_TOKEN']
SLACK_APP_TOKEN = environ['SLACK_APP_TOKEN']
clu_endpoint = environ['AZURE_CONVERSATIONS_ENDPOINT']
clu_key = environ['AZURE_CONVERSATIONS_KEY']
project_name = ['AZURE_CONVERSATIONS_PROJECT_NAME']
deployment_name = ['AZURE_CONVERSATIONS_DEPLOYMENT_NAME']

app = App(token = SLACK_BOT_TOKEN)

def getLuisResults(query):
    # import libraries
    import os
    from azure.core.credentials import AzureKeyCredential
    from azure.ai.language.conversations import ConversationAnalysisClient

    # get secrets
    clu_endpoint = os.environ["AZURE_CONVERSATIONS_ENDPOINT"]
    clu_key = os.environ["AZURE_CONVERSATIONS_KEY"]
    project_name = os.environ["AZURE_CONVERSATIONS_PROJECT_NAME"]
    deployment_name = os.environ["AZURE_CONVERSATIONS_DEPLOYMENT_NAME"]

    client = ConversationAnalysisClient(clu_endpoint, AzureKeyCredential(clu_key))
    with client:
        result = client.analyze_conversation(
            task={
                "kind": "Conversation",
                "analysisInput": {
                    "conversationItem": {
                        "participantId": "1",
                        "id": "1",
                        "modality": "text",
                        "language": "en",
                        "text": query
                    },
                    "isLoggingEnabled": False
                },
                "parameters": {
                    "projectName": project_name,
                    "deploymentName": deployment_name,
                    "verbose": True
                }
            }
        )
        return result

def displayResults(query):
    result = getLuisResults(query)
    # view result
    print("query: {}".format(result["result"]["query"]))
    print("project kind: {}\n".format(result["result"]["prediction"]["projectKind"]))

    print("top intent: {}".format(result["result"]["prediction"]["topIntent"]))
    print("category: {}".format(result["result"]["prediction"]["intents"][0]["category"]))
    print("confidence score: {}\n".format(result["result"]["prediction"]["intents"][0]["confidenceScore"]))

    print("entities:")
    for entity in result["result"]["prediction"]["entities"]:
        print("\ncategory: {}".format(entity["category"]))
        print("text: {}".format(entity["text"]))
        print("confidence score: {}".format(entity["confidenceScore"]))
        if "resolutions" in entity:
            print("resolutions")
            for resolution in entity["resolutions"]:
                print("kind: {}".format(resolution["resolutionKind"]))
                print("value: {}".format(resolution["value"]))
        if "extraInformation" in entity:
            print("extra info")
            for data in entity["extraInformation"]:
                print("kind: {}".format(data["extraInformationKind"]))
                if data["extraInformationKind"] == "ListKey":
                    print("key: {}".format(data["key"]))
                if data["extraInformationKind"] == "EntitySubtype":
                    print("value: {}".format(data["value"]))

@app.event("app_mention")
def mention_handler(body, say):
	event = body['event'] # pulls the part of the body dictionary that contains the user message
	text = event['text'] 
	message = text[15:] # this is just the user input message without the bot name
	# the above is the full uterance
	print(message)

	result = getLuisResults(message)
	displayResults(message)

	say("So you want me to " + result["result"]["prediction"]["topIntent"] + "?")
	
	


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