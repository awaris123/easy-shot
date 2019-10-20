'''import sqlite3
from flask import g

DATABASE = '/path/to/database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()'''

#Read Flu_Shot_Locations_-_2014_-_Present.csv from file from current direcory
import csv
import datetime
import pandas
import numpy as np
import sqlite3

fd = open('Flu_Shot_Locations_-_2014_-_Present.csv', 'r')
reader = csv.reader(fd)
fs_location = []
c = 0
for row in reader:
    if c > 0:
        date = row[15].split("/")
        typed_date = datetime.date(int(date[2]), int(date[0]), int(date[1]))
        #row[15] = arrow.typed_date.format('YYYY-MM-DD')
        row[15] = date[2]+"-"+date[0]+"-"+date[1]
        fs_location.append(row)
    #print(row)
    c += 1
fd.close()

#print(fs_location[0][2:4])
#print(fs_location[1][14:16])


#Define SQL Table
createtbl = """
CREATE TABLE Facility
(
    FacilityID      DECIMAL(3,0),
    Latitude        DOUBLE PRECISION,
    Longtitude      DOUBLE PRECISION,
    Street1         VARCHAR(100),
    PostCode        DECIMAL(6,0),
    FacilityName    VARCHAR(50),
    PhoneNum        DECIMAL(10,0),
    BeginDate       TEXT,
    EndDate         TEXT
);
"""

conn = sqlite3.connect('local.db') # open the connection
cursor = conn.cursor()
cursor.execute(createtbl)   # create the table
conn.commit()   # finalize inserted data

for x in range(len(fs_location)):
    if x > 0:
        #DATE in SQLITE date("YYYY-MM-DD")
        #Selecting facilities where flu shot contract is currently active
        cursor.execute("""INSERT OR IGNORE INTO Facility VALUES(?,?,?,?,?,?,?,?,date(?))""", [fs_location[x][1],fs_location[x][2],fs_location[x][3],fs_location[x][4],fs_location[x][8],fs_location[x][10],fs_location[x][12],fs_location[x][14],fs_location[x][15]])
conn.commit()

#Selecting facilities where flu shot contract is currently active
cursor.execute("select Latitude,Longtitude,FacilityID,Street1,PostCode from Facility where EndDate >= date('now')")
active_facilities = cursor.fetchall()

#Test coordinate will be replaced by current user location coordinate
test_coordinate = [41.878982, -87.625581]

shortest_d = 180 #farthest distance is 180 degrees
for facility_cordinate in active_facilities:
    distance = ((facility_cordinate[0] - test_coordinate[0])**2 + (facility_cordinate[1] - test_coordinate[1])**2)**(1/2)
    if distance <= shortest_d:
        #Save shortest distance location info
        shortest_d = distance
        closest_index = facility_cordinate[2]
        Street1 = facility_cordinate[3]
        PostCode = facility_cordinate[4]
    
    #distance = np.array(facility_cordinate).sub(np.array(test_coordinate)).pow(2).sum(1).pow(0.5)
    #print(distance)
print("shortest distance is: " + str(shortest_d))
print("closes facility index: " + str(closest_index))
#Query the closet location information
cursor.execute("""select DISTINCT FacilityName,Street1,FacilityID,PostCode from Facility where FacilityID = ? and Street1 = ? and PostCode = ? and EndDate >= date('now')""", [str(closest_index),Street1,str(PostCode)])
facility_name = cursor.fetchall()
print(facility_name)

#close SQLite connection
conn.close()

