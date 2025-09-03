import os
from dotenv import load_dotenv
load_dotenv()

def add_path(path):
    path_cwd = os.getenv("PATH_CWD")
    return os.join(path_cwd, path)

path_files       = add_path(os.getenv("PATH_FILES"))
path_appdata     = add_path(os.getenv("PATH_APPDATA"))
path_appFiles    = add_path(os.getenv("PATH_APP_FILES"))
path_logo        = add_path(os.getenv("PATH_LOGO"))
path_qp          = add_path(os.getenv("PATH_QP"))
path_userCarryover = add_path(os.getenv("PATH_USER_CARRYOVER"))
path_myFile      = add_path(os.getenv("PATH_MY_FILE"))
path_figFile     = add_path(os.getenv("PATH_FIG_FILE"))

db_host     = add_path(os.getenv("MS_HOST"))
db_port     = add_path(int(os.getenv("MS_PORT")))
db_user     = add_path(os.getenv("MS_USER"))
db_password = add_path(os.getenv("MS_PASSWORD"))
db_logindb  = add_path(os.getenv("DB_loginDB"))
db_userdata = add_path(os.getenv("DB_USERDATA"))