# choose-database-type
​
## Status
​
accepted
​
## Context

In order to create functionality with the database that is interchangeable (and therefore reuseable) we need a shared understanding of what type of database we will be using. Primary considerations are a document store or a relational database. Although a document store would be ideal for long term scaling, we have far less experience with it. Also, a relational database is capable of accomplishing what we are trying to do with no major issues.
Using a document store, although probably a more realistic long-term decision with greater benefits, would require extra learning by each member of the group in addition to the other aspects of the project that already require extensive reasearch and experimentation. 
​
## Decision
​
We will utilize a relational database.
​
## Consequences

Implementing database functionality becomes much easier using a design that we are all familiar with. Since we are using a relational database we are inherently using a less flexible design than if we were to use a document store. Despite this consequence, we do not expect the structure of courses to change any time soon (i.e. there will still be a course name, course number, etc.) and see no threat of having to restructure our database.
