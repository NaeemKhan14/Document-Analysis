import os
import time
import tkinter as tk
from tkinter import filedialog, ttk
from tkinter.messagebox import showinfo, showwarning

from PIL import ImageTk, Image

from DataHandler import DataHandler
from GraphHandler import GraphHandler

LARGE_FONT = ("Verdana", 12)


class GUIHandler(tk.Tk):
    """
    This class is responsible for handling of displaying and processing
    all the GUI elements and their properties.
    """

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.graph = None
        self.minsize(400, 550)
        # GUI Title
        self.title("Document Analysis")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (MainFrame, Task2a, Task4):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(MainFrame)

    def show_frame(self, class_name):
        # Show the frame of given class
        frame = self.frames[class_name]
        frame.tkraise()
        # Pass an event to this Frame for running functions once its visible.
        frame.event_generate("<<Show>>")


class MainFrame(tk.Frame):
    # File selection label
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.data = None
        tk.Label(self, text="File:").grid(row=2)

        # File Entry's text which will change with the file name selected from browse button
        self.filename_str = tk.StringVar()
        self.filename = tk.Entry(self, textvariable=self.filename_str, width=78)
        self.filename.grid(row=2, column=1)

        # Label and Entry for document_uuid
        tk.Label(self, text="Document UUID").grid(row=3)
        self.doc_uuid = tk.Entry(self, width=78)
        self.doc_uuid.grid(row=3, column=1)

        # Label and Entry for visitor_uuid
        tk.Label(self, text="Visitor UUID").grid(row=4)
        self.visitor_uuid = tk.Entry(self, width=78)
        self.visitor_uuid.grid(row=4, column=1)

        # Browse button to look for the file on the computer
        tk.Button(self, text="Browse File", command=self.load_file).grid(row=2, column=2, sticky=tk.W + tk.E)
        # Tasks' buttons
        tk.Button(self, text="Task 2a", command=lambda: controller.show_frame(Task2a)).grid(row=5, column=0,
                                                                                            sticky=tk.W + tk.E)
        tk.Button(self, text="Task 2b", command=lambda: controller.show_frame(Task2a)).grid(row=5, column=2,
                                                                                                sticky=tk.W + tk.E)
        tk.Button(self, text="Task 3a", command=lambda: controller.show_frame(Task2a)).grid(row=6, column=0,
                                                                                            sticky=tk.W + tk.E)
        tk.Button(self, text="Task 3b", command=lambda: controller.show_frame(Task2a)).grid(row=6, column=2,
                                                                                            sticky=tk.W + tk.E)
        tk.Button(self, text="Task 4", command=lambda: controller.show_frame(Task4)).grid(row=5, column=1,
                                                                                          sticky=tk.W + tk.E)
        tk.Button(self, text="Task 5", command=lambda: controller.show_frame(Task2a)).grid(row=6, column=1,
                                                                                           sticky=tk.W + tk.E)
        tk.Button(self, text="Task 6", command=lambda: controller.show_frame(Task2a)).grid(row=7, column=1,
                                                                                           sticky=tk.W + tk.E)

    ###########################
    #    Helper Functions     #
    ###########################
    def get_button_name(self, b_name):
        return b_name.widget._name

    def get_file_name(self):
        return self.filename_str.get()

    def entry_is_empty(self, entry_box):
        """
        Checks if the given Entry box is empty or not.
        :param entry_box: The tk.Entry to check.
        :return: Boolean based on tk.Entry value.
        """
        if len(entry_box.get()) == 0:
            return True
        return False

    def load_file(self):
        """
        This function makes sure that the selected file from file selection
        menu shows up in the filename text field.
        """
        self.filename_str.set(filedialog.askopenfilename(master=self))

    def file_exist(self):
        """
        This function is responsible for error handling of the file loader.
        :return: Boolean based on condition met.
        """
        # If no file is given.
        if self.entry_is_empty(self.filename):
            showinfo("No file given", "Please select a file to continue")
            return False
        # If the given file does not exist.
        elif not self.entry_is_empty(self.filename) and not os.path.isfile(str(self.filename.get())):
            showwarning("File does not exist", "Please select a valid file")
            return False
        # If a file other than .json is given.
        elif self.filename.get().split('/')[-1]:
            if self.filename.get().split('.')[-1].lower() != 'json':
                showwarning("Wrong file format", "Only .json files are allowed")
                return False
        # Return True if none of the above conditions were True.
        return True


class Task2a(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        button1 = ttk.Button(self, text="Back to Home",
                             command=lambda: controller.show_frame(MainFrame))
        button1.pack()

        self.controller = controller
        self.bind("<<Show>>", self.get_graph)

    def get_graph(self, event):
        main_frame = self.controller.frames[MainFrame]
        if not main_frame.entry_is_empty(main_frame.doc_uuid):
            graph = GraphHandler(main_frame.filename.get())
            graph.get_country_graph(main_frame.doc_uuid.get())
            load = Image.open("countries_graph.png")
            render = ImageTk.PhotoImage(load)
            img = tk.Label(self, image=render)
            img.image = render
            img.place(x=42, y=30)
        else:
            showwarning('No document ID given', 'Document ID field cannot be empty')
            self.controller.show_frame(MainFrame)


class Task4(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        button1 = ttk.Button(self, text="Back to Home",
                             command=lambda: self.go_back_home())
        button1.pack()
        self.controller = controller
        self.bind("<<Show>>", self.get_top_ten_readers)

    def go_back_home(self):
        self.controller.show_frame(MainFrame)
        if self.tree:
            self.tree.destroy()

    def get_top_ten_readers(self, event):
        """
        Creates a TreeView and displays the top 10 readers list in it.
        """
        if self.controller.frames[MainFrame].file_exist():
            # Get the file name from file textbox
            data = DataHandler(self.controller.frames[MainFrame].filename.get().split('/')[-1])
            self.tree = ttk.Treeview(self)
            # Set the column ids for Treeview
            self.tree['columns'] = ('rank', 'visitor_uuid', 'event_readtime')
            # TreeView column properties
            self.tree.column('#0', width=0, minwidth=0)  # Phantom column that needs to be defined
            self.tree.column('rank', anchor=tk.W, width=50)
            self.tree.column('visitor_uuid', anchor=tk.W, width=120)
            self.tree.column('event_readtime', anchor=tk.CENTER, width=120)
            # Column names
            self.tree.heading('rank', text='Rank', anchor=tk.W)
            self.tree.heading('visitor_uuid', text='Visitor UUID', anchor=tk.W)
            self.tree.heading('event_readtime', text='Read Time', anchor=tk.CENTER)
            index = 0
            for value in data.get_top_reader().iteritems():
                index += 1
                self.tree.insert(parent='', index='end', iid=index - 1, text='',
                                 values=(index, value[0], int(value[1])))
            self.tree.pack(side=tk.TOP, fill='x')
