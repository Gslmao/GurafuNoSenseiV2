"""
Initialization script for Gurafu No Sensei.

Creates the required database tables and folders for the application.
- Creates Log_Cred table in loginDB with columns: u_name, pw, email.
- Creates user_data database if not present.
- Creates files and App_Data directories if not present.
"""
import mysql.connector
import json
import os

from config import db_host, db_port, db_user, db_password, db_logindb, db_userdata,  path_files, path_appdata

config_data = {
    "FILES": path_files,
    "APPDATA": path_appdata
}

with open('config.json', 'w') as config_file:
    json.dump(config_data, config_file, indent=4)

os.makedirs(path_files, exist_ok=True)
os.makedirs(path_appdata, exist_ok=True)

try:
    conn = mysql.connector.connect(
        host=db_host,
        port=db_port,
        user=db_user,
        password=db_password
    )
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_logindb}")
    cursor.execute(f"USE {db_logindb}")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Log_Cred (
            u_name VARCHAR(64) PRIMARY KEY,
            pw VARCHAR(128) NOT NULL,
            email VARCHAR(128)
        )
    """)
    print(f"Table Log_Cred created in database {db_logindb}.")
except Exception as e:
    print(f"Error creating Log_Cred table: {e}")
finally:
    cursor.close()
    conn.close()

try:
    conn = mysql.connector.connect(
        host=db_host,
        port=db_port,
        user=db_user,
        password=db_password
    )
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_userdata}")
    print(f"Database {db_userdata} ensured.")
except Exception as e:
    print(f"Error creating user_data database: {e}")
finally:
    cursor.close()
    conn.close()