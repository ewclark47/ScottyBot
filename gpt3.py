"""
author: Elliott Clark, Mayank Bansal

Module to use GPT to mantain natural flow in conversation.

This module requires that `openai` be installed within the Python
environment you are running this script in.

This module contains the following functions:

    * gpt_response - sets the parameters for sending request to gpt3 
    and getting the response
"""

import openai


class gpt3:
    def __init__(self, api_key):
        """
        Parameters
        ----------
        api_key : str
            API key for GPT3
        """

        self.api_key = api_key

    def gpt_response(self, input):
        """ Sets the parameters for sending request to gpt3 
        and gets the response

        Parameters
        ----------
        input : str
            String containing the input to be sent to GPT3

        Returns
        -------
        str
            response from GPT3
        """

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
