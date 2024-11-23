#!/usr/bin/env python3
import mysql.connector # type: ignore
import cgi, cgitb
import os, glob
import datetime

def processLogs():
            logFiles = glob.glob('/var/www/lansharks.com/logs/*.csv')
            newIncidents = []

    # Check if any log files are found
            if len(logFiles) >= 1:
    
                for file in logFiles:
            # Read the content of the file
                    with open(file, 'r') as current:
                     tempList = current.readlines()
                     newIncidents.append(tempList)

            # Extract customerNumber from the filename
                nameParts = file.split('/')
                fileParts = nameParts[-1].split('_')
                customerNumber = fileParts[0]  # Assuming customerNumber is before the underscore
                moreParts = nameParts[-1].split('.')
                newFilename = '/var/www/lansharks.com/logs/'+moreParts[0]+str(datetime.date.today()+'.old')
                os.rename(file, newFilename)

                for file in newIncidents:
                 fileCounter = 0
                for incident in file:
                    # Skip the first line (header)
                        if fileCounter == 0:
                            fileCounter += 1
                            continue
                    
                    # Split the incident data into individual fields
                        items = incident.split(',')
                        itemCounter = 0
                        for item in items:
                        # Remove any surrounding double quotes
                            items[itemCounter] = item.strip('"')
                            itemCounter += 1

                    # Remove the newline character from the last field
                            items[-1] = items[-1].rstrip('\n')

                    # Append the customer number to the items list
                            items.append(customerNumber)

                    # Prepare the SQL statement to insert data into the incidents table
                            sql = "INSERT INTO incidents (packetDateTime, srcIP, destIP, protocol, srcPort, destPort, hostIP, serverIP, srcMac, destMac, info, customerNumber) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

                    # Skip items[0] and items[5], and map the remaining items to the incidents table
                            values = (items[1], items[2], items[3], items[4],items[6], items[7], items[8], items[9],items[10], items[11], items[12], int(items[13]))

                    # Execute the SQL insert query
                            cursor.execute(sql, values)

                    # Commit the transaction to save the data in the database
                            db.commit()
                            processLogs()
                            
                            
                            
def findSynFlood(customerNumber):
    sql = f"SELECT packetDateTime, srcIP, destIP, info, destPort FROM incidents WHERE customerNumber = {customerNumber}"
    cursor.execute(sql)
    packets = cursor.fetchall()

    badPackets = []
    for packet in packets:
        if packet[1] == packet[2] and '[SYN]' in packet[3]:
            badPackets.append(packet)

    datePorts = dict()
    for badPacket in badPackets:
        date = badPacket[0]
        port = badPacket[4]

        if date not in datePorts:
            datePorts[date] = {port: 1}
        else:
            if port not in datePorts[date]:
                datePorts[date][port] = 1
            else:
                datePorts[date][port] += 1

    return datePorts
    
db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='P@ssw0rd',
    database='python'
)

cursor = db.cursor()

print('Content-type:text/html')
print('')
print('')
print('')
print('<html>')
print('<head>')
print('<meta http-equiv="content-type" content="text/html; charset=utf-8">')
print('<link rel="stylesheet" type="text/css" href="styles.css">')
print('<title>LAN Sharks App</title>')
print('</head>')

with open('/var/www/lansharks.com/pageStart.htm', 'r') as start:
    content = start.readlines()

for i in content:
    print(i.rstrip('\n'))

form = cgi.FieldStorage()
userName = form.getvalue('UserName')
password = form.getvalue('Password')
employee = form.getvalue('employee')


# Prepared statement for authentication query (security improvement)
sql = "SELECT * FROM users WHERE userName = %s AND password = %s"
cursor.execute(sql, (str(userName).lower(), str(password)))
results = cursor.fetchall()

if len(results) == 1:
    userID = results[0][0]  # Assuming userID is the first column in the users table

    # Check if the user is an employee or customer
    if employee == 'Employee':
        sql = "SELECT * FROM employees WHERE empNumber = %s AND lastName = %s"
    else:
        sql = "SELECT * FROM customers WHERE customerNumber = %s AND lastName = %s"
    
    cursor.execute(sql, (str(userID), userName[1:]))  # Parameterized query (security improvement)
    userRecord = cursor.fetchall()
    print(userRecord)

    if len(userRecord) == 1:
        if employee == 'Employee':
            print('<form class="loginform" action="main.py" method="post">')
            print('<input type="hidden" id="userName" name="userName" value="' + str(userName) + '">')
            print('<input type="hidden" id="employee" name="employee" value="True">')
            print('<h2 class="heading" style="text-align: left;">' + userRecord[0][1] + ' ' + userRecord[0][2] + '</h2>')  # Assuming first name and last name are in index 1 and 2
            print('<p id="commonthreats" style="text-align: left;">' + userRecord[0][4] + '</p>')  # Assuming position is in index 4
            print('<h2 style="text-align: left;">Email: ' + userRecord[0][3] + '</h2>')  # Email index is 3
            print('<h2 style="text-align: left;">User Name: ' + userName + '</h2>')
            print('<a href="login.htm" style="background: none; border: none; color: #FFD700; text-decoration: underline; cursor: pointer; font-size: 250%;">Click here to go to main app</a>')
            # Add Change Password Link/Button
            print('<a href="changepw.py?userName=' + str(userName) + '&employee=True" style="color: #FFD700; text-decoration: underline;">Change Password</a>')
            print('</form>')
        else:
        
            # Fetch SYN flood attack details for the customer
            synAttacks = findSynFlood(userID)
            print('<form class="loginform" action="main.py" method="post">')
            print('<input type="hidden" id="userName" name="userName" value="' + str(userName) + '">')
            print('<input type="hidden" id="employee" name="employee" value="False">')
            print('<h2 class="heading" style="text-align: left;">' + userRecord[0][1] + ' ' + userRecord[0][2] + '</h2>')  # Assuming first name and last name are in index 1 and 2
            print('<p id="commonthreats" style="text-align: left;">' + userRecord[0][4] + '</p>')  # Assuming some common info
            print('<h2 style="text-align: left;">Email: ' + userRecord[0][3] + '</h2>')  # Email index is 3
            print('<h2 style="text-align: left;">User Name: ' + userName + '</h2>')
            
            
            print('<p>Here are the details of any SYN flood attacks detected for your account:</p>')
            if synAttacks:
                print('<table border="1">')
                print('<tr><th>Date</th><th>Port</th><th>Number of Attacks</th></tr>')

                for date, portCounts in synAttacks.items():
                    for port, count in portCounts.items():
                        print(f'<tr><td>{date}</td><td>{port}</td><td>{count}</td></tr>')

                print('</table>')
            else:
                print("<p>No SYN flood attacks were detected.</p>")

            #print('<input type="submit" style="background: none; border: none; color: #FFD700; text-decoration: underline; cursor: pointer; font-size: 250%;" value="Click here to go to main app">')
            print('<a href="login.htm" style="background: none; border: none; color: #FFD700; text-decoration: underline; cursor: pointer; font-size: 250%;">Click here to go to main app</a>')


        
            # Add Change Password Link/Button
            '''print('<p><a href="changepw.py?userName=' + str(userName) + '&employee=False" style="color: #FFD700; text-decoration: underline;">Change Password</a></p>')
            print('</form>')
            print('<p><a href="changinfo.py?userName=' + str(userName) + '&employee=False" style="color: #FFD700; text-decoration: underline;">Update Contact</a></p>')
            print('</form>')'''
             # Add Change Password and Update Contact Info Links/Buttons
            print('<p><a href="changepw.py?userName=' + str(userName) + '&employee=False" style="color: #FFD700; text-decoration: underline;">Change Password</a></p>')
            print('<p><a href="changeInfo.py?userName=' + str(userName) + '&employee=False" style="color: #FFD700; text-decoration: underline;">Update Contact</a></p>')
    else:
        print('<h2 class="heading">Something Went Wrong</h2>')
        print('<p class="description">Uh oh. Something went wrong. If you are an employee, make sure you checked the employee box on the login page. If you are not, please do not check the box.</p>')
        print('<p class="description">Click <a href="/login.htm" style="color: #FFD700;">here</a> to retry.</p>')
else:
    print('<h2 class="heading">Authentication Failed</h2>')
    print('<p class="description">Click <a href="/login.htm" style="color: #FFD700;">here</a> to retry.</p>')

with open('/var/www/lansharks.com/pageEnd.htm', 'r') as end:
    content = end.readlines()

for i in content:
    print(i.rstrip('\n'))

cursor.close()
db.close()














