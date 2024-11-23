#!user/bin/env/python3
import mysql.connector

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="P@ssw0rd",
    database="python"
)

cursor = db.cursor()

# Define the customer number (example: 1)
customer_number = 1

# SQL query to fetch relevant incident data
sql = f"SELECT packetDateTime, srcIP, destIP, info, destPort FROM incidents WHERE customerNumber = {customer_number}"
cursor.execute(sql)
packets = cursor.fetchall()

# List to hold potential SYN flood attack packets
badPackets = []

# Loop through packets and find SYN attacks
for packet in packets:
    if packet[1] == packet[2] and packet[3].find('[SYN]') != -1:
        badPackets.append(packet)

# Dictionary to hold date and port attack counts
datePorts = dict()

# Build the dictionary with the count of attacks by date and port
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

# Print the result (for testing purposes)
print(datePorts)

# Close the database connection
db.close()

