import os
import tkinter as tk
from tkinter import filedialog, ttk
from tkinter.messagebox import showinfo, showwarning
from DataHandler import DataHandler
from GraphHandler import GraphHandler


class GUIHandler(tk.Tk):
    """
    This class is responsible for handling of displaying and processing
    all the GUI elements and their properties.
    """
    def __init__(self):
        super(GUIHandler, self).__init__()
        self.graph = None
        self.data = None

        # GUI Title
        self.title("Document Analysis")

        # File selection label
        tk.Label(self, text="File:").grid(row=2)

        # File Entry's text which will change with the file name selected from browse button
        self.filename_str = tk.StringVar()
        self.filename = tk.Entry(self, textvariable=self.filename_str, width=50)
        self.filename.grid(row=2, column=1)

        # Label and Entry for document_uuid
        tk.Label(self, text="* Document UUID").grid(row=3)
        self.doc_uuid = tk.Entry(self, width=50)
        self.doc_uuid.grid(row=3, column=1)

        # Label and Entry for visitor_uuid
        tk.Label(self, text="Visitor UUID").grid(row=4)
        self.visitor_uuid = tk.Entry(self, width=50)
        self.visitor_uuid.grid(row=4, column=1)

        # Browse button to look for the file on the computer
        tk.Button(self, text="Browse File", command=self.load_file).grid(row=2, column=2, sticky=tk.W+tk.E)
        # Tasks' buttons
        tk.Button(self, text="Task 2a", command=self.get_top_ten_readers).grid(row=5, column=0, sticky=tk.W+tk.E)
        tk.Button(self, text="Task 2b", command=self.get_top_ten_readers).grid(row=5, column=2, sticky=tk.W+tk.E)
        tk.Button(self, text="Task 3a", command=self.get_top_ten_readers).grid(row=6, column=0, sticky=tk.W+tk.E)
        tk.Button(self, text="Task 3b", command=self.get_top_ten_readers).grid(row=6, column=2, sticky=tk.W+tk.E)
        tk.Button(self, text="Task 4", command=self.get_top_ten_readers).grid(row=5, column=1, sticky=tk.W+tk.E)
        tk.Button(self, text="Task 5", command=self.get_top_ten_readers).grid(row=6, column=1, sticky=tk.W+tk.E)
        tk.Button(self, text="Task 6", command=self.get_top_ten_readers).grid(row=7, column=1, sticky=tk.W+tk.E)

    ##################
    #  Task 4        #
    ##################
    def get_top_ten_readers(self):
        """
        Creates a TreeView and displays the top 10 readers list in it.
        """
        if self.file_exist():
            # Get the file name from file textbox
            self.data = DataHandler(self.filename.get().split('/')[-1])
            root = tk.Tk()
            root.title('User Ranking')
            tree = ttk.Treeview(root)
            # Set the column ids for Treeview
            tree['columns'] = ('rank', 'visitor_uuid', 'event_readtime')
            # Treeview column properties
            tree.column('#0', width=0, minwidth=0)  # Phantom column that needs to be defined
            tree.column('rank', anchor=tk.W, width=50)
            tree.column('visitor_uuid', anchor=tk.W, width=120)
            tree.column('event_readtime', anchor=tk.CENTER, width=120)
            # Column names
            tree.heading('rank', text='Rank', anchor=tk.W)
            tree.heading('visitor_uuid', text='Visitor UUID', anchor=tk.W)
            tree.heading('event_readtime', text='Read Time', anchor=tk.CENTER)
            index = 0
            for value in self.data.get_top_reader().iteritems():
                index += 1
                tree.insert(parent='', index='end', iid=index-1, text='', values=(index, value[0], int(value[1])))
            tree.pack(side=tk.TOP, fill=tk.X)

    ###########################
    #    Helper Functions     #
    ###########################
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

