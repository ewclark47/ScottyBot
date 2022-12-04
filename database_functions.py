import mysql.connector

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "",
    database = "ScottyBot"
)

def addCourse(username, courseNumber):
    try:
        cursor = mydb.cursor()
        queryString = "SELECT * FROM course WHERE CourseNumber=" + str(courseNumber)
        cursor.execute(queryString)
        courseInfo = cursor.fetchone()
        queryString = "SELECT UserID FROM users WHERE username="+username
        userID = cursor.execute(queryString)
        # get how many courses this user has and then add in the request course as 'course#' based on that number

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
        queryString = "SELECT UserID FROM users WHERE username="+username
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
        queryString = "SELECT UserID FROM users WHERE username="+username
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
        
    except mysql.connector.Error as e:
        print(e)

    finally:
        cursor.close()
        mydb.close()

if __name__ == '__main__':
    query_with_fetchall()