#!/usr/bin/env python3

import mysql.connector
import os
import shutil
import glob
import datetime


# Find all .csv files in the logs folder
logFiles = glob.glob('/var/www/lansharks.com/logs/*.csv')

# Check if any log files are found
if len(logFiles) >= 1:
    # Connect to the MySQL database
    db = mysql.connector.connect(
        host='localhost', 
        user='root', 
        password='P@ssw0rd', 
        database='python'
    )
    cursor = db.cursor()


    # Initialize list to store new incidents
    newIncidents = []
 
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
        #newFilename = '/var/www/lansharks.com/logs/'+ moreParts[0] + str(datetime.date.today() + '.old')
        newFilename = '/var/www/lansharks.com/logs/' + moreParts[0] + str(datetime.date.today()) + '.old'

        os.rename(file, newFilename)
        print(file)
        print(newFilename) 

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

        # Rename the processed file to avoid reprocessing
        fileNameParts = nameParts[-1].split('.')
        newFileName = f"{fileNameParts[0]}_{datetime.date.today()}.old"
        print(type(file), file)
        shutil.move(file, f"/var/www/lansharks.com/logs/{newFileName}")


    # Close the database connection
    cursor.close()
    db.close()

'''#!/usr/bin/env python3

import mysql.connector
import os
import shutil
import glob
import datetime

# Find all .csv files in the logs folder
logFiles = glob.glob('/var/www/lansharks.com/logs/*.csv')

# Check if any log files are found
if len(logFiles) >= 1:
    # Connect to the MySQL database
    db = mysql.connector.connect(
        host='localhost', 
        user='root', 
        password='P@ssw0rd', 
        database='python'
    )
    cursor = db.cursor()

    # Initialize list to store new incidents
    newIncidents = []

    for logFile in logFiles:  # Renamed variable to avoid conflict
        # Read the content of the file
        with open(logFile, 'r') as current:  # Open the correct file
            tempList = current.readlines()
        newIncidents.append(tempList)

        # Extract customerNumber from the filename
        nameParts = logFile.split('/')
        fileParts = nameParts[-1].split('_')
        customerNumber = fileParts[0]  # Assuming customerNumber is before the underscore

        for incidentFile in newIncidents:  # Renamed to avoid conflict
            fileCounter = 0
            for incident in incidentFile:
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

        # Rename the processed file to avoid reprocessing
        fileNameParts = nameParts[-1].split('.')
        newFileName = f"{fileNameParts[0]}_{datetime.date.today()}.old"
        shutil.move(logFile, f"/var/www/lansharks.com/logs/{newFileName}")  # Move the original logFile


    # Close the database connection
    cursor.close()
    db.close() '''


