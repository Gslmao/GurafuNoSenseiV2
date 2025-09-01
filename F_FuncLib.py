from mysql.connector import Error
from tkinter import simpledialog, messagebox
from dotenv import load_dotenv

import json
import matplotlib.pyplot as plt
import mysql.connector as msl
import pickle
import os

load_dotenv()

# Declare environment variables at the top
db_host = os.getenv("MS_HOST")
db_port = int(os.getenv("MS_PORT"))
db_user = os.getenv("MS_USER")
db_password = os.getenv("MS_PASSWORD")
db_userdata = os.getenv("DB_USERDATA")
db_logindb = os.getenv("DB_loginDB")

file_path = os.getenv('FILES_PATH')
appdata = os.getenv('APPDATA_PATH')

with open('config.json', 'r') as f:
    config = json.load(f)


def data_entry(filename: str):
    """
    Adds a new graph entry for the current user in the database.

    :param filename: The name of the graph file to be saved.
    """
    user_file_path = os.path.join(file_path, 'user_carryover.txt')
    with open(user_file_path, 'r') as file:
        user = file.read().strip()

    sensei = msl.connect(
        host=db_host,
        port=db_port,
        username=db_user,
        password=db_password,
        database=db_userdata
    )
    entries = sensei.cursor()

    entries.execute(f"SELECT * FROM u_{user}")
    serial = len(entries.fetchall())

    query = f"INSERT INTO u_{user} (SNum, graphs) VALUES (%s, %s)"
    values = (serial + 1, filename)
    entries.execute(query, values)
    sensei.commit()

    entries.close()
    sensei.close()

def derivative(x_val, y_val):
    """
    Calculates the numerical derivative of y with respect to x.

    :param x_val: List of x values.
    :param y_val: List of y values.
    :return: List of derivative values.
    """
    deriv = []

    for i in range(len(x_val) - 1):
        dx = x_val[i + 1] - x_val[i]
        dy = y_val[i + 1] - y_val[i]
        derivative = dy / dx
        deriv.append(derivative)
    
    deriv.append(deriv[-1])
    return deriv

def save_graph(chck, figure):
    """
    Saves the graph image and its object for the current user.

    :param chck: The base name for the saved files.
    :param figure: The matplotlib figure object to be saved.
    """
    user_file_path = os.path.join(file_path, 'user_carryover.txt')
    with open(user_file_path, 'r') as file:
        user = file.read().strip()

    dir = os.path.join(appdata, f"u_{user}")
    os.chdir(dir)

    pic_file = chck + '.png'
    graph_obj = chck + '.pkl'

    plt.savefig(pic_file)

    with open(graph_obj, 'wb') as file:
        pickle.dump(figure, file)
    try:
        data_entry(f'{chck}')
        messagebox.showinfo("Savestate", f"Graph saved as {pic_file}")

    except Exception as e:
        os.remove(os.path.join(dir, graph_obj))
        os.remove(os.path.join(dir, pic_file))
        messagebox.showerror('Error', e)

def export(user):
    """
    Exports all graph data for the user as a zip file.

    :param user: Username whose data is to be exported.
    """
    def create_zip(zip_name, foldr):
        import zipfile

        foldr_base = os.path.basename(foldr.rstrip('/\\'))
        with zipfile.ZipFile(zip_name, 'w') as zipf:
            for r_dir, dirs, files in os.walk(foldr):
                for f_name in files:
                    f_path = os.path.join(r_dir, f_name)
                    arc_rel = os.path.join(foldr_base, os.path.relpath(f_path, foldr))
                    zipf.write(f_path, arc_rel)

    import shutil

    db_conn = msl.connect(
        host=db_host,
        port=db_port,
        username=db_user,
        password=db_password,
        database=db_userdata
    )
    db_cursor = db_conn.cursor()

    outfile_path = os.path.join(appdata, f'u_{user}', f'{user}.csv')
    db_cursor.execute(
        f"""SELECT * FROM u_{user} INTO OUTFILE '{outfile_path}' 
            FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n';"""
    )

    dest_foldr = os.path.join(appdata, f'u_{user}')
    create_zip(f'{user}.zip', dest_foldr)

    csv_file = os.path.join(dest_foldr, f'{user}.csv')

    if os.path.exists(csv_file):
        os.remove(csv_file)

def clear(user):
    """
    Clears all graph data and files for the specified user.

    :param user: Username whose data is to be cleared.
    """
    def clear_directory(dirc):
        import shutil

        for file in os.listdir(dirc):
            file_path = os.path.join(dirc, file)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                pass

    db = msl.connect(
        host=db_host,
        port=db_port,
        username=db_user,
        password=db_password,
        database=db_userdata
    )
    cursor = db.cursor()

    cursor.execute(f'truncate table u_{user}')

    clear_directory(os.path.join(appdata, f'u_{user}'))

def import_util(user):
    """
    Imports graph data for the user from a zip file.

    :param user: Username whose data is to be imported.
    """
    import zipfile as z
    import pandas as pd
    import shutil

    zipfile_name = simpledialog.askstring('Input', 'Enter Name of the Zipfile.zip')

    folder = os.path.join(appdata, f"u_{user}")
    targ = os.path.join(appdata, zipfile_name)
    table = f'u_{user}'

    db = msl.connect(
        host=db_host,
        port=db_port,
        username=db_user,
        password=db_password,
        database=db_userdata
    )
    cursor = db.cursor()

    os.makedirs(folder, exist_ok=True)

    original_files = set(os.listdir(folder))
    try:
        temp_dir = os.path.join(folder, 'temp_extracted')
        os.makedirs(temp_dir, exist_ok=True)

        with z.ZipFile(targ, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        extracted_folders = [f for f in os.listdir(temp_dir) if os.path.isdir(os.path.join(temp_dir, f))]
        if len(extracted_folders) == 1:
            singular_folder = extracted_folders[0]
            singular_folder_path = os.path.join(temp_dir, singular_folder)

            for item in os.listdir(singular_folder_path):
                try:
                    shutil.move(os.path.join(singular_folder_path, item), folder)
                except:
                    pass

        shutil.rmtree(temp_dir)

        csv_files = [f for f in os.listdir(folder) if f.endswith('.csv')]
        if csv_files:
            csv_file = os.path.join(folder, csv_files[0])

            df = pd.read_csv(csv_file, header=None, index_col=False)

            for index, row in df.iterrows():
                s_num = row[0]
                graph_name = row[1]
                sql_query = f"INSERT INTO {table} (SNum, graphs) VALUES (%s, %s)"
                cursor.execute(sql_query, (s_num, graph_name))

            db.commit()
        else:
            messagebox.showerror("ValueError", "CSV File is Empty")

    except Exception as e:
        shutil.rmtree(temp_dir)
        messagebox.showerror("Error", e)
    finally:
        cursor.close()
        db.close()

def check_data_consistency():
    """
    Checks and ensures that every user in the database has a corresponding folder.

    No parameters.
    """
    try:
        mydb = msl.connect(
            host=db_host,
            port=db_port,
            username=db_user,
            password=db_password,
            database=db_logindb
        )
        if mydb.is_connected():
            cursor = mydb.cursor()

            cursor.execute("select * from Log_Cred")
            account = cursor.fetchall()
            accounts_set = {i[0] for i in account}

            folders_set = set(os.listdir(appdata))

            missing = accounts_set - folders_set

            for i in missing:
                new_folder_path = os.path.join(appdata, i)
                os.mkdir(new_folder_path)
    except Error as e:
        pass

    finally:
        if mydb.is_connected():
            cursor.close()
            mydb.close()
    db = msl.connect(host='localhost', username='root', password='DBroot1324*!', database='loginDB')

