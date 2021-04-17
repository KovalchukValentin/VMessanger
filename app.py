import tkinter as tk
from client import Client
import app_style as style
from db_client import DB
import time


class Entry(tk.Entry):
    def __init__(self, master, font='Arial 12', height=None, width=None):
        super(Entry, self).__init__(master=master, font=font, cursor="xterm", width=width)


class Label(tk.Label):
    def __init__(self, master, text='', font='Arial 12', justify=tk.LEFT, bg=style.bg_main, height=None, width=None):
        super(Label, self).__init__(master=master, text=text, font=font, justify=justify, bg=bg, width=width, height=height)


class Button(tk.Button):
    def __init__(self,
                 master,
                 text='',
                 font='Arial 12',
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
            self.master.title(' '.join([str(item) for key, item in client.get_user().items()]))

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
        attention = client.check_name(name)
        if not attention:
            user_id = client.sing_up(name)
            if user_id is None:
                self.show_attention(attention='hasalready')
            else:
                client.set_user(user_name=name, user_id=user_id)
                self.master.change_window('main')
                db.save_user_if_not_exists(client.get_user())
        else:
            self.show_attention(attention=attention)

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
        self.contacts.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.add_contact_btn = Button(master=self, text='Add contact', width=30, height=2, command=self.press_add_contact)
        self.add_contact_btn.pack(side=tk.TOP, fill=tk.X)

    def press_add_contact(self):
        Add_contact(self)


class Add_contact(tk.Toplevel):
    def __init__(self, master):
        super(Add_contact, self).__init__(master=master)
        self.grab_set()
        self.focus_set()
        self.title('Add contact')
        self.geometry('400x220+400+300')
        self.resizable(False, False)
        label_description = Label(self, text='Name:')
        label_description.place(x=50, y=50)
        self.attention_lbl = Label(self)
        self.attention_lbl.place(x=110, y=75)
        self.input_name = Entry(self)
        self.input_name.place(x=110, y=50)
        cancel_btn = Button(self, text="Cancel", width=10, height=1, command=self.destroy)
        cancel_btn.place(x=70, y=120)
        add_btn = Button(self, text="Add", width=10, height=1, command=self.press_add_contact)
        add_btn.place(x=195, y=120)

    def press_add_contact(self):
        name = self.input_name.get().lower()
        attention = client.check_name(name)
        if not attention:
            result = client.add_contact(contact_name=name)
            if result == 'ok':
                self.destroy()
                self.master.contacts.update_contacts()
                return
            attention = result
        self.show_attention(attention)

    def show_attention(self, attention):
        if attention == 'is_your_name':
            self.attention_lbl['text'] = 'Lol it is U name'
        elif attention == 'contact_is_not_exist':
            self.attention_lbl['text'] = 'Contact is not exist'
        elif attention == 'contact_is_in_contacts':
            self.attention_lbl['text'] = 'Contact is in contact'
        else:
            self.attention_lbl['text'] = 'Wrong name'


class Menu(tk.Canvas):
    def __init__(self, master):
        self.master = master
        self.btn_size = (30, 3)
        super(Menu, self).__init__(master=self.master)
        self.add_widgets()

    def add_widgets(self):
        self.menu_btn = Button(self, text="Menu", width=self.btn_size[0], height=self.btn_size[1])
        self.menu_btn.pack(side=tk.LEFT)


class Contacts(tk.Canvas):
    def __init__(self, master):
        self.master = master
        super(Contacts, self).__init__(master=self.master)
        self.show_contacts()
        self.add_scroll()

    def add_scroll(self):
        scroll = tk.Scrollbar(master=self, orient=tk.VERTICAL, command=self.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.configure(scrollregion=self.bbox(tk.ALL),
                       yscrollcommand=scroll.set)

    def show_contacts(self):
        self.frame = tk.Frame(self)
        self.create_window(0, 0, anchor=tk.NW, window=self.frame)
        self.contacts = client.get_contacts()
        if not self.contacts is None:
            self.contact_btns = []
            for contact_id, contact_name in self.contacts:
                self.contact_btns.append(Contact(master=self.frame, name=str(contact_name), contact_id=contact_id))
        self.update_idletasks()

    def update_contacts(self):
        self.frame.destroy()
        self.show_contacts()
        self.configure(scrollregion=self.bbox(tk.ALL))


class Contact(Button):
    def __init__(self, master, name, contact_id):
        self.contact_id = int(contact_id)
        self.name = name
        self.btn_size = (28, 3)
        super(Contact, self).__init__(master=master,
                                      text=self.name.title(),
                                      width=self.btn_size[0],
                                      height=self.btn_size[1], command=self.press)
        self.pack()

    def press(self):
        client.current_chat_id = client.get_chat_id(contact_id=self.contact_id)
        app.window.workspace.update_space(self.name)


class Workspace(tk.Canvas):
    def __init__(self, master):
        self.master = master
        super(Workspace, self).__init__(master=self.master, bg='black')


    def update_space(self, contact_name):
        contact_name = contact_name.title()
        if not client.current_chat_id is None:
            try:
                self.title['text'] = contact_name
                self.clr_text()
                self.correct_height_textbox()
            except:
                self.topbar = tk.Frame(self)
                self.topbar.pack(side=tk.TOP, fill=tk.X)
                self.title = Label(self.topbar, text=contact_name, height=3, justify=tk.LEFT)
                self.title.pack(side=tk.LEFT)

                self.messages_space = Messages_space(self)
                self.messages_space.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

                self.sendbar = tk.Frame(self)
                self.sendbar.pack(side=tk.TOP, fill=tk.X)
                self.message_input = tk.Text(self.sendbar, font="Arial 18", height=1,cursor="xterm")
                self.message_input.pack(side=tk.LEFT, fill=tk.X, expand=True)
                self.send_btn = Button(self.sendbar, text="Send", width=10, height=3, command=self.press_send)
                self.send_btn.pack(side=tk.LEFT)

                self.message_input.bind('<Return>', self.press_entr)
                self.message_input.bind("<Control-Return>", self.press_send)
                self.message_input.bind('<BackSpace>', self.press_backspace)
                # self.entry = tk.Entry(self.sendbar, width=30, font="Arial 18", bd=10)
                # self.entry.focus()
                # self.entry.pack(side=tk.LEFT)


    def press_entr(self, event):
        self.correct_height_textbox('entr')
        # print(self.message_input.get())

    def press_send(self, event=None):
        self.send()
        self.clr_text()
        self.correct_height_textbox()

    def press_backspace(self, event):
        self.correct_height_textbox('back')

    def correct_height_textbox(self, key=None):
        count_of_lines = int(self.message_input.index('end').split('.')[0]) - 1
        if key == 'entr':
            count_of_lines += 1
        if count_of_lines <= 10:
            self.message_input.config(height=count_of_lines)

    def send(self):
        self.message_input.get("0.0", 'end')

    def clr_text(self):
        self.message_input.delete('1.0', 'end')


class Messages_space(tk.Canvas):
    def __init__(self, master):
        self.master = master
        super(Messages_space, self).__init__(master=self.master)
        self.show_messages()
        self.add_scroll()

    def add_scroll(self):
        scroll = tk.Scrollbar(master=self, orient=tk.VERTICAL, command=self.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.configure(scrollregion=self.bbox(tk.ALL),
                       yscrollcommand=scroll.set)

    def show_messages(self):
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
    while True:
        root.update()
        app.update()
        time.sleep(0.01)