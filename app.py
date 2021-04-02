import tkinter as tk
import client


class App(tk.Frame):
    def __init__(self, master):
        self.master = master
        super().__init__(self.master)
        self.master.title = "VMessanger"
        self.master.geometry("{0}x{1}+0+0".format(self.master.winfo_screenwidth() - 100,
                                                  self.master.winfo_screenheight() - 100))
        self.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.window = None
        self.change_window('main')

    def change_window(self, name):
        if not self.window is None:
            self.remove_window()
        if name == 'sing_up':
            self.window = Sing_up_window(self)
        elif name == 'main':
            self.window = Main_window(self)

    def remove_window(self):
        self.window.destroy()


class Sing_up_window(tk.Canvas):
    def __init__(self, master):
        self.name = 'sing_up'
        self.master = master
        super(Sing_up_window, self).__init__(master=master)
        self.draw_widgets()

    def draw_widgets(self):
        pass


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


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    app.mainloop()