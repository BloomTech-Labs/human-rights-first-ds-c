#imports 
import psycopg2
import os
import csv
import datetime
from dotenv import load_dotenv
load_dotenv() #loads env
#Police of Force Table Create

POLICE_TABLE = """CREATE TABLE IF NOT EXISTS police_force (
    id SERIAL PRIMARY KEY NOT NULL,
    dates TIMESTAMP,
    added_on TIMESTAMP,
    links TEXT,
    case_id TEXT,
    city TEXT,
    state TEXT,
    lat FLOAT,
    long FLOAT,
    title TEXT,
    description TEXT,
    tags TEXT,
    verbalization INT,
    empty_hand_soft INT,
    empty_hand_hard INT,
    less_lethal_methods INT,
    lethal_force INT,
    uncategorized INT

);"""
#Connection to DB
DB_CONECTION = os.getenv('DBURLS')
pg_conn = psycopg2.connect(DB_CONECTION)
pg_curs = pg_conn.cursor()

#Execute command to create table
pg_curs.execute(POLICE_TABLE)
pg_conn.commit() # Commit changes. 

#Script to read rows from csv, upload to created table on postgres sql
with open ('Labs28_AllSources_wo_DuplicateLinks3.csv','r') as f:
    next(f)
    reader =csv.reader(f,delimiter='|')
    counter = 0
    for row in reader:
        current_dt = datetime.datetime.today()        
        row = [None if cell == '' else cell for cell in row]
        pg_curs.execute("""INSERT INTO police_force (dates,added_on, links, case_id, city, state,lat,long, title, description, tags,verbalization,empty_Hand_soft, empty_hand_hard, less_lethal_methods, lethal_force, uncategorized) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);""",(row[0],current_dt,str(row[1]),str(row[2]),str(row[3]),str(row[4]),row[5],row[6],str(row[7]),str(row[8]),row[9],row[10],row[11],row[12],row[13],row[14],row[15]))
        print("Inserted Row Number: ",counter)
        counter += 1

pg_conn.commit()
pg_curs.close()
pg_conn.close()
