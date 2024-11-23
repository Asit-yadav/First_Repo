#!/usr/bin/env python3
import cgi
import cgitb
import mysql.connector 

cgitb.enable()

form = cgi.FieldStorage()
userName = form.getvalue('userName')
employee = form.getvalue('employee')
currentPassword = form.getvalue('currentPassword')
newPassword = form.getvalue('newPassword')
confirmPassword = form.getvalue('confirmPassword')

print("Content-Type: text/html\n")
print('<html><head><title>LAN Sharks - Change Password</title></head><body>')

# Connect to MySQL database
db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='P@ssw0rd',
    database='python'
)

cursor = db.cursor()

# Check current password with a parameterized query (security improvement)
cursor.execute("SELECT password FROM users WHERE userName = %s", (userName,))
result = cursor.fetchone()

if result:
    storedPassword = result[0]
    if currentPassword != storedPassword:
        print('<h2>Something Went Wrong</h2>')
        print('<p>Current password is incorrect.</p>')
        print('<p><a href="changepw.py?userName=' + userName + '">Try Again</a></p>')
    elif newPassword != confirmPassword:
        print('<h2>Something Went Wrong</h2>')
        print('<p>New passwords do not match.</p>')
        print('<p><a href="changepw.py?userName=' + userName + '">Try Again</a></p>')
    else:
        # Update the password with a parameterized query (security improvement)
        cursor.execute("UPDATE users SET password = %s WHERE userName = %s", (newPassword, userName))
        db.commit()
         # Determine the correct table to pull the user's first and last name
        if employee == "True":
            sql2 = "SELECT firstName, lastName FROM employees WHERE empNumber = (SELECT userID FROM users WHERE userName = %s)"
        else:
            sql2 = "SELECT firstName, lastName FROM customers WHERE customerNumber = (SELECT userID FROM users WHERE userName = %s)"
        
        cursor.execute(sql2, (userName,))
        names = cursor.fetchone()

        print('<h2>Password Changed!</h2>')
        if names:
            firstName, lastName = names
            print('<p>' + firstName + ' ' + lastName + ', your password has been successfully changed.</p>')
        print('<p><a href="/login.py">Return to Login</a></p>')
else:
    print('<h2>Something Went Wrong</h2>')
    print('<p>User not found.</p>')

# Close the database connection
db.close()

print('</body></html>')
if result:
    storedPassword = result[0]
    if currentPassword != storedPassword:
        print('<h2>Something Went Wrong</h2>')
        print('<p>Current password is incorrect.</p>')
        print('<p><a href="changepw.py?userName=' + userName + '">Try Again</a></p>')
    elif newPassword != confirmPassword:
        print('<h2>Something Went Wrong</h2>')
        print('<p>New passwords do not match.</p>')
        print('<p><a href="changepw.py?userName=' + userName + '">Try Again</a></p>')
    else:
        # Update the password
        cursor.execute("UPDATE users SET password = %s WHERE userName = %s", (newPassword, userName))
        db.commit()
        print('<h2>Password Changed!</h2>')
        print('<p>Your password has been successfully changed.</p>')
        print('<p><a href="/login.py">Return to Login</a></p>')
else:
    print('<h2>Something Went Wrong</h2>')
    print('<p>User not found.</p>')

# Close the database connection
db.close()

print('</body></html>')