from config import db_host, db_user, db_password, db_logindb, db_userdata, path_appdata, path_logo, path_userCarryover, path_myFile, path_figFile
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk, FigureCanvasTkAgg
from F_FuncLib import save_graph, export, clear, import_util
from tkinter import ttk, font, simpledialog, messagebox
from PIL import Image

import mysql.connector as msl
import customtkinter as ctk
import tkinter as tk
import subprocess
import pickle
import time
import os
import sys

theme = "#191919"
but_theme = "#191919"
canvas = "#3d3d3d"
b_col, b_w = "#A2678A", 0
font = ('arial', 18)
win_w, win_h = 1200, 720

sbx, sby = 5, 5
sbw, sbh = 110, win_h - 10
tfx, tfy = sbx + 10 + sbw, 5
tfw, tfh = win_w - (15 + sbw + sbx), 90
mfx, mfy = sbx + sbx + sbw + 5, tfh + 15
mfw, mfh = win_w - (15 + sbw + sbx), win_h - (20 + tfh)

def log_out(instance):
    messagebox.showwarning("Confirm", "You sure you wanna log out?")
    instance.home_page.quit()
    instance.home_page.destroy()
    for attr in instance.__dict__:
        setattr(instance, attr, None)
    del instance

    with open(path_userCarryover, 'w') as file:
        pass

