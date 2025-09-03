import os
from dotenv import load_dotenv
load_dotenv()

path_cwd = os.getenv("PATH_CWD")
path_files = os.getenv("PATH_FILES")
path_appdata = os.getenv("PATH_APPDATA")
path_appFiles = os.getenv("PATH_APP_FILES")
path_logo = os.getenv("PATH_LOGO")
path_qp = os.getenv("PATH_QP")
path_userCarryover = os.getenv("PATH_USER_CARRYOVER")
path_myFile = os.getenv("PATH_MY_FILE")
path_figFile = os.getenv("PATH_FIG_FILE")

db_host = os.getenv("MS_HOST")
db_port = int(os.getenv("MS_PORT"))
db_user = os.getenv("MS_USER")
db_password = os.getenv("MS_PASSWORD")
db_logindb = os.getenv("DB_loginDB")
db_userdata = os.getenv("DB_USERDATA")