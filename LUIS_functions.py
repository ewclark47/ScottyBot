"""
help with integration into bot at: https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/cognitivelanguage/azure-ai-language-conversations/samples/sample_analyze_conversation_app.py

This module incorporates the functionality of the Microsoft Azure LUIS project 
for ScottyBot. The LUIS class includes functions to iniate and instance of LUIS.
Use LUIS to predict Intent and included Entities from user input (message to ScottyBot).
The LUIS class also has a function to print the predicted results to the console as well
as functions that determine the responses for the user trying to add a course, drop a 
course, find a course or view their schedule. LUIS responses will hopefully be augmented
or replaced by GPT-3 generative response functionality.
"""

class LUIS: 
    def __init__(self, clu_endpoint, clu_key, project_name, deployment_name):
        self.clu_endpoint = clu_endpoint
        self.clu_key = clu_key
        self.project_name = project_name
        self.deployment_name = deployment_name

    def getLuisResults(self, query):
        # import libraries
        from azure.core.credentials import AzureKeyCredential
        from azure.ai.language.conversations import ConversationAnalysisClient

        # initialize client with the Azure project and then analyze the user input for predictions
        client = ConversationAnalysisClient(self.clu_endpoint, AzureKeyCredential(self.clu_key))
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
                        "projectName": self.project_name,
                        "deploymentName": self.deployment_name,
                        "verbose": True
                    }
                }
            )
            return result

    def displayResults(self,query):
        result = self.getLuisResults(query)
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

    def addCourse(self, courseNumber):
        bot_respone = "Ok I'll add course " + str(courseNumber) + " to your schedule!"
        return bot_respone
    
    def dropCourse(self, courseNumber):
        bot_respone = "Ok I'll drop course " + str(courseNumber) + " from your schedule!"
        return bot_respone
    
    def findCourse(self, courses):
        bot_response = "Are any of these the course you are looking for? \n" + courses
        return bot_response

    def viewSchedule(self, scheduleString):
        bot_response = "OK, let's look at your schedule!" + "\n" + scheduleString
        return bot_response

    # also put in a smalltalk function that will respond with GPT-3 stuff
    # so that if the user isn't asking anything related to scheduling it
    # is still interactive
    def aboutBot(self):
        return "Hello! I am ScottyBot! I can help you with scheduling here at CMU. I can add, drop and find courses as well as show you your schedule. Let me know what you want course you want to add/drop or what kind of course you are looking for. Or simply ask to view your schedule!"

    def smallTalk(self, utterance):
        return "GPT-3 Stuff will go in here"