class AppElements:
    class SideBar:
        def __init__(self, master, instance, page_switch):
            self.side_bar = None
            self.logout = None
            self.account = None
            self.graph = None
            self.home = None
            self.exit = None
            self.switch_command = page_switch
            self.AppInst = instance
            self.master = master

            self.sidebar()

        def sidebar(self):
            self.side_bar = ctk.CTkFrame(master=self.master, width=sbw, height=sbh, corner_radius=10,
                                         fg_color=theme, border_color=b_col, border_width=b_w)

            logo_img = ctk.CTkImage(light_image=Image.open(path_logo), dark_image=Image.open(path_logo), size=(90, 90))
            logo = ctk.CTkLabel(master=self.side_bar, text='', corner_radius=0, image=logo_img)
            logo.place(x=10, y=15)

            self.home = Buttons(master=self.side_bar, text='Home', command=lambda: self.switch_command('Home'),
                                font=('Segoe UI', 21))
            self.graph = Buttons(master=self.side_bar, text='Plotter', command=lambda: self.switch_command('Plotter'),
                                 font=('Segoe UI', 21))
            self.account = Buttons(master=self.side_bar, text='Account',
                                   command=lambda: self.switch_command('Accounts'), font=('Segoe UI', 21))
            self.logout = Buttons(master=self.side_bar, text='Log Out', command=lambda: log_out(self.AppInst),
                                  font=('Segoe UI', 21))
            self.exit = Buttons(master=self.side_bar, text='Exit', command=lambda: self.AppInst.exit(),
                                font=('Segoe UI', 21))

            self.home.place(x=10, y=135)
            self.graph.place(x=10, y=135+65)
            self.account.place(x=10, y=135+2*65)
            self.logout.place(x=10, y=135+3*65)
            self.exit.place(x=10, y=sbh - 60)

            self.side_bar.place(x=sbx, y=sby)

    class TopBar:
        def __init__(self, master, pagename):
            self.home_title = pagename
            self.home_header = None
            self.top_frame = None
            self.master = master

            self.top_bar()

        def top_bar(self):
            self.top_frame = ctk.CTkFrame(master=self.master, width=tfw, height=tfh, fg_color=theme,
                                          corner_radius=10, border_color=b_col, border_width=b_w)
            self.home_header = ctk.CTkLabel(master=self.top_frame, text=self.home_title, width=20, height=50,
                                            corner_radius=5, font=('Inter', 38.5), text_color="white")

            self.top_frame.place(x=tfx, y=tfy)
            self.home_header.place(relx=0.5, rely=0.5, anchor='center')

    class HomeFrame:
        def __init__(self, master, uname, switch, p_master):
            self.intro = """Welcome to Gurafu no Sensei!

This app is designed to help you explore mathematical concepts through visualizations in a simple and intuitive way. You can differentiate and integrate equations, allowing you to see their transformations and understand them better. Whether you're learning new concepts or reviewing familiar ones, this tool makes it easier to grasp complex ideas with clear, interactive graphs.

To get started, create an account and jump into your own graph creations. Save your work, so you can come back to it whenever you need. If you're ever unsure of how to proceed or need assistance, we're here to help guide you.

Enjoy the process, and let’s make math an enjoyable journey!"""

            self.switch_func = switch
            self.p_master = p_master
            self.master = master
            self.uname = uname
            self.home_header = None
            self.main_frame = None
            self.qp_label = None
            self.qp = None

            self.main()

        def main(self):
            text_fnt = ("Courier New", 19.5)
            self.main_frame = ctk.CTkFrame(master=self.master, width=mfw, height=mfh, fg_color=theme, corner_radius=10, border_color=b_col, border_width=b_w)

            intro_lbl = ctk.CTkTextbox(master=self.main_frame, wrap='word', width=580, height=480, font=text_fnt, fg_color=theme)
            saved = ctk.CTkLabel(master=self.main_frame, width=300, height=20, font=text_fnt, fg_color=theme, text='The Graphs You\'ve Saved')
            open_graph = ctk.CTkLabel(master=self.main_frame, width=300, text='Double Click to Open!!', height=20, font=text_fnt, fg_color=theme)

            intro_lbl.insert('1.0', self.intro)

            intro_lbl.place(x=40, y=35)
            saved.place(x=715, y=30)
            open_graph.place(x=715, y=450 + 10 + 65)

            self.fetch_tables()
            self.main_frame.place(x=mfx, y=tfy + tfw + 10)

        def fetch_tables(self):
            style = ttk.Style()
            style.theme_use("default")
            style.configure("Treeview", background="#3d3d3d", foreground="white")
            style.configure("Treeview.Heading", background="#3d3d3d", foreground="white")

            mydb = msl.connect(host=db_host, port=db_port, username=db_user, password=db_password, database=db_userdata)
            cursor = mydb.cursor()

            cursor.execute(f"SELECT * from u_{self.uname}")
            r = cursor.fetchall()

            columns = ['Serial', 'Graph']

            def double(event):
                my_db = msl.connect(host=db_host, port=db_port, username=db_user, password=db_password, database=db_logindb)
                cur = my_db.cursor()

                item = t.selection()[0]
                data = t.item(item, "values")
                cur.execute(f'SELECT graphs from u_{self.uname} where SNum={data[0]}')
                name = cur.fetchone()[0]

                self.switch_func('Plotter')

                with open(os.path.join(path_appdata, f"u_{self.uname}", f"{name}.pkl"), 'rb') as file:
                    fig = pickle.load(file)

                self.p_master.draw_graph(fig)

            t = ttk.Treeview(master=self.main_frame, selectmode='browse', columns=columns, show='headings')

            t.column('Serial', width=150, anchor='c')
            t.column('Graph', width=150, anchor='c')
            t.heading('Serial', text='S.No')
            t.heading('Graph', text='Graphs')

            for index, row in enumerate(r):
                t.insert(parent='', index='end', iid=index, values=row)

            t.bind("<Double-1>", double)

            t.place(x=715, y=70, height=450)

    class PlotFrame:
        def __init__(self, master, inst):
            self.ul = None
            self.ll, self.ll = None, None
            self.entry = None
            self.canvas = None
            self.slots = None
            self.master = master
            self.main_frame = None
            self.inst = inst
            self.save_var = tk.StringVar()

            self.main_frame = ctk.CTkFrame(master=self.master, width=mfw, height=win_h - 10, fg_color=theme,
                                           corner_radius=10, border_color=b_col, border_width=b_w)

            self.three = ctk.CTkSegmentedButton(master=self.main_frame, values=['Plot Graphs', 'Differentiation', 'Integration'],
                                                command=self.toggle, width=300, height=50)
            self.three.place(x=65, y=115)
            self.main_frame.place(x=5, y=mfy + 5)

            self.create_main()

        def create_main(self):
            top = ctk.CTkLabel(master=self.main_frame, text='Plot Graphs', font=('arial', 30), text_color="black",
                               width=370, height=75, fg_color="#D9D9D9", corner_radius=10)

            self.slots = [ctk.CTkEntry(master=self.main_frame, font=('arial', 30), text_color="black",
                                       width=370, height=60, fg_color="#D9D9D9", corner_radius=10) for _ in range(0, 6)]

            chckbox = ctk.CTkCheckBox(master=self.main_frame, text="Check to Save Graph",
                                      onvalue="y", offvalue="n", variable=self.save_var)
            but = ctk.CTkButton(master=self.main_frame, text='Plot', command=lambda: self.plot_graph(), width=145)

            for num, slot in enumerate(self.slots):
                slot.place(x=15, y=115 + 75 * (num + 1))

            but.place(x=15, y=115 + 75 * 7)
            chckbox.place(x=15 + 145 + 20, y=115 + 75 * 7)
            top.place(x=15, y=10)

        def integrate(self):
            i_top = ctk.CTkLabel(master=self.main_frame, text='Integrate', font=('arial', 30), text_color="black", width=370, height=75, fg_color="#D9D9D9", corner_radius=10)

            self.entry = ctk.CTkEntry(master=self.main_frame, font=('arial', 30), text_color="black", width=370, height=60, fg_color="#D9D9D9", corner_radius=10)
            self.ul = ctk.CTkEntry(master=self.main_frame, font=('arial', 30), text_color="black", width=180, height=60, fg_color="#D9D9D9", corner_radius=10)
            self.ll = ctk.CTkEntry(master=self.main_frame, font=('arial', 30), text_color="black", width=180, height=60, fg_color="#D9D9D9", corner_radius=10)

            u_label = ctk.CTkLabel(master=self.main_frame, font=('arial', 25), fg_color=theme, text='Upper Limit', text_color="white", width=110, height=60, corner_radius=10)
            l_label = ctk.CTkLabel(master=self.main_frame, font=('arial', 25), fg_color=theme, text='Lower Limit', text_color="white", width=110, height=60, corner_radius=10)
            text = ctk.CTkLabel(master=self.main_frame, font=('arial', 22), fg_color=theme, text='Leave Blank for Indefinite Integration', text_color="#959595", width=110, height=60, corner_radius=10)

            but = ctk.CTkButton(master=self.main_frame, text='Plot', command=lambda: self.plot_graph('i'), width=145)
            chckbox = ctk.CTkCheckBox(master=self.main_frame, text="Check to Save Graph", onvalue="y", offvalue="n", variable=self.save_var)

            inc = 0
            self.ul.place(x=15, y=190 + 75 + inc)
            self.ll.place(x=15, y=190 + 75 * 2 + inc)
            u_label.place(x=225, y=190 + 75 + inc)
            l_label.place(x=225, y=190 + 75 * 2 + inc)
            text.place(x=15, y=115 + 75 * 4 + inc)

            chckbox.place(x=15 + 145 + 20, y=115 + 75 * 7)

            i_top.place(x=15, y=10)

            but.place(x=15, y=115 + 75 * 7)

            self.entry.place(x=15, y=190)

        def differentiate(self):
            d_top = ctk.CTkLabel(master=self.main_frame, text='Differentiate', font=('arial', 30), text_color="black", width=370, height=75, fg_color="#D9D9D9", corner_radius=10)
            self.entry = ctk.CTkEntry(master=self.main_frame, font=('arial', 30), text_color="black", width=370, height=60, fg_color="#D9D9D9", corner_radius=10)
            but = ctk.CTkButton(master=self.main_frame, text='Plot', command=lambda: self.plot_graph('d'), width=145)
            chckbox = ctk.CTkCheckBox(master=self.main_frame, text="Check to Save Graph", onvalue="y", offvalue="n", variable=self.save_var)

            chckbox.place(x=15 + 145 + 20, y=115 + 75 * 7)
            d_top.place(x=15, y=10)
            but.place(x=15, y=115 + 75 * 7)
            self.entry.place(x=15, y=190)

        def plot_graph(self, flag='normal'):
            self.three.place_forget()

            save_state = self.save_var.get()

            if flag == 'normal':
                eqns = [i.get() for i in self.slots]
                det = {'eqns': eqns, 'calc': 'n', 'limits': []}
            else:
                eqn = self.entry.get()
                eqns = [eqn]
                det = {'eqns': eqns}

                if flag == 'i':
                    lim_u, lim_l = self.ul.get(), self.ll.get()
                    det['limits'] = [float(lim_u), float(lim_l)] if lim_l != '' and lim_u != '' else [0, 0]
                    det['calc'] = 'i'
                elif flag == 'd':
                    det['limits'] = []
                    det['calc'] = 'd'

            det['savestate'] = save_state if save_state != "" else 'n'

            try:
                with open(path_myFile, "wb") as file:
                    pickle.dump(det, file)
            except Exception as e:
                print(f"Error writing to file: {e}")

            AppElements.PlotFrame.processor()

            try:
                with open(path_figFile, 'rb') as file:
                    fig = pickle.load(file)

                if save_state == 'y':
                    name = simpledialog.askstring('Input', 'Enter the name for the saved graph file (without extension): ')
                    save_graph(str(name), fig)
                    self.inst.home.fetch_tables()

                self.draw_graph(fig)
            except Exception as e:
                #messagebox.showerror("Processing Error", e)
                print(f"Error processing or drawing graph: {e}")

            self.three.place(x=65, y=115)

        def draw_graph(self, figg):
            figure = FigureCanvasTkAgg(figg, master=self.main_frame)
            figure.draw()

            figure.get_tk_widget().place(x=400, y=15)

            toolbar = NavigationToolbar2Tk(figure, self.main_frame)
            toolbar.update()
            toolbar.place(x=400, y=570)

        def toggle(self, value):
            for widget in self.main_frame.winfo_children():
                if widget != self.three:
                    widget.destroy()

            if value == 'Plot Graphs':
                self.create_main()
            elif value == 'Differentiation':
                self.differentiate()
            elif value == 'Integration':
                self.integrate()

        @staticmethod
        def processor():
            cmd2 = [sys.executable, "F_parallel_processor.py"]
            process = subprocess.Popen(cmd2)

            while process.poll() is None:
                time.sleep(0.2)

    class Accounts:
        def __init__(self, master, username, instance):
            self.main_frame = None
            self.page_top = None
            self.addmail = None
            self.mail_id = None
            self.new_pw = None
            self.inst = instance
            self.master = master
            self.uname = username

            self.make_ui()

        def make_ui(self):
            a = 30

            mydb = msl.connect(host=db_host, port=db_port, username=db_user, password=db_password, database=db_logindb)
            cursor = mydb.cursor()

            cursor.execute(f'select email from Log_Cred where u_name="{self.uname}"')
            mail_id = cursor.fetchall()[0][0]
            font_inter = ('Inter', 20)
            text_font = ("Arial", 20, 'italic')

            self.page_top = AppElements.TopBar(self.master, 'Accounts')
            self.main_frame = ctk.CTkFrame(master=self.master, width=mfw, height=mfh, fg_color=theme, corner_radius=10, border_color=b_col, border_width=b_w)

            draw_canvas = tk.Canvas(self.main_frame, width=880, height=mfh, bg='#191919', bd=0, highlightthickness=0)
            draw_canvas.place(x=174, y=0)
            draw_canvas.create_line(0, 38, 879, 38, fill='#3d3d3d', width=4)
            draw_canvas.create_line(30, 325-a, 879, 325-a, fill='#3d3d3d', width=4)

            general = ctk.CTkLabel(self.main_frame, text='General', font=('Inter', 28, 'italic', 'bold'))
            name = ctk.CTkLabel(self.main_frame, text=f'Name\t\t - {self.uname}', font=font_inter)
            self.mail_id = ctk.CTkLabel(self.main_frame, text=f'Mail ID (Optional)\t - {mail_id if mail_id is not None else "NULL"}', font=font_inter)

            if mail_id is None:
                self.addmail = ctk.CTkButton(self.main_frame, text='Add Mail ID', command=lambda: self.ask())
                self.addmail.place(x=30 + 300, y=110)

            reset_pw = Buttons(master=self.main_frame, width=40, height=20, text='Forgot Password?', font=font_inter,
                               command=self.change_pw)
            user_d = ctk.CTkLabel(self.main_frame, text='User Data', font=('Inter', 28, 'italic', 'bold'))

            import_data = Buttons(master=self.main_frame, width=40, height=20, text='Import Data', font=font_inter,
                                  command=lambda: import_util(self.uname))
            export_data = Buttons(master=self.main_frame, width=40, height=20, text='Export Data', font=font_inter,
                                  command=lambda: export(self.uname))
            delete_data = Buttons(master=self.main_frame, width=40, height=20, text='Clear Data', font=font_inter,
                                  command=lambda: [clear(self.uname), self.inst.home.fetch_tables()])

            label = ctk.CTkLabel(master=self.main_frame, text='GNS Version 2.0.0', text_color='#3d3d3d', font=text_font,
                                 fg_color=theme)

            import_data.place(x=30, y=355-a)
            export_data.place(x=30, y=415-a)
            delete_data.place(x=30, y=475 - a)

            label.place(relx=0.825, rely=0.935)
            reset_pw.place(x=30, y=535 - a)
            user_d.place(x=30, y=305 - a)
            general.place(x=30, y=20)
            name.place(x=30, y=70)

            self.mail_id.place(x=30, y=110)
            self.main_frame.place(x=mfx, y=tfy + tfw + 10)

        def ask(self):
            global mail
            mydb1 = msl.connect(host=db_host, port=db_port, username=db_user, password=db_password, database=db_logindb)
            mail = simpledialog.askstring('Input', 'Enter your Mail ID')
            cursor1 = mydb1.cursor()

            cursor1.execute('UPDATE Log_Cred SET email = %s WHERE u_name = %s;', (mail, self.uname))
            mydb1.commit()
            self.mail_id.configure(text=f'Mail ID (Optional)\t - {mail}')
            self.addmail.destroy()

        def change_pw(self):
            def fetch_change():
                p1 = str(pw_new_a.get())
                p2 = str(pw_new_b.get())
                if p1 == p2:
                    self.new_pw = p1
                else:
                    raise ValueError

                mydb1 = msl.connect(host=db_host, port=db_port, username=db_user, password=db_password, database=db_logindb)
                cursor1 = mydb1.cursor()
                query, parameters = f'update log_cred set pw= %s where u_name=%s', (self.new_pw, self.uname)
                cursor1.execute(query, parameters)
                cursor1.close()
                mydb1.commit()
                pw_frame.destroy()
                messagebox.showinfo('Information', "Password Changed")

            pw_frame = ctk.CTkFrame(master=self.main_frame, width=390, height=180, fg_color=theme)
            pw_new_a = ctk.CTkEntry(master=pw_frame, width=280, height=40)
            pw_new_b = ctk.CTkEntry(master=pw_frame, width=280, height=40)
            cancel = ctk.CTkButton(master=pw_frame, width=30, height=30, text='X', command=pw_frame.destroy)
            get_but = ctk.CTkButton(master=pw_frame, width=135, height=30, text='Change Password',
                                    command=lambda: fetch_change())

            pw_new_a.place(x=0, y=0)
            pw_new_b.place(x=0, y=60)
            get_but.place(x=0, y=120)
            cancel.place(x=135 + 10, y=120)
            pw_frame.place(x=635, y=75)

