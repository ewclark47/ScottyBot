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
    #print(username)
    #print(type(username))
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
        mydb.commit()
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
        mydb.commit()
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
                cursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='schedules'")
                scheduleColumns = cursor.fetchall()
                columnList =[]
                for column in scheduleColumns:
                    columnList.append(column[0])
                print("All existing columns retrieved")
                print(columnList)
                updateCol = "Course " + str(courseCount)
                print(updateCol)
                print(updateCol in columnList)
                if updateCol in columnList:
                    queryString = "UPDATE schedules SET `Course "+str(courseCount)+"`=\'"+str(courseInfo)+"\' WHERE UserID="+str(userID)
                    cursor.execute(queryString)
                    mydb.commit()
                    queryString = "UPDATE schedules SET CourseCount="+str(courseCount)+" WHERE UserID="+str(userID)
                    cursor.execute(queryString)
                    mydb.commit() # manual commit added because database was not receiving autocommit from update query
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
        queryString = "SELECT CourseCount FROM schedules WHERE UserID="+str(userID)
        cursor.execute(queryString)
        courseCount = cursor.fetchone()
        courseCount = courseCount[0]
        # iterate through the schedule and figure out how to get the column
        # name for whichever course entry contain the specified course number
        # (our course description) 
        # then update that column to null for the user "dropping" that course
        cursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='schedules'")
        scheduleColumns = cursor.fetchall()
        columnList =[]
        for column in scheduleColumns:
            columnList.append(column[0])
        print("All existing columns retrieved")
        cursor.execute("SELECT * FROM schedules WHERE UserID="+str(userID))
        scheduleRow=cursor.fetchone()
        scheduleValues = []
        for value in scheduleRow:
            scheduleValues.append(value)
        for i in range(len(scheduleValues)):
            if str(courseNumber) in str(scheduleValues[i]):
                columnName = columnList[i]
        cursor.execute("UPDATE schedules SET `"+str(columnName)+"`=\' \' WHERE UserID="+str(userID))
        mydb.commit()
        # use the original coursecount to check if columns need slid left
        courses=[]
        for i in range(1,courseCount+1):
            cursor.execute("SELECT `Course "+str(i)+"` FROM schedules WHERE UserID="+str(userID))
            info = cursor.fetchone()
            courses.append(info[0])
        print(courses)
        courses.remove(' ')
        for i in range(len(courses)):
            cursor.execute("UPDATE schedules SET `Course "+str(i+1)+"`=\'"+str(courses[i])+"\' WHERE UserID="+str(userID))
            mydb.commit()
        cursor.execute("UPDATE schedules SET `Course "+str(courseCount)+"`=\' \'")
        mydb.commit()
        cursor.execute("UPDATE schedules SET CourseCount="+str(courseCount-1)+" WHERE UserID="+str(userID))
        mydb.commit()

        
    except mysql.connector.Error as e:
        print(e)

def viewSchedule(username):
    try:
        cursor = mydb.cursor()
        if checkUser(username):
            queryString = "SELECT UserID FROM users WHERE UserName=\'"+str(username)+"\'"
            userID = cursor.execute(queryString)
            userID = cursor.fetchone()
            userID=userID[0]
            print("User's ID is: " + str(userID))
            if checkUserSchedule(userID):
                queryString = "SELECT * FROM schedules WHERE UserID="+str(userID)
                cursor.execute(queryString)
                row = cursor.fetchone()
                #print(row[3:])
                scheduleString=""
                print("start loop through schedule")
                if len(row[3:])>0:
                    for r in row[3:]:
                        if r == "" or r == " ":
                            scheduleString+=""
                        else:
                            scheduleString += "\n" + str(r)
                    if scheduleString=="":
                        scheduleString="You haven't scheduled anything yet!"
                else:
                    scheduleString = "You haven't scheduled anything yet!"
        return scheduleString
        
    except mysql.connector.Error as e:
        print(e)

def findCourse(description):
    try:
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM course")
        courses = cursor.fetchall()
        possibleCourse = ""
        for course in courses:
            courseString = ""
            useableString= ""
            for c in course[1:]:
                useableString += str(c) + " "
                courseString += str(c).lower() + " "
            #print(courseString)
            if str(description).lower() in courseString:
                possibleCourse += useableString + "\n"
        print("Possible course(s): ")
        print(possibleCourse)
        return possibleCourse
    
    except mysql.connector.Error as e:
        print(e)


# below was used for testing and will not be functionality in the final product
def method_tests():
    try:
        cursor = mydb.cursor()
        # test using partial course number -> shows all
        """ print("Finding a course using partial course number: ")
        findCourse(95) """
        # test using partial course name "Machine Learning" -> shows ecomm and MLPS
        """ print("Finding a course using a topic: ")
        findCourse("Machine Learning") """
        # test find all courses -> works
        """ print("Finding all courses: ")
        findCourse(" ") """

        # test viewing an empty schedule -> works
        #print(viewSchedule("nonexistuser"))
        # test adding a course when others have more courses -> works
        #addCourse("testuserrando", 95729)
        # test dropping a course -> works
        #dropCourse("testuserrando", 95729)

        # testing to make sure the new drop method shifts -> works
        """ addCourse("randotestuser",95702)
        addCourse("randotestuser",95729)
        addCourse("randotestuser",95828)
        dropCourse("randotestuser",95702)
        print(viewSchedule("randotestuser"))
        addCourse("randotest",95702)
        addCourse("randotest",95729)
        addCourse("randotest",95828)
        dropCourse("randotest",95729)
        print(viewSchedule("randotest"))
        addCourse("randouser",95702)
        addCourse("randouser",95729)
        addCourse("randouser",95828)
        dropCourse("randouser",95828)
        print(viewSchedule("randouser")) """
        
    except mysql.connector.Error as e:
        print(e)

    finally:
        cursor.close()
        mydb.close()

if __name__ == '__main__':
    method_tests()
