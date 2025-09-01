import tkinter.messagebox as msg
import mysql.connector
import tkinter as tk
import os
from dotenv import load_dotenv

load_dotenv()
host = os.getenv("MS_HOST")
port = os.getenv("MS_PORT")
username = os.getenv("MS_USER")
paswd = os.getenv("MS_PASSWORD")

def create_login():
    """
    Handles the account creation process and closes the window after completion.

    No parameters.
    """
    fetch_data_newacc()
    CA_Win.quit()

def fetch_data_newacc():
    """
    Fetches new account data from the GUI, validates it, and creates a new user profile in the database.

    No parameters.
    """
    global UID, PW, chck

    UID = uname_get.get().strip()
    PW = pass_get.get().strip()
    chck = re_get.get().strip()

    db_L = os.getenv("DB_loginDB")

    if UID != "" and PW != "" and chck != "":
        if PW == chck:
            try:
                ipw_db = mysql.connector.connect(
                    host = host, username = username, password = paswd, database = db_L) 
                cursor = ipw_db.cursor()

                cursor.execute("select * from Log_Cred")
                exists = cursor.fetchall()
                for i in exists:
                    if UID == i[0]:
                        msg.showwarning('Caution', 'Account already exists')
                        CA_Win.destroy()
                        CA_Win.quit()
                        break
                else:

                    try:
                        profile_create()

                        cmd = "insert into Log_Cred(u_name, pw) values(%s, %s)"
                        val = (UID, PW)
                        cursor.execute(cmd, val)
                        ipw_db.commit()

                        cursor.close()
                        ipw_db.close()
                    except Exception as e:
                        print(e)

                    msg.showinfo("", "Account Created Successfully")
                    CA_Win.destroy()

            except mysql.connector.Error as err:
                msg.showerror("Error", f"Error: {err}")
        else:
            msg.showwarning("Input Error", "Passwords do not match")

    else:
        msg.showwarning("Error", "Any Entry cant be empty")

def Create_Page():
    """
    Renders the account creation GUI page.

    No parameters.
    """
    global uname_get, pass_get, re_get, CA_Win

    # Account Creation page Window
    CA_Win = tk.Tk()
    CA_Win.title("Create Your Account")
    CA_Win.geometry("500x500")
    CA_Win.configure(bg="#333333")

    CA_frame = tk.Frame(CA_Win, bg="#333333", pady=30)

    # Creating the Elements
    Page_Head = tk.Label(CA_frame, text="Create your account", bg="#333333", fg="#FFFFFF", font={"Arial", 20})

    username_lab = tk.Label(CA_frame, text="Username", bg="#333333", fg="#FFFFFF", font={"Arial", 14})
    pass_lab = tk.Label(CA_frame, text="Password", bg="#333333", fg="#FFFFFF", font={"Arial", 14})
    check_lab = tk.Label(CA_frame, text="Re-enter Password", bg="#333333", fg="#FFFFFF", font={"Arial", 14})
    uname_get = tk.Entry(CA_frame)
    pass_get = tk.Entry(CA_frame, show="*")
    re_get = tk.Entry(CA_frame, show="*")
    Create_int = tk.Button(CA_frame, text='Create!', bg="#333333", fg="#FFFFFF", command=create_login)

    # Placement
    Page_Head.grid(row=1, column=1, pady=35, columnspan=4)
    username_lab.grid(row=2, column=1, padx=5, pady=10)
    pass_lab.grid(row=3, column=1, padx=5, pady=10)
    check_lab.grid(row=4, column=1, padx=5, pady=10)
    uname_get.grid(row=2, column=2, columnspan=4)
    pass_get.grid(row=3, column=2, columnspan=4)
    re_get.grid(row=4, column=2, columnspan=4)
    Create_int.grid(row=5, column=2, columnspan=3)

    # Frame Placement
    CA_frame.pack()

    #Rendering the GUI
    CA_Win.mainloop()

def profile_create():
    """
    Creates a new user profile in the database and sets up the user's directory.

    No parameters.
    """
    db_U = os.getenv("DB_USERDATA")
    appdata_path = os.getenv("APPDATA_PATH")
    user_dir = os.path.join(appdata_path, f"u_{UID}")

    with mysql.connector.connect(host = host, username = username, password = paswd, database = db_U) as user_db:
        with user_db.cursor() as user_cursor:
            user_cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_U}")

    if os.path.exists(user_dir):
        os.rmdir(user_dir)
    os.mkdir(user_dir)

    with mysql.connector.connect(host=host, port=port, user=username, password=paswd, database=db_U) as user_db:
        with user_db.cursor() as cursor:
            tab_create = f"CREATE TABLE IF NOT EXISTS u_{UID} (SNum INT AUTO_INCREMENT, graphs VARCHAR(256));"
            cursor.execute(tab_create)
        user_db.commit()
