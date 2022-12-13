# create-joint-nlp-training
​
## Status
​
accepted
​
## Context

To ensure that Dialogflow and LUIS can be accurately compared we must make sure they are trained on the same (or at least very similar) data. We therefore could have a single individual input the training data and label the entities/intents for both systems, we have everyone add training as they see fit, or we could have one inidividual responsible for each system and keep a shared google doc where members input training data. The individuals in charge of each system can ensure their systems are up to date with the training data and keep the systems comparable. 
​
## Decision
​
Elliott will be responsible for the training and labeling of LUIS and Mayank will be responsible for the training and labeling of Dialogflow. The shared training data file will be shared on the Trello board for easy access and comments with @Elliott or @Mayank will be used to notify them if there is a change that needs their attention or a question about implementation/adjustment of existing data.
​
## Consequences
​
By having one individual in charge of each we get rid of the risk of two people double training with the same data. We also ensure that a single person doesn't have to do all of it since it is a fairly dull task and can be quite a lot of work (especially if responsible for both). Keeping a shared file for the data allows all members to contribute. 