import tkinter as tk
from client import Client
import app_style as style
from db_client import DB


class Label(tk.Label):
    def __init__(self, master, text='', font='Arial 17', justify=tk.LEFT, bg=style.bg_main):
        super(Label, self).__init__(master=master, text=text, font=font, justify=justify, bg=bg)


class Button(tk.Button):
    def __init__(self,
                 master,
                 text='',
                 font='Arial 17',
                 justify=tk.CENTER,
                 bg=style.bg_main,
                 command=None,
                 height=1,
                 width=20):
        super(Button, self).__init__(master=master,
                                     text=text,
                                     font=font,
                                     justify=justify,
                                     bg=bg,
                                     command=command,
                                     height=height,
                                     width=width)

class App(tk.Frame):
    def __init__(self, master):
        self.master = master
        super().__init__(self.master)

        self.master.geometry("{0}x{1}+0+0".format(self.master.winfo_screenwidth() - 100,
                                                  self.master.winfo_screenheight() - 100))
        self.master.title("VMessanger")
        self.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.window = None
        if client.user_name is None:
            self.change_window('sing_up')
        else:
            self.change_window('main')
            self.master.title(' '.join([str(x) for x in client.get_user()]))

    def change_window(self, name):
        if not self.window is None:
            self.remove_window()
        if name == 'sing_up':
            self.window = Sing_up_window(self)
        elif name == 'main':
            self.window = Main_window(self)

    def remove_window(self):
        self.window.remove()
        self.window.destroy()


class Sing_up_window(tk.Frame):
    def __init__(self, master):
        self.name = 'sing_up'
        self.master = master
        super(Sing_up_window, self).__init__(master=master, bg=style.bg_main)
        self.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.draw_widgets()
        self.bind('<Configure>', self.resize)

    def draw_widgets(self):
        self.sing_up_input = tk.Frame(self, bg=style.bg_main)
        self.sing_up_input.place(x=self.winfo_width()//2, y=self.winfo_height()//2, anchor=tk.CENTER)
        self.lbl_title = Label(self.sing_up_input, text='Sing up\nEnter these fields:', font='Arial 27')
        self.lbl_title.grid(row=0, columnspan=2, ipady=10, sticky=tk.NW)
        self.lbl_name = Label(self.sing_up_input, text='Name:')
        self.lbl_name.grid(row=1)
        self.input_name = tk.Entry(self.sing_up_input, font='Arial 17')
        self.input_name.grid(row=1, column=1)
        self.confirm_btn = Button(self.sing_up_input, text='Confirm', height=1, width=20, font='15', bg=style.bg_main, command=self.press_confirm_btn)
        self.confirm_btn.grid(row=2, column=1, sticky=tk.NE)
        self.attention_lbl = Label(self.sing_up_input)
        self.attention_lbl.grid(row=3, columnspan=2, sticky=tk.NW)

    def resize(self, event):
        self.update()
        self.sing_up_input.place(x=self.winfo_width() // 2, y=self.winfo_height() // 2, anchor=tk.CENTER)

    def remove(self):
        self.sing_up_input.destroy()

    def press_confirm_btn(self):
        name = self.input_name.get().lower()
        if len(name) > 14:
            self.show_attention('longname')
            return
        if name == '':
            self.show_attention('empty')
            return

        good_letters='qwertyuiopasdfghjklzxcvbnm'

        for letter in name:
            if not letter in good_letters:
                self.show_attention('badname')
                return

        result = client.sing_up(name)
        if result is None:
            self.show_attention('hasalready')
            return
        else:
            client.set_user(user_id=result, user_name=name)
            print(result, name, client.last_time)
            db.save_user_if_not_exists(user_id=int(result), user_name=str(name), last_time=str(client.last_time))
            self.master.change_window('main')

    def show_attention(self, attention):
        if attention == 'empty':
            self.attention_lbl['text'] = 'empty'
        elif attention == 'badname':
            self.attention_lbl['text'] = 'badname'
        elif attention == 'longname':
            self.attention_lbl['text'] = 'longname'
        elif attention == 'hasalready':
            self.attention_lbl['text'] = 'hasalready'
        self.input_name.delete(0, 'end')


class Main_window(tk.Canvas):
    def __init__(self, master):
        self.name = 'main'
        self.master = master
        super(Main_window, self).__init__(master=master)
        self.pack(side=tk.LEFT, fill=tk.BOTH)
        self.draw_widgets()

    def draw_widgets(self):
        self.leftbar = Leftbar(self)
        self.leftbar.pack(side=tk.LEFT, fill=tk.Y)
        self.workspace = Workspace(self.master)
        self.workspace.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def remove(self):
        self.leftbar.destroy()
        self.workspace.destroy()


class Leftbar(tk.Canvas):
    def __init__(self, master):
        self.master = master
        super(Leftbar, self).__init__(master=self.master, bg='white')
        self.add_widgets()

    def add_widgets(self):
        self.menu = Menu(self)
        self.menu.pack(side=tk.TOP, fill=tk.X)
        self.contacts = Contacts(self)
        self.contacts.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)


class Menu(tk.Canvas):
    def __init__(self, master):
        self.master = master
        self.btn_size = (35, 3)
        super(Menu, self).__init__(master=self.master)
        self.add_widgets()

    def add_widgets(self):
        self.menu_btn = tk.Button(self, text="Menu", width=self.btn_size[0], height=self.btn_size[1])
        self.menu_btn.pack(side=tk.LEFT)


class Contacts(tk.Canvas):
    def __init__(self, master):
        self.master = master
        super(Contacts, self).__init__(master=self.master)
        self.add_contacts()
        self.add_scroll()

    def add_scroll(self):
        scroll = tk.Scrollbar(master=self, orient=tk.VERTICAL, command=self.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.configure(scrollregion=self.bbox(tk.ALL),
                       yscrollcommand=scroll.set)

    def add_contacts(self):
        self.frame = tk.Frame(self)
        self.create_window(0, 0, anchor=tk.NW, window=self.frame)

        self.contacts = []
        for i in range(15):
            self.contacts.append(Contact(master=self.frame, name=str(i)))
        self.update_idletasks()


class Contact(tk.Button):
    def __init__(self, master, name):
        self.name = name
        self.btn_size = (35, 3)
        super(Contact, self).__init__(master=master,
                                      text=self.name,
                                      width=self.btn_size[0],
                                      height=self.btn_size[1])
        self.pack()

    def press(self):
        pass


class Workspace(tk.Canvas):
    def __init__(self, master):
        self.master = master
        super(Workspace, self).__init__(master=self.master, bg='black')
        scroll = tk.Scrollbar(master=self)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        scroll['command'] = self.yview
        self['yscrollcommand'] = scroll.set
        self.add_widgets()

    def add_widgets(self):
        pass


def connect_db2client():
    user_info = db.get_user()
    client.set_user(user_id=user_info['user_id'],
                    user_name=user_info['user_name'],
                    last_time=user_info['last_time'])


if __name__ == "__main__":
    db = DB()
    client = Client()
    connect_db2client()
    root = tk.Tk()
    app = App(root)
    app.mainloop()