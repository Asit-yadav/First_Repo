#!/usr/bin/env python3
import mysql.connector
import cgi

print('Content-type:text/html')
print('')
print('<html>')
print('<head>')
print('<meta http-equiv="content-type" content="text/html; charset=utf-8">')
print('<link rel="stylesheet" type="text/css" href="styles.css">')
print('<title>Customer Page</title>')
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

sql = 'SELECT * FROM customers WHERE customerNumber = %s'
cursor.execute(sql, (user_id,))
customer = cursor.fetchone()

cursor.close()
db.close()

if customer:
    (customerNumber, firstName, lastName, companyName, address, city, state, zipCode, email, phone, comments) = customer
    print(f'<h1>Welcome, {firstName} {lastName}</h1>')
    print(f'<p>Company: {companyName}</p>')
    print(f'<p>Address: {address}, {city}, {state}, {zipCode}</p>')
    print(f'<p>Email: {email}</p>')
    print(f'<p>Phone: {phone}</p>')
    print(f'<a href="/change_password.py?user_id={user_id}">Change Password</a>')
    print(f'<a href="/update_contact.py?user_id={user_id}">Update Contact Information</a>')

    # Display attack information
    db = mysql.connector.connect(
        host='localhost',
        user='root',
        password='P@ssw0rd',
        database='python'
    )
    cursor = db.cursor()

    # SYN Flag Attack Detection
    sql = '''
        SELECT destPort, COUNT(*) as attack_count, packetDateTime
        FROM incidents
        WHERE info LIKE '%[SYN]%' AND srcIP = destIP
        GROUP BY destPort, packetDateTime
    '''
    cursor.execute(sql)
    syn_attacks = cursor.fetchall()

    # ARP Poisoning Attack Detection
    sql = '''
        SELECT srcMac, COUNT(DISTINCT info) as ip_count, packetDateTime
        FROM incidents
        WHERE protocol = 'ARP'
        GROUP BY srcMac, packetDateTime
        HAVING ip_count > 1
    '''
    cursor.execute(sql)
    arp_attacks = cursor.fetchall()

    cursor.close()
    db.close()

    # Display SYN Flag Attacks
    print('<h2>SYN Flag Attacks:</h2>')
    for attack in syn_attacks:
        destPort, attack_count, packetDateTime = attack
        print(f'<p>Port {destPort} was attacked {attack_count} times on {packetDateTime}</p>')

    # Display ARP Poisoning Attacks
    print('<h2>ARP Poisoning Attacks:</h2>')
    for attack in arp_attacks:
        srcMac, ip_count, packetDateTime = attack
        print(f'<p>MAC Address {srcMac} was used for {ip_count} different IP addresses on {packetDateTime}</p>')

print('</html>')
