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
        print(addedUser[0][0])
        print("added user: " + str(addedUser))
        return True

# Check to see if the user that mentioned ScottyBot has a schedule
# If so, return True. If not, add a schedule for the user to the database and then 
# return True
def checkUserSchedule(userID):
    print(userID)
    queryString = "SELECT * FROM schedules WHERE UserID="+str(userID)
    cursor.execute(queryString)
    scheduleDoesExist = cursor.fetchall()
    if len(scheduleDoesExist)>0:
        print("First part of Schedule Check, it exists")
        return True
    else:
        # add in a schedule for this user with default values
        print("Went on to checkUserSchedule second part")
        queryString = "INSERT INTO schedules(UserID) VALUES ("+str(userID)+")"
        cursor.execute(queryString)
        print("Added row to schedules with this users userID")
        return True

def addCourse(username, courseNumber):
    print("Start of addCourse database function")
    try:
        queryString = "SELECT * FROM course WHERE CourseNumber=" + str(courseNumber)
        cursor.execute(queryString)
        courseInfo = cursor.fetchone()
        courseInfo = courseInfo[1:]
        new_str = ""
        for r in courseInfo:
            new_str += str(r)+", "
        courseInfo = new_str
        print("Got the course info")
        #print("UserName check function: " + str(checkUser(username)))
        if checkUser(username):
            print("Validated or added the user")
            queryString = "SELECT UserID FROM users WHERE UserName=\'"+str(username)+"\'"
            cursor.execute(queryString)
            userID = cursor.fetchone()
            userID = userID[0]
            print("Got the users ID")
            # get how many courses this user has (IF THEY HAVE THEM) and then add in the request course as 'course#' based on that number
            if checkUserSchedule(userID):
                print("Validated or added schedule for this user")
                queryString = "SELECT CourseCount FROM schedules WHERE UserID="+str(userID)
                cursor.execute(queryString)
                courseCount = cursor.fetchone()
                print("Got the Course Count " + str(courseCount[0]))
                courseCount = courseCount[0]+1
                ## **EITHER MAKE A CHECK TO SEE IF COLUMN EXIST OR BASELINE X CLASSES FOR EVERYONE AND JUST INSERT INFO
                # testing below -- ask one of the others to try and add a course
                cursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='schedules'")
                scheduleColumns = cursor.fetchall()
                columnList =[]
                for column in scheduleColumns:
                    columnList.append(column[0])
                updateCol = "Column " + str(courseCount)
                if updateCol in columnList:
                    queryString = "UPDATE schedules SET `"+updateCol+"`=\'"+str(courseInfo)+"\' WHERE UserID="+str(userID)
                    cursor.execute(queryString)
                    mydb.commit()
                # end testing
                else:
                    queryString = "ALTER TABLE schedules ADD `Course "+str(courseCount)+"` VARCHAR(500)"
                    cursor.execute(queryString)
                    queryString = "UPDATE schedules SET CourseCount="+str(courseCount)+" WHERE UserID="+str(userID)
                    cursor.execute(queryString)
                    mydb.commit() # manual commit added because database was not receiving autocommit from update query
                    print("This users course count after adding a course: " + str(courseCount))
                    queryString = "UPDATE schedules SET `Course "+str(courseCount)+"`=\'"+str(courseInfo)+"\' WHERE UserID="+str(userID)
                    cursor.execute(queryString)
                    mydb.commit() # manual commit added because database was not receiving autocommit from update query
                    print("added: " + str(courseInfo) + "to the users schedule")
        else:
            print("Issue with the username")

    except mysql.connector.Error as e:
        print(e)

def dropCourse(username, courseNumber):
    try:
        cursor = mydb.cursor()
        queryString = "SELECT UserID FROM users WHERE username=\'"+str(username)+"\'"
        cursor.execute(queryString)
        userID = cursor.fetchone()
        userID=userID[0]
        # iterate through the schedule and figure out how to get the column
        # name for whichever course entry contain the specified course number
        # (our course description) 
        # then update that column to null for the user "dropping" that course
        cursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='schedules'")
        scheduleColumns = cursor.fetchall()
        columnList =[]
        for column in scheduleColumns:
            columnList.append(column[0])
        cursor.execute("SELECT * FROM schedules WHERE UserID="+str(userID))
        scheduleRow=cursor.fetchone()
        scheduleValues = []
        for value in scheduleRow:
            scheduleValues.append(value)
        for i in range(len(scheduleValues)):
            if str(courseNumber) in str(scheduleValues[i]):
                columnName = columnList[i]
        cursor.execute("UPDATE schedules SET `"+str(columnName)+"`=\' \'")
        mydb.commit()
        
    except mysql.connector.Error as e:
        print(e)

def viewSchedule(username):
    try:
        cursor = mydb.cursor()
        queryString = "SELECT UserID FROM users WHERE UserName=\'"+str(username)+"\'"
        userID = cursor.execute(queryString)
        userID = cursor.fetchone()
        userID=userID[0]
        print("User's ID is: " + str(userID))
        queryString = "SELECT * FROM schedules WHERE UserID="+str(userID)
        cursor.execute(queryString)
        row = cursor.fetchone()
        print(row[3:])

        scheduleString=""
        for r in row[3:]:
            scheduleString += str(r)+"\n "
        return scheduleString
        
    except mysql.connector.Error as e:
        print(e)


# below was used for testing and will not be functionality in the final product
def query_with_fetchall():
    try:
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM course")
        rows = cursor.fetchall()

        print("Total Rows(s):", cursor.rowcount)
        for row in rows:
            print(row)
            new_str = ""
            for r in row[1:]:
                new_str += str(r)+", "
            print(new_str)

        """ cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        print("Total Users: ", cursor.rowcount)
        for row in rows:
            print(row) """

        # testing to figure out how to make updates go through in the database
        """ cursor.execute("UPDATE users SET UserName='testing testing' WHERE UserID=2")
        mydb.commit()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        print("Total Users: ", cursor.rowcount)
        for row in rows:
            print(row) """

        # testing to get a course column check to make sure we aren't trying to add a column that exists
        cursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='schedules'")
        scheduleColumns = cursor.fetchall()
        print("Schedules table columns output: ")
        columnList =[]
        for column in scheduleColumns:
            columnList.append(column[0])
        print(columnList)
        print('Course 1' in columnList)
        print('Course 4' in columnList)
        cursor.execute("SELECT * FROM schedules WHERE UserID="+str(24))
        scheduleRow=cursor.fetchone()
        scheduleValues = []
        for value in scheduleRow:
            scheduleValues.append(value)
        for i in range(len(scheduleValues)):
            if str(95702) in str(scheduleValues[i]):
                print("Column for this course: " + columnList[i])
                columnName = columnList[i]
        cursor.execute("UPDATE schedules SET `"+str(columnName)+"`= \' \'")
        mydb.commit()
        ## the above drops the course but need to make sure courses get shifted
        # so that there aren't random gaps
        # Get the number of courses and then use number of courses to drop and shift
        # info rather than using the whole column name
        
    except mysql.connector.Error as e:
        print(e)

    finally:
        cursor.close()
        mydb.close()

if __name__ == '__main__':
    query_with_fetchall()