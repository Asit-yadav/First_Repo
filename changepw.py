#!/usr/bin/env python3
import cgi
import cgitb
import mysql.connector

cgitb.enable()

form = cgi.FieldStorage()
userName = form.getvalue('userName')
employee = form.getvalue('employee')

print("Content-Type: text/html\n")
print('<html><head><title>LAN Sharks - Change Password</title></head><body>')
print('<h1>Change Password</h1>')

# Retrieve user details
db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='P@ssw0rd',
    database='python'
)

cursor = db.cursor()

#Use the employee/customer flag to determine which table to query
if employee == "True":
   query = "SELECT e.firstName, e.lastName FROM users u JOIN employees e ON u.userName = %s AND u.userID = e.empNumber"
else:
    query = "SELECT c.firstName, c.lastName FROM users u JOIN customers c ON u.userName = %s AND u.userID = c.customerNumber"



cursor.execute(query, (userName,))
userRecord = cursor.fetchone()
db.close()

if userRecord:
    firstName, lastName = userRecord
    print('<h2>' + firstName + ' ' + lastName + '</h2>')
    print('<form action="changeOutcome.py" method="post">')
    print('<input type="hidden" name="userName" value="' + str(userName) + '">')
    print('<input type="hidden" name="employee" value="' + str(employee) + '">')
    print('<label for="currentPassword">Current Password:</label>')
    print('<input type="password" name="currentPassword" id="currentPassword" required><br>')
    print('<label for="newPassword">New Password:</label>')
    print('<input type="password" name="newPassword" id="newPassword" required><br>')
    print('<label for="confirmPassword">Confirm New Password:</label>')
    print('<input type="password" name="confirmPassword" id="confirmPassword" required><br>')
    print('<input type="submit" value="Change Password">')
    print('</form>')
else:
    print('<p>User not found. Please try again.</p>')

print('</body></html>')

'''#!/usr/bin/env python3
import cgi
import cgitb
import mysql.connector

cgitb.enable()

form = cgi.FieldStorage()
userName = form.getvalue('userName')
employee = form.getvalue('employee')

print("Content-Type: text/html\n")
print('<html><head><title>LAN Sharks - Change Password</title></head><body>')
print('<h1>Change Password</h1>')

# Retrieve user details
db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='P@ssw0rd',
    database='python'
)

cursor = db.cursor()

# Use the employee/customer flag to determine which table to query
if employee == "True":
    query = "SELECT e.firstName, e.lastName FROM users u JOIN employees e ON u.userName = %s AND u.userID = e.empNumber"
else:
    query = "SELECT c.firstName, c.lastName FROM users u JOIN customers c ON u.userName = %s AND u.userID = c.customerNumber"

cursor.execute(query, (userName,))
userRecord = cursor.fetchone()
db.close()

if userRecord:
    firstName, lastName = userRecord
    print('<h2>' + firstName + ' ' + lastName + '</h2>')
    print('<form action="changeOutcome.py" method="post">')
    print('<input type="hidden" name="userName" value="' + str(userName) + '">')
    print('<input type="hidden" name="employee" value="' + str(employee) + '">')
    print('<label for="currentPassword">Current Password:</label>')
    print('<input type="password" name="currentPassword" id="currentPassword" required><br>')
    print('<label for="newPassword">New Password:</label>')
    print('<input type="password" name="newPassword" id="newPassword" required><br>')
    print('<label for="confirmPassword">Confirm New Password:</label>')
    print('<input type="password" name="confirmPassword" id="confirmPassword" required><br>')
    print('<input type="submit" value="Change Password">')
    print('</form>')
else:
    print('<p>User not found. Please try again.</p>')

print('</body></html>')'''