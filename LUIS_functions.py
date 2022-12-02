"""
help with integration into bot at: https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/cognitivelanguage/azure-ai-language-conversations/samples/sample_analyze_conversation_app.py
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

    def addCourse(courseNumber):
        # this will be the method call for adding a course
        bot_respone = "Ok I'll add course " + courseNumber + " to your schedule!"
        return bot_respone
    
    def dropCourse(courseNumber):
        #this will be the method call for dropping a course
        bot_respone = "Ok I'll drop course " + courseNumber + " from your schedule!"
        return bot_respone
    
    def findCourse(description):
        #this will be the method call for finding courses
        bot_response = "Are any of these the course you are looking for?"
        return bot_response

    def viewSchedule():
        #this will be the method call for displaying the schedule
        return "Ok, let's look at your schedule"
