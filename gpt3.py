import openai
import os

class gpt3:
    def __init__(self, api_key):
        self.api_key = api_key

    def gpt_response(self, message):
        openai.api_key = os.environ['OPENAI_API_KEY']
        response = openai.Completion.create(
                engine="text-davinci-002",
                prompt=message,
                temperature=.5,
                max_tokens=1000,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0
        )
        return response.choices[0].text
