#!/usr/bin/env python3

import cgi
import cgitb
import mysql.connector 

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

# Get the updated information from the form
form = cgi.FieldStorage()
userName = form.getvalue('userName')
companyName = form.getvalue('companyName')
address = form.getvalue('address')
city = form.getvalue('city')
state = form.getvalue('state')
zipCode = form.getvalue('zipCode')
email = form.getvalue('email')
phone = form.getvalue('phone')
# SQL query to update the customer's contact information
sql_update = """
    UPDATE customers 
    SET companyName = %s, address = %s, city = %s, state = %s, zipCode = %s, email = %s, phone = %s
    WHERE customerNumber = (SELECT customerNumber FROM users WHERE userName = %s)
"""
cursor.execute(sql_update, (companyName, address, city, state, zipCode, email, phone, userName))
db.commit()

# HTML page to show update outcome
print('<html>')
print('<head>')
print('<title>LAN Sharks - Update Info</title>')
print('</head>')
print('<body>')
print('<h1>Information Updated</h1>')
print('<p>Your contact information has been successfully updated.</p>')
print('<a href="login.py">Return to Home Page</a>')
print('</body>')
print('</html>')

# Close the database connection
cursor.close()
db.close()
