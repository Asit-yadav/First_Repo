#!/usr/bin/env python3
import mysql.connector
import os
import csv
from datetime import datetime

# Directory containing the CSV files
log_dir = '/var/www/lansharks.com/logs/'

def process_csv_file(file_path):
    # Open and read the CSV file
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Extract relevant data
            packetDateTime = row['DateTime']
            srcIP = row['SrcIP']
            destIP = row['DestIP']
            protocol = row['Protocol']
            srcPort = row['SrcPort']
            destPort = row['DestPort']
            hostIP = row['HostIP']
            serverIP = row['ServerIP']
            srcMac = row['SrcMAC']
            destMac = row['DestMAC']
            info = row['Info']

            # Connect to the database
            db = mysql.connector.connect(
                host='localhost',
                user='root',
                password='P@ssw0rd',
                database='python'
            )
            cursor = db.cursor()

            # Insert into incidents table
            sql = '''
                INSERT INTO incidents (packetDateTime, srcIP, destIP, protocol, srcPort, destPort, hostIP, serverIP, srcMac, destMac, info)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            '''
            value = (packetDateTime, srcIP, destIP, protocol, srcPort, destPort, hostIP, serverIP, srcMac, destMac, info)
            cursor.execute(sql, value)
            db.commit()
            cursor.close()
            db.close()

    # Rename the file after processing
    new_file_name = f'{datetime.now().strftime("%Y%m%d_%H%M%S")}.old'
    os.rename(file_path, os.path.join(log_dir, new_file_name))

def main():
    for filename in os.listdir(log_dir):
        if filename.endswith('.csv'):
            process_csv_file(os.path.join(log_dir, filename))

if __name__ == '__main__':
    main()
