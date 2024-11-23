#!/usr/bin/env python3
import mysql.connector
import cgi
import cgitb
cgitb.enable()


print('Content-type:text/html')
print('')

print('<html>')
print('<head>')
print('<meta http-equiv="content-type" content="text/html; charset=utf-8">')
print('<link rel="stylesheet" type="text/css" href="styles.css">')
print('<title>Success</title>')
print('</head>')

# Directly adding the required HTML instead of reading from external files
print('<body>')
print('<div class="wholepage">')
print('<div class="nav">')
print('<img src="images/banner1.jpg" usemap="#image-map">')
print('<map name="image-map">')
print('<area target="" alt="Home" title="Home" href="index.htm" coords="5,155,115,200" shape="rect">')
print('<area target="" alt="Services" title="Services" href="services.htm" coords="135,155,280,200" shape="rect">')
print('<area target="" alt="Threats" title="Threats" href="threats.htm" coords="300,155,445,200" shape="rect">')
print('<area target="" alt="Contact" title="Contact" href="contact.htm" coords="470,155,625,200" shape="rect">')
print('<area target="" alt="About" title="About" href="about.htm" coords="655,155,765,200" shape="rect">')
print('<area target="" alt="Login" title="Login" href="login.htm" coords="975,155,1095,200" shape="rect">')
print('</map>')
print('</div>')

form = cgi.FieldStorage()
firstName = form.getvalue('FirstName')
lastName = form.getvalue('LastName')
companyName = form.getvalue('CompanyName')
address = form.getvalue('Street')
city = form.getvalue('City')
state = form.getvalue('State')
zipCode = form.getvalue('ZIP')
email = form.getvalue('Email')
phone = form.getvalue('Phone')
comments = form.getvalue('Comments')

# Debugging output
print(f"FirstName: {firstName}, LastName: {lastName}, CompanyName: {companyName}")

db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='P@ssw0rd',
    database='python'
)
cursor = db.cursor()

try:
    # Insert new customer
    sql = "INSERT INTO customers (firstName, lastName, companyName, address, city, state, zipCode, email, phone, comments) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    value = (firstName, lastName, companyName, address, city, state, zipCode, email, phone, comments)
    cursor.execute(sql, value)
    db.commit()

    # Check the number of affected rows
    print(f"Rows affected by insertion: {cursor.rowcount}")

    print('<h2 class="heading">Application Successful!</h2>')
    print(f'<p class="description">Your contact information has been successfully added. You can click <a href="login.htm" style="color: #FFD700;">here</a> to login.</p>')

except mysql.connector.Error as err:
    print(f'<h2 class="heading">Database error: {err}</h2>')

finally:
    cursor.close()
    db.close()

# Closing HTML tags that were previously in pageEnd.htm
print('</div>')  # close wholepage
print('</body>')
print('</html>')
