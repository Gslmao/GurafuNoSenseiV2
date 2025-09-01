"""
Initialization script for Gurafu No Sensei.

Creates the required database tables and folders for the application.
- Creates Log_Cred table in loginDB with columns: u_name, pw, email.
- Creates user_data database if not present.
- Creates files and App_Data directories if not present.
"""

import mysql.connector
import os
from dotenv import load_dotenv
import json

load_dotenv()

# Loads environment variables
db_host = os.getenv("MS_HOST")
db_port = int(os.getenv("MS_PORT"))
db_user = os.getenv("MS_USER")
db_password = os.getenv("MS_PASSWORD")
db_logindb = os.getenv("DB_loginDB")
db_userdata = os.getenv("DB_USERDATA")

files_path = os.getenv("FILES_PATH")
appdata_path = os.getenv("APPDATA_PATH")

config_data = {
    "FILES": files_path,
    "APPDATA": appdata_path
}

# Save config data to config.json
with open('config.json', 'w') as config_file:
    json.dump(config_data, config_file, indent=4)

os.makedirs(files_path, exist_ok=True)
os.makedirs(appdata_path, exist_ok=True)

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