from G_Login_GUI import AppGUI
from G_Main_App_GUI import App
from dotenv import load_dotenv

import os

load_dotenv()

direct = os.getenv("FILES_PATH")
user_carryover_path = os.path.join(direct, 'user_carryover.txt')

def get_logged_in_user():
    if os.path.exists(user_carryover_path):
        with open(user_carryover_path, 'r') as file:
            user = file.read().strip()
            if user:
                return user
    return None

def main():
    user = get_logged_in_user()
    if user:
        try:
            home_page = App(user)
            home_page.run()
        except Exception as e:
            print(f"Error launching main app: {e}")
            welcome = AppGUI()
            welcome.run()
    else:
        welcome = AppGUI()
        welcome.run()

if __name__ == "__main__":
    main()
