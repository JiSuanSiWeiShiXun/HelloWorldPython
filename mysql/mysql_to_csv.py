import csv
import mysql.connector

# Connect to the database
cnx = mysql.connector.connect(user='dump', password='dump@xsj.com',
                              host='10.11.10.200', port=3307,
                              database='dump_win32')
cursor = cnx.cursor()

# Execute the SELECT query
# dump_base
query = ("SELECT  GUID,DumpKey,DumpTime,UUID,NewUUID  FROM `dump_win32`.`dump_base` "
         "WHERE Project='JX3' AND VersionEx='pakv4_hdzhcn' AND DumpTime > '2023-10-29 00:00:00'")
# dump_session
# query = ("""SELECT  UploadTime,IP,UUID,NewUUID  FROM `dump_win32`.`dump_session` 
#         WHERE Project="JX3" AND VersionEx="pakv4_hdzhcn" AND UploadTime> "2023-10-29 00:00:00";""")
cursor.execute(query)

# Write the results to a CSV file
with open('base.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow([i[0] for i in cursor.description])  # write headers
    while True:
        rows = cursor.fetchmany(size=10000)
        if not rows:
            break
        writer.writerows(rows)

# Close the database connection
cursor.close()
cnx.close()