class Buttons(ctk.CTkButton):
    def __init__(self, **kwargs):
        self.corner_rad = kwargs.get("corner_radius", 0)
        self.anchor = kwargs.get('anchor', 'center')
        self.command = kwargs.get('command', None)
        self.border = kwargs.get('border', True)
        self.image = kwargs.get('image', None)
        self.font = kwargs.get('font', None)
        self.fore = kwargs.get('fgc', None)
        self.w = kwargs.get('width', 90)
        self.h = kwargs.get('height', 50)
        self.master = kwargs.get('master')
        self.text = kwargs.get('text')

        super().__init__(master=self.master, width=self.w, height=self.h, text=self.text, font=font, bg_color=theme,
                         fg_color=theme, text_color="#c1c1c1", border_width=b_w, border_color="#976E6E",
                         anchor=self.anchor, image=self.image)

        self.check_attr()
        self.change_color()

    def check_attr(self):
        if self.border:
            self.configure(width=90, height=50, font=font, bg_color=theme,
                           text_color="#c1c1c1", border_width=b_w, border_color="#976E6E")
        else:
            self.configure(width=90, height=50, font=font, bg_color=theme,
                           text_color="white", border_width=0, border_color='')

        if self.command and callable(self.command):
            self.configure(command=self.command)
        else:
            pass

        if self.font:
            self.configure(font=self.font)
        else:
            pass

    def change_color(self):
        self.bind("<Enter>", lambda e: self.configure(fg_color="#2c2c2c"))
        self.bind("<Leave>", lambda e: self.configure(fg_color=theme))

