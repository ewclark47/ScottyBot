"""
author: Elliott Clark
Module to handle all of the database queries that need to be made 
for ScottyBots functionality.
This module contains functions to add a course to a users schedule,
drop a course from a users schedule, search the available courses and
display them to the user and display a users individual schedule.
This module also validates user and schedule existence in serparate 
in order to add the user or schedule if needed prior to performing
any queries.
"""
import mysql.connector

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "",
    database = "ScottyBot"
)
cursor = mydb.cursor()

# Check to see if the user that mentioned ScottyBot is in the database
# If so, return True. If not, add the user to the database and then 
# return True
def checkUser(username):
    #cursor = mydb.cursor()
    print(username)
    print(type(username))
    queryString = "SELECT * FROM users WHERE UserName=\'"+str(username)+"\'"
    cursor.execute(queryString)
    validUser = cursor.fetchall()
    print(validUser)
    if len(validUser)>0:
        print("This is happening in checkUser first part")
        return True
    else:
        print("It went on to the checkUser second part")
        queryString = "INSERT INTO users(UserName) VALUES (\'"+str(username)+"\')"
        cursor.execute(queryString)
        queryString = "SELECT * FROM users WHERE UserName=\'"+str(username)+"\'"
        cursor.execute(queryString)
        addedUser = cursor.fetchall()
        print("Second part of checkUser ran")
        print("added user: " + str(addedUser))
        #cursor.close()
        return True

def checkUserSchedule(userID):
    queryString = "SELECT * FROM schedules WHERE UserID="+str(userID)
    cursor.execute(queryString)
    scheduleDoesExist = cursor.fetchall()
    if len(scheduleDoesExist)>0:
        print("First part of Schedule Check, it exists")
        return True
    else:
        # add in a schedule for this user with default values
        return True

def addCourse(username, courseNumber):
    print("Start of addCourse database function")
    try:
        #cursor = mydb.cursor()
        queryString = "SELECT * FROM course WHERE CourseNumber=" + str(courseNumber)
        cursor.execute(queryString)
        courseInfo = cursor.fetchone()
        print("Got the course info")
        #print("UserName check function: " + str(checkUser(username)))
        if checkUser(username):
            print("Validated or added the user")
            queryString = "SELECT UserID FROM users WHERE UserName=\'"+str(username)+"\'"
            cursor.execute(queryString)
            userID = cursor.fetchone()
            print("Got the users ID")
            # get how many courses this user has (IF THEY HAVE THEM) and then add in the request course as 'course#' based on that number
            # AS OF RIGHT NOW IT IS JUST TRYING TO GET COURSECOUNT EVEN THOUGH THERE ARE NO SCHEDULES
            # MAKE SURE TO CHECK IF THERE ARE SCHEDULES AND THEN DO THAT
            if checkUserSchedule(userID):
                queryString = "SELECT CourseCount FROM schedules WHERE UserID="+str(userID)
                cursor.execute(queryString)
                courseCount = cursor.fetchone()
                print("Got the Course Count")
                courseCount = int(courseCount)+1
                print(courseCount)
                # right here need to also update the row to reflect that this user has another course now
                print("Incremented course count")
                # add the new course and increment CourseCount
                queryString = "ALTER TABLE schedules ADD Course "+str(courseCount)+" VARCHAR(150)"
                cursor.execute(queryString)
                queryString = "INSERT INTO schedules (CourseCount, Course "+str(courseCount)+") VALUES ("+str(courseCount) + ", \'" +str(courseInfo)+"\') WHERE UserID="+str(userID)
                cursor.execute(queryString)
        else:
            print("Issue with the username")

    except mysql.connector.Error as e:
        print(e)

    finally:
        cursor.close()
        mydb.close()

def dropCourse(username, courseNumber):
    try:
        cursor = mydb.cursor()
        queryString = "SELECT * FROM course WHERE CourseNumber=" + str(courseNumber)
        cursor.execute(queryString)
        courseInfo = cursor.fetchone()
        queryString = "SELECT UserID FROM users WHERE username=\'"+str(username)+"\'"
        userID = cursor.execute(queryString)
        # get how many courses this user has and then add in the request course as 'course#' based on that number

    except mysql.connector.Error as e:
        print(e)

    finally:
        cursor.close()
        mydb.close()

def viewSchedule(username):
    try:
        cursor = mydb.cursor()
        queryString = "SELECT UserID FROM users WHERE username="+str(username)
        userID = cursor.execute(queryString)
        queryString = "SELECT * FROM schedule WHERE UserID="+str(userID)
        cursor.execute(queryString)
        rows = cursor.fetchall()

        scheduleString = ""
        for row in rows:
            scheduleString+= row + "\n"
        return scheduleString
        
    except mysql.connector.Error as e:
        print(e)

    finally:
        cursor.close()
        mydb.close()


# below was used for testing and will not be functionality in the final product
def query_with_fetchall():
    try:
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM course")
        rows = cursor.fetchall()

        print("Total Rows(s):", cursor.rowcount)
        for row in rows:
            print(row)

        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        print("Total Users: ", cursor.rowcount)
        for row in rows:
            print(row)
        
    except mysql.connector.Error as e:
        print(e)

    finally:
        cursor.close()
        mydb.close()

if __name__ == '__main__':
    query_with_fetchall()