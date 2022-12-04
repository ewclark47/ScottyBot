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