# design-database-schema
​
## Status
​
accepted

## Context

In order to write reuseable methods that interact with our relational database, we must decide on a schema that we will all implement when working with our code. 
​
​
## Decision
​
We decided on the schema that can be found under the Baseline Database Card on our ScottyBot Trello board. The schema is a database of three tables: course, users and schedules. The course table will hold all available course information, the users table will record the user from Slack and assign them an ID and the schedules table will store each users "registerd" classes through the UserID foreign key.
​
## Consequences
​
By creating a schema that we all agreed on and can individually implement ensures that none of us are writing methods that interact with the database that will break when integrated with a different aspect of the project.