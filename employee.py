#!/usr/bin/env python3
import mysql.connector
import cgi

print('Content-type:text/html')
print('')
print('<html>')
print('<head>')
print('<meta http-equiv="content-type" content="text/html; charset=utf-8">')
print('<link rel="stylesheet" type="text/css" href="styles.css">')
print('<title>Employee Page</title>')
print('</head>')

form = cgi.FieldStorage()
user_id = form.getvalue('user_id')

db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='P@ssw0rd',
    database='python'
)
cursor = db.cursor()

sql = 'SELECT * FROM employees WHERE empNumber = %s'
cursor.execute(sql, (user_id,))
employee = cursor.fetchone()

cursor.close()
db.close()

if employee:
    empNumber, firstName, lastName, email, position = employee
    print(f'<h1>Welcome, {firstName} {lastName}</h1>')
    print(f'<p>Email: {email}</p>')
    print(f'<p>Title: {position}</p>')
    print(f'<a href="/change_password.py?user_id={user_id}">Change Password</a>')

print('</html>')
