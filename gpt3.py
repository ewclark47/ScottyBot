import openai

class gpt3:
    def __init__(self, api_key):
        self.api_key = api_key

    def gpt_response(self, input):
            response = openai.Completion.create(
                    engine="text-davinci-002",
                    prompt=input,
                    temperature=0.7,
                    max_tokens=1000,
                    top_p=1.0,
                    frequency_penalty=0.0,
                    presence_penalty=0.0
            )
            return response.choices[0].text