#!/usr/bin/env python3

import cgi
import cgitb
import mysql.connector # type: ignore

cgitb.enable()

print("Content-type: text/html\n")

# Database connection
db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='P@ssw0rd',
    database='python'
)

cursor = db.cursor()

# Get the logged-in user's information
form = cgi.FieldStorage()
userName = form.getvalue('userName')

# SQL query to fetch the customer's details
sql2 = "SELECT * FROM customers WHERE customerNumber = (SELECT customerNumber FROM users WHERE userName = %s)"
cursor.execute(sql2, (userName,))
userName = cursor.fetchall()

# HTML form for updating contact information
print('<html>')
print('<head>')
print('<title>LAN Sharks - Update Info</title>')
print('</head>')
print('<body>')
print('<h1>Update Contact Information</h1>')
print('<form action="infoOutcome.py" method="post">')
print('<input type="hidden" id="userName" name="userName" value="{}">'.format(userName))

# Displaying the customer's name
print('<h2 class="heading" style="text-align: left;">{} {}</h2>'.format(userName[0][1], userName[0][2]))

# Form fields with current values from the database
print('<label for="company">Company Name: </label>')
print('<input size="67" type="text" id="company" name="companyName" value="{}" /><p/>'.format(userName[0][3]))
print('<label for="address">Address: </label>')
print('<input size="75" type="text" id="address" name="address" value="{}"/><p/>'.format(userName[0][4]))
print('<label for="city">City: </label>&nbsp;&nbsp;&nbsp; ')
print('<input size="19" type="text" id="city" name="city" value="{}" />&nbsp;&nbsp;&nbsp; '.format(userName[0][5]))
print('<label for="state">State: </label>')
print('<input size="14" type="text" id="state" name="state" value="{}" />&nbsp;&nbsp;&nbsp; '.format(userName[0][6]))
print('<label for="zip">ZIP code: </label>')
print('<input required="required" size="10" maxlength="5" type="text" id="zip" name="zipCode" value="{}" /><p/>'.format(userName[0][7]))
print('<label for="email">E-mail: </label>')
print('<input required="required" size="38" type="email" id="email" name="email" value="{}" />&nbsp;&nbsp;&nbsp; '.format(userName[0][8]))
print('<label for="phone">Phone: </label>')
print('<input size="20" type="tel" id="phone" name="phone" value="{}" /><p/>'.format(userName[0][9]))

# Submit button
print('<input class="button btnlogin" type="submit" value="Update Contact Information" style="margin-left: 250px" /></p>')
print('</form>')
print('</body>')
print('</html>')

# Close the database connection
cursor.close()
db.close()