class App:
    def __init__(self, username):
        self.home = None
        self.top_bar = None
        self.sidebar = None
        self.plotpage = None
        self.accounts = None
        self.home_page = ctk.CTk()
        self.username = username
        self.home_page.title(f'Gurafu no Sensei v2.0.0')
        self.home_page.geometry(f'{win_w}x{win_h}')
        self.home_page.configure(fg_color=canvas)

        self.makeUI()
        self.show_page("Home")

    def makeUI(self):
        self.plotpage = AppElements.PlotFrame(self.home_page, inst=self)
        self.top_bar = AppElements.TopBar(self.home_page, f'Gurafu No Sensei - Home')
        self.sidebar = AppElements.SideBar(self.home_page, self, self.show_page)
        self.accounts = AppElements.Accounts(self.home_page, self.username, self)
        self.home = AppElements.HomeFrame(self.home_page, self.username, self.show_page, self.plotpage)

    def exit(self):
        pass
        self.home_page.quit()
        self.home_page.destroy()

    def show_page(self, page):
        self.plotpage.main_frame.place_forget()
        self.home.main_frame.place_forget()
        self.top_bar.top_frame.place_forget()
        self.accounts.page_top.top_frame.place_forget()
        self.accounts.main_frame.place_forget()

        if page == "Home":
            self.home.main_frame.place(x=mfx, y=mfy)
            self.top_bar.top_frame.place(x=tfx, y=tfy)

        elif page == "Plotter":
            self.plotpage.main_frame.place(x=mfx, y=5)

        elif page == "Accounts":
            self.accounts.main_frame.place(x=mfx, y=mfy)
            self.accounts.page_top.top_frame.place(x=tfx, y=tfy)

    def run(self):
        self.home_page.mainloop()

if __name__ == "__main__":
    MainApp = App('guru')
    MainApp.run()
