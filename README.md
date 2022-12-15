# ScottyBot LUIS

## Getting Started

First make sure that a recent version of python is installed on your computer.
Once python is installed, enter the main project directory and open a terminal (bash terminal for Mac, git bash for windows).
Create a virtual environment:
```Shell
$ pip install virtualenv
$ python -m virtualenv venv
```

> Note: if python -m virtualenv venv does not work, try python3 -m virtualenv venv

next activate the virtual environment 
for Windows CMD Terminal:
```Shell
C:\> venv\Scripts\activate
```
for Mac:
```Shell
$ source venv/bin/activate
```
Now that the virtual environment is activated (you should see somthing along the lines of (venv) above or preceding your command input line. Now we will install the required packages for this project.
```Shell
(venv) $ pip install -r requirements.txt
```

> Note: if you plan on pushing this to github, ensure that your .gitignore file includes venv

## Setting up Environment Variables 

Next we want to ensure our environment variables are set up so that our project runs smoothly. To do this, create a .env file and create a variable OPENAI_API_KEY with the provided GPT3 api secret key (or your own if that is preferred) as well as a variable DB_PASSWORD with the provided password to access our Azure MySQL database. You will also need to input the Azure Conversation key as well as the Slack Bot and Slack App tokens, but keep the variables set that are already present in the .env-sample. 
For a Windows set up, you will make a call in your cmd terminal.
```Shell
set DB_Password=<password_here>
set OPENAI_API_KEY=<GPT3_API_SECRET_KEY_HERE>
set SLACK_APP_TOKEN=<XAPP_TOKEN_HERE>
set SLACK_BOT_TOKEN=<XOXB_TOKEN_HERE>
set AZURE_CONVERSATIONS_KEY=<AZURE_CONVO_KEY>
```

> Note: If you prefer a bash terminal on windows then use export ENV_VAR_NAME=ENV_VAR_VALUE

> Note: If you prefer to use your own database, please use the provided Generate ScottyBot Database script to populate a relational database named scottybot. If you choose to use your own database (this can be a local database) then you will need to change the host, user and password in the database_functions.py module as well as update or delete the ssl_ca and port sections of the connection  

Once you have your .env file, in your terminal run the command 
for Mac:
```Shell
$ source .env 
```

> Note: if you plan on pushing this to github, ensure that your .gitignore file includes .env

## Running and Interacting with ScottyBot

Now that the virtual environment is set up, all we have to do is run the main program to be able to interact with ScottyBot! To do this, run the command:
```Shell
$ python mainbot.py
```
Now go to the scottybot-development-workspace channel and message @ScottyBot_Elliott to start interacting with our bot! If you don't want to schedule any classes (since the functionality is the same as the Dialogflow bot) don't forget that our bot uses GPT3 to generate original text in response to anything you ask that isn't trying to add, drop, find a course or view your schedule.

> Note: if the above command does not work try replacing python with python3

## Final Steps

Once you are done communicating with ScottyBot, make sure to stop the application with the red square or ctrl+c as well as stop the ngrok tunnel with ctrl+c in your terminal. Now that everything is stopped, type the command <strong>deactivate</strong> in the terminal that is open from the project directory to stop the virtual environment.

Please feel free to reach out if you have any questions or concerns. Thank you and we hope you enjoyed ScottyBot!