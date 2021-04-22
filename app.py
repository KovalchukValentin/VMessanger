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
                 width=20,
                 anchor=tk.CENTER):
        super(Button, self).__init__(master=master,
                                     text=text,
                                     font=font,
                                     justify=justify,
                                     bg=bg,
                                     command=command,
                                     height=height,
                                     width=width,
                                     anchor=anchor)


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
            self.change_window('sing_in')
        else:
            self.change_window('main')
            self.master.title(' '.join([str(item) for key, item in client.get_user().items()]))

    def change_window(self, name):
        if not self.window is None:
            self.remove_window()
        if name == 'sing_in':
            self.window = Sing_in_window(self)
        elif name == 'sing_up':
            self.window = Sing_up_window(self)
        elif name == 'main':
            self.window = Main_window(self)

    def remove_window(self):
        self.window.remove()
        self.window.destroy()


class Template_start_window(tk.Frame):
    def __init__(self, master):
        self.set_name()
        self.master = master
        super(Template_start_window, self).__init__(master=master, bg=style.bg_main)
        self.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.center_frame = tk.Frame(self, bg=style.bg_main)
        self.center_frame.place(x=self.winfo_width() // 2, y=self.winfo_height() // 2, anchor=tk.CENTER)
        self.attention_lbl = Label(self.center_frame)

        self.draw_widgets()
        self.bind('<Configure>', self.resize)

    def draw_widgets(self):
        pass

    def resize(self, event):
        self.update()
        self.center_frame.place(x=self.winfo_width() // 2, y=self.winfo_height() // 2, anchor=tk.CENTER)

    def remove(self):
        self.center_frame.destroy()

    def press_confirm_btn(self):
        pass

    def show_attention(self, attention):
        if attention == 'empty':
            self.attention_lbl['text'] = 'empty'
        elif attention == 'badname':
            self.attention_lbl['text'] = 'badname'
        elif attention == 'longname':
            self.attention_lbl['text'] = 'longname'
        elif attention == 'hasalready':
            self.attention_lbl['text'] = 'hasalready'

    def set_name(self):
        self.name = 'template'

    def check_name(self, name):
        attention = client.check_name(name)
        self.show_attention(attention=attention)


class Sing_up_window(Template_start_window):
    def set_name(self):
        self.name = 'sing_up'

    def draw_widgets(self):
        self.lbl_title = Label(self.center_frame, text='Sing up\nEnter these fields:', font='Arial 27')
        self.lbl_title.grid(row=0, columnspan=2, ipady=10, sticky=tk.NW)

        self.lbl_name = Label(self.center_frame, text='Name:')
        self.lbl_name.grid(row=1)

        self.input_name = tk.Entry(self.center_frame, font='Arial 17')
        self.input_name.grid(row=1, column=1)

        self.confirm_btn = Button(self.center_frame, text='Confirm', height=1, width=20, font='15', bg=style.bg_main,
                                  command=self.press_confirm_btn)
        empty = Label(self.center_frame).grid(row=2)
        self.confirm_btn.grid(row=3, column=1, sticky=tk.NE)
        self.sing_in_btn = Button(self.center_frame, text="Sing in", height=1, font='15', bg=style.bg_main,
                                  command=self.sing_in_press)
        self.sing_in_btn.grid(row=3, column=0)
        self.attention_lbl.grid(row=4, columnspan=2, sticky=tk.NW)

    def sing_in_press(self):
        app.change_window('sing_in')

    def press_confirm_btn(self):
        name = self.input_name.get().lower()
        self.check_name(name=name)
        self.input_name.delete(0, 'end')

    def check_name(self, name):
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


class Sing_in_window(Template_start_window):
    def set_name(self):
        self.name = 'sing_in'

    def draw_widgets(self):
        self.lbl_title = Label(self.center_frame, text='Sing in\nEnter these fields:', font='Arial 27')
        self.lbl_title.grid(row=0, columnspan=2, ipady=10, sticky=tk.NW)
        self.lbl_name = Label(self.center_frame, text='Name:')
        self.lbl_name.grid(row=1)
        self.input_name = tk.Entry(self.center_frame, font='Arial 17')
        self.input_name.grid(row=1, column=1)
        self.confirm_btn = Button(self.center_frame, text='Confirm', height=1, width=20, font='15', bg=style.bg_main,
                                  command=self.press_confirm_btn)
        empty = Label(self.center_frame).grid(row=2)
        self.confirm_btn.grid(row=3, column=1, sticky=tk.NE)
        self.sing_up_btn = Button(self.center_frame, text="Sing up", height=1, font='15', bg=style.bg_main,
                                  command=self.sing_up_press)
        self.sing_up_btn.grid(row=3, column=0)
        self.attention_lbl.grid(row=4, columnspan=2, sticky=tk.NW)

    def press_confirm_btn(self):
        name = self.input_name.get().lower()
        self.check_name(name=name)

    def sing_up_press(self):
        app.change_window('sing_up')

    def check_name(self, name):
        attention = client.check_name(name)
        if not attention:
            user_id = client.sing_in(name)
            if user_id is None:
                self.show_attention(attention='wrong name')
            else:
                client.set_user(user_name=name, user_id=user_id)
                self.master.change_window('main')
                db.save_user_if_not_exists(client.get_user())
                return
        else:
            self.show_attention(attention=attention)
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

    def update_data(self):
        self.leftbar.update_data()
        self.workspace.update_data()


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

    def update_data(self):
        pass


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
        self.log_out = Button(self, text="Log Out", width=self.btn_size[0], height=self.btn_size[1], command=self.press_log_out)
        self.log_out.pack(side=tk.LEFT)

    def press_log_out(self):
        db.remove_user()
        app.change_window(name='sing_in')


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
        client.current_chat = {'chat_id': client.get_chat_id(contact_id=self.contact_id),
                                  'contact_id' : self.contact_id,
                                  'contact_name': self.name}
        app.window.workspace.update_space()


class Workspace(tk.Canvas):
    def __init__(self, master):
        self.master = master
        super(Workspace, self).__init__(master=self.master, bg='black')

    def update_space(self):
        if not client.current_chat is None:
            contact_name = client.current_chat['contact_name'].title()
            try:
                self.title['text'] = contact_name.title()
                self.clr_text()
                self.correct_height_textbox()
                self.messages_space.show_messages()
            except:
                self.topbar = tk.Frame(self)
                self.topbar.pack(side=tk.TOP, fill=tk.X)
                self.title = Label(self.topbar, text=contact_name, height=3, justify=tk.LEFT)
                self.title.pack(side=tk.LEFT)

                self.messages_space = Messages_space(self)
                self.messages_space.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

                self.sendbar = tk.Frame(self)
                self.sendbar.pack(side=tk.TOP, fill=tk.X)
                self.message_input = tk.Text(self.sendbar, font="Arial 18", height=1, cursor="xterm")
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
            self.messages_space.resize_space()

    def send(self):
        text = self.message_input.get("0.0", 'end')
        client.send_message(self.format_send(text, len_str=50))

    def format_send(self, text, len_str):
        text = text.strip()
        strings = text.split('\n')
        new_text = []
        for string in strings:
            if len(string) >= len_str:
                words = string.split(' ')
                string = ''
                count_len = 0
                for word in words:
                    len_w = len(word)
                    if len_w + count_len >= len_str:
                        bitword = word[:len_str - count_len:]
                        endword = word[len_str - count_len::]
                        if len(bitword) <= 8:
                            new_text.append(string)
                            string = word + ' '
                        else:
                            new_text.append(string + bitword)
                            string = endword + ' '
                        count_len = len(string)
                    else:
                        string += word + ' '
                        count_len = len(string)
                    if count_len >= len_str:
                        new_text.append(string)
                        string = ''
                        count_len = 0
                new_text.append(string)
            else:
                new_text.append(string)
        return '\n'.join(new_text)


    def clr_text(self):
        self.message_input.delete('1.0', 'end')

    def update_data(self):
        pass
        # if not client.current_chat_id is None:
        #     self.messages_space.add_messages()


class Messages_space(tk.Canvas):
    def __init__(self, master):
        self.master = master
        super(Messages_space, self).__init__(master=self.master)
        self.frame = tk.Frame(self)
        self.frame_id = self.create_window(0, 0, anchor=tk.NW, window=self.frame)
        self.add_scroll()
        self.show_messages()

    def add_scroll(self):
        self.scroll = tk.Scrollbar(master=self, orient=tk.VERTICAL, command=self.yview)
        self.scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.configure(scrollregion=self.bbox(tk.ALL),
                       yscrollcommand=self.scroll.set)
        self.bind("<Configure>", self.resize_frame)
        self.yview_moveto(1)

    def resize_frame(self, event):
        self.itemconfig(self.frame_id, width=event.width-25)
        self.scroll.set(1, 1)

    def resize_space(self):
        move = False
        if self.yview()[1] == 1:
            move = True
        self.update_idletasks()
        self.configure(scrollregion=self.bbox(tk.ALL),
                       yscrollcommand=self.scroll.set)
        if move:
            self.yview_moveto(1)


    def show_messages(self):
        messages = db.get_messages_from_chat(client.current_chat['chat_id'])
        try:
            self.clear()
        except:
            pass
        self.messages = []
        self.add_messages(messages)

    def add_messages(self, messages):
        if not messages is None:
            for message in messages:
                self.messages.append(Message(self.frame, message))
        self.resize_space()

    def clear(self):
        for message in self.messages:
            message.destroy()


class Message(tk.Frame):
    def __init__(self, master, message):
        if set(message) != {'id', 'chat_id', 'user_id', 'text', 'time'}:
            return
        # print(message)
        self.init_message(message)
        super(Message, self).__init__(master=master)
        self.pack(side=tk.TOP, fill=tk.X, expand=True)
        count_of_line = len(self.show_text.split('\n'))
        body = Button(self, text=self.show_text, width=50, height=count_of_line*1, justify=tk.LEFT, anchor=tk.W)
        if self.user_id == client.user_id:
            body.pack(side=tk.RIGHT)
        else:
            body.pack(side=tk.LEFT)

    def init_message(self, message):
        self.id_message = message['id']
        self.chat_id = message['chat_id']
        self.user_id = message['user_id']
        self.text = message['text']
        self.time = message['time']
        self.show_text = self.format_message()

    def format_message(self):
        return f"{self.get_name(self.user_id)}:\n{self.text}\n{self.time}"

    def get_name(self, user_id):
        if user_id == client.user_id:
            return client.user_name.title()
        return client.current_chat['contact_name'].title()

def connect_db2client():
    user_info = db.get_user()
    client.set_user(user_id=user_info['user_id'],
                    user_name=user_info['user_name'],
                    last_time=user_info['last_time'])


def stop():
    global run
    if app.window.name == 'main':
        db.save_user_if_not_exists(client.get_user())
    run = False


def run_app():
    global run, new_messages
    run = True
    new_messages = None
    counter = 0
    while run:
        root.update()
        app.update()
        if counter == 240 and app.window.name == 'main':
            # print(client.get_messages())
            new_messages = client.get_messages()
            if not new_messages is None:
                try:
                    app.window.workspace.messages_space.add_messages(new_messages)
                except:
                    pass
                db.save_messages(new_messages)
                app.window.update_data()
        if counter >= 240:
            counter = 0
        time.sleep(0.01)
        counter += 1


# def test_format_send():
#     text = '''\n\nHello\nmy name is Gogoses i am good programer i think cuz i want be it i am fine 123456789012345678901234567890123456789012345678901234567890\n'''
#     result = app.window.workspace.format_send(text, 50)
#     print(result)

if __name__ == "__main__":
    db = DB()
    client = Client()
    connect_db2client()
    root = tk.Tk()
    app = App(root)
    root.protocol("WM_DELETE_WINDOW", stop)
    # test_format_send()
    run_app()