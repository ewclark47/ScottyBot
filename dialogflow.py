class DialogFlow:
    def __init__(self):
        import dialogflow
        from google.api_core.exceptions import InvalidArgument

        DIALOGFLOW_PROJECT_ID='INSERT ID HERE'
        DIALOGFLOW_LANGUAGE_CODE= 'en-US'
        GOOGLE_APPLICATION_CREDENTIALS = 'CREDENTIALS JSON HERE'
        SESSION_ID = 'current-user-id here'

        session_client = dialogflow.SessionsClient()
        session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)