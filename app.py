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
        self.draw_widgets()

    def draw_widgets(self):
        self.leftbar = Leftbar(self)
        self.leftbar.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.workspace = Workspace(self.master)
        self.workspace.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)


class Leftbar(tk.Canvas):
    def __init__(self, master):
        self.master = master
        super(Leftbar, self).__init__(master=self.master, bg='white')
        self.add_widgets()

    def add_widgets(self):
        self.menu = Menu(self)
        self.menu.pack(side=tk.TOP, fill=tk.X )
        self.contacts = Contacts(self)
        self.contacts.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


class Menu(tk.Canvas):
    def __init__(self, master):
        self.master = master
        super(Menu, self).__init__(master=self.master)
        self.add_widgets()

    def add_widgets(self):
        pass


class Contacts(tk.Canvas):
    def __init__(self, master):
        self.master = master
        super(Contacts, self).__init__(master=self.master)
        self.add_contacts()
        scroll = tk.Scrollbar(master=self)
        scroll.pack(side='right', fill='y')
        scroll['command'] = self.yview
        self['yscrollcommand'] = scroll.set

    def add_contacts(self):
        pass


class Workspace(tk.Canvas):
    def __init__(self, master):
        self.master = master
        super(Workspace, self).__init__(master=self.master, bg='black')
        scroll = tk.Scrollbar(master=self)
        scroll.pack(side='right', fill='y')
        scroll['command'] = self.yview
        self['yscrollcommand'] = scroll.set
        self.add_widgets()


    def add_widgets(self):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    app.mainloop()