
# sql libraries :: for safety reasons db credentials are stored in a separate file
# sql libraries :: for safety reasons db credentials are stored in a separate file

import configDB_hidden as cdbh
import psycopg2 as dbapi
from psycopg2 import sql

dbUser = cdbh.dbUser
dbPass = cdbh.dbPass
dbName = cdbh.dbName
dbHost = cdbh.dbHost

db = dbapi.connect(database=dbName, user=dbUser, password=dbPass)
