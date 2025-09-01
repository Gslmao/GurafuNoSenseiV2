from G_Main_App_GUI import App
from dotenv import load_dotenv

import tkinter.messagebox as msg
import mysql.connector as msc
import tkinter
import os


load_dotenv()

global id1
state_var = "failed"

def login_func():
    try:
        id1, pw = fetch_data_login()
    except Exception as e:
        print(f"Error in login_func: {e}")

    if state_var == 'success':
        dir = os.getenv("FILES_PATH")
        with open(os.path.join(dir, 'user_carryover.txt'), 'w') as carry:
            carry.write(id1)
        MainApp = App(id1)
        MainApp.run()
    else:
        pass

def fetch_data_login():
    global state_var
    ID = id_get.get().strip()
    PW = pw_get.get().strip()

    host = os.getenv("MS_HOST")
    port = int(os.getenv("MS_PORT"))
    username = os.getenv("MS_USER")
    password = os.getenv("MS_PASSWORD")
    db_L = os.getenv("DB_loginDB")

    try:
        ipw_db = msc.connect(
            host=host,
            port=port,
            username=username,
            password=password,
            database=db_L
        )
        cursor = ipw_db.cursor()
        cursor.execute("select * from Log_Cred")
        creds = cursor.fetchall()
    except Exception as e:
        msg.showerror("Database Error", f"Could not connect to database: {e}")
        return 0, 0

    if ID != "" and PW != "":
        for i in creds:
            if ID == i[0]:
                if PW == i[1]:
                    msg.showinfo("", "Login Successful")
                    state_var = "success"
                    LoginWin.destroy()
                    LoginWin.quit()
                    cursor.close()
                    ipw_db.close()
                    return ID, PW
                else:
                    msg.showwarning("Error", "Wrong Password!, Exiting...")
                    LoginWin.destroy()
                    LoginWin.quit()
                    cursor.close()
                    ipw_db.close()
                    return 0, 0
        else:
            msg.showwarning("Error", "User ID doesn't Exist")
            LoginWin.destroy()
            LoginWin.quit()
            cursor.close()
            ipw_db.close()
    else:
        msg.showwarning("Error", "Any entry cant be Empty")

def Acc_Login():
    global id_get, pw_get, LoginWin
    # Login Page Window
    LoginWin = tkinter.Tk()
    LoginWin.title("Login form")
    LoginWin.geometry("500x500")
    LoginWin.configure(bg="#333333")

    # Frame with the elements
    LoginFrame = tkinter.Frame(LoginWin, pady=50, bg="#333333")

    # Page Elements
    Header = tkinter.Label(LoginFrame, text="Account Login", bg="#333333", fg="#FFFFFF", font={"Arial", 20})
    id_lab = tkinter.Label(LoginFrame, text="Username", bg="#333333", fg="#FFFFFF", font={"Arial", 14})
    pw_lab = tkinter.Label(LoginFrame, text="Password", bg="#333333", fg="#FFFFFF", font={"Arial", 14})
    id_get = tkinter.Entry(LoginFrame)
    pw_get = tkinter.Entry(LoginFrame, show="*")
    login_int = tkinter.Button(LoginFrame, text="Login", command=login_func)

    # Elements placements
    Header.grid(row=0, column=0, columnspan=3, pady=15)
    id_lab.grid(row=1, column=0, pady=10)
    pw_lab.grid(row=2, column=0, pady=10)
    id_get.grid(row=1, column=1, columnspan=3, pady=10)
    pw_get.grid(row=2, column=1, columnspan=3, pady=10)
    login_int.grid(row=3, column=1, columnspan=3, pady=5)

    # Packing the frame
    LoginFrame.pack()

    # Rendering the GUI
    LoginWin.mainloop()