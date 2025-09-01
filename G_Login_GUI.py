from G_CreateAccount import Create_Page
from G_Login import Acc_Login
import tkinter as tk

class Functionality:
    """
    Functionality class provides custom button widgets and static methods for login and account creation actions.

    Classes:
        Button: A custom Tkinter Button widget for consistent styling.

    Methods:
        login(ele): Handles the login button action.
        create(ele): Handles the account creation button action.
    """
    class Button(tk.Button):
        def __init__(self, master=None, text='', command=None):
            super().__init__(master=master, text=text, command=command, bg="#333333", fg="#FFFFFF", font=("Arial", 14))

    @staticmethod
    def login(ele):
        ele.destroy()
        ele.quit()
        Acc_Login()

    @staticmethod
    def create(ele):
        ele.destroy()
        ele.quit()
        Create_Page()

class AppGUI:
    """
    AppGUI is the main graphical user interface class for the Gurafu No Sensei application.

    Attributes:
        window (tk.Tk)          : The main application window.
        main_frame (tk.Frame)   : The frame containing all widgets.
        m_head (tk.Label)       : The main header label.
        log_but (Functionality.Button): The login button.
        MakeAcc_but (Functionality.Button): The account creation button.

    Methods:
        make_place_widgets(): Places and configures all widgets in the main window.
        run()               : Starts the main event loop for the GUI.
    """
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Gurafu No Sensei")
        self.window.geometry("800x800")
        self.window.configure(bg="#333333")
        self.main_frame, self.m_head, self.log_but, self.MakeAcc_but = None, None, None, None

        self.make_place_widgets()

    def make_place_widgets(self):
        self.main_frame = tk.Frame(self.window, bg="#333333", pady=60)
        self.m_head = tk.Label(self.main_frame, text="WELCOME!!", bg="#333333", fg="#FFFFFF", font=("Arial", 25))

        self.log_but = Functionality.Button(self.main_frame, "Log into your account", lambda: Functionality.login(self.window))
        self.MakeAcc_but = Functionality.Button(self.main_frame, "Create a new Account", lambda: Functionality.create(self.window))

        self.m_head.grid(row=1, column=1, columnspan=4, pady=40)
        self.log_but.grid(row=2, column=1, columnspan=4, pady=10)
        self.MakeAcc_but.grid(row=3, column=1, columnspan=4, pady=10)
        self.main_frame.pack()

    def run(self):
        self.window.mainloop()

if __name__ == '__main__':
    MainGUI = AppGUI()
    MainGUI.run()
