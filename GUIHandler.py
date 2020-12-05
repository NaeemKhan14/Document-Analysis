import os
import tkinter as tk
from tkinter import filedialog, ttk
from tkinter.messagebox import showinfo, showwarning
from PIL import ImageTk, Image
from DataHandler import DataHandler
from GraphHandler import GraphHandler


class GUIHandler(tk.Tk):
    """
    This class is responsible for handling of displaying and processing
    all the GUI elements class and changing between tk.Frame classes.
    """
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # GUI's general properties.
        self.minsize(400, 550)
        self.title("Document Analysis")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (MainFrame, GraphsTask, DataTasks):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(MainFrame)

    def show_frame(self, class_name):
        # Show the Frame of given class.
        frame = self.frames[class_name]
        frame.tkraise()
        # Pass an event to this Frame for running functions once its visible.
        frame.event_generate("<<Show>>")


class MainFrame(tk.Frame):
    """
    This is the main page class that is displayed on load. This class
    contains collects user input and passes it on to its relevant Frame
    class to display the data. This is a child class of tk.Frame class.
    """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        tk.Label(self, text="File:").grid(row=2)

        # File Entry's text which will change with the file name selected from browse button.
        self.filename_str = tk.StringVar()
        self.filename = tk.Entry(self, textvariable=self.filename_str, width=78)
        self.filename.grid(row=2, column=1)

        # Label and Entry for document_uuid.
        tk.Label(self, text="Document UUID").grid(row=3)
        self.doc_uuid = tk.Entry(self, width=78)
        self.doc_uuid.grid(row=3, column=1)

        # Label and Entry for visitor_uuid.
        tk.Label(self, text="Visitor UUID").grid(row=4)
        self.visitor_uuid = tk.Entry(self, width=78)
        self.visitor_uuid.grid(row=4, column=1)
        # We use this text later in GraphsTask class to determine which
        # button is pressed.
        self.button_text = tk.StringVar()
        # Browse button to look for the file on the computer.
        tk.Button(self, text="Browse File", command=self.load_file).grid(row=2, column=2, sticky=tk.W + tk.E)
        # Tasks' buttons.
        tk.Button(self, text="Task 2a", command=lambda x=self: self.button_controller(GraphsTask, 'task_2a')).grid(
            row=5, column=0, sticky=tk.W + tk.E)
        tk.Button(self, text="Task 2b", command=lambda: self.button_controller(GraphsTask, 'task_2b')).grid(
            row=5, column=2, sticky=tk.W + tk.E)
        tk.Button(self, text="Task 3a", command=lambda: self.button_controller(GraphsTask, 'task_3a')).grid(
            row=6, column=0, sticky=tk.W + tk.E)
        tk.Button(self, text="Task 3b", command=lambda: self.button_controller(GraphsTask, 'task_3b')).grid(
            row=6, column=2, sticky=tk.W + tk.E)
        tk.Button(self, text="Task 4", command=lambda: self.button_controller(DataTasks, 'task_4')).grid(
            row=5, column=1, sticky=tk.W + tk.E)
        tk.Button(self, text="Task 5", command=lambda: self.button_controller(DataTasks, 'task_5')).grid(
            row=6, column=1, sticky=tk.W + tk.E)
        tk.Button(self, text="Task 6", command=lambda: self.button_controller(GraphsTask, 'task_6')).grid(
            row=7, column=1, sticky=tk.W + tk.E)

    ###########################
    #    Helper Functions     #
    ###########################
    def button_controller(self, class_name, btn_text):
        self.button_text.set(btn_text)
        self.controller.show_frame(class_name)

    def get_button_text(self):
        return self.button_text.get()

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
        # Return True if none of the above error conditions were met.
        return True


class GraphsTask(tk.Frame):
    """
    This class displays the results of Task 2 and 3.
    """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        button1 = ttk.Button(self, text="Back to Home",
                             command=lambda: self.go_back_home())
        button1.pack()
        # Bind a variable to run this function only when the Frame
        # is visible.
        self.bind("<<Show>>", self.get_graph)

    def go_back_home(self):
        """
        Destroys the results to not show them the
        next time this class is called.
        """
        self.controller.show_frame(MainFrame)
        self.img.config(image='')
        self.pack_forget()

    def get_graph(self, event):
        """
        Produces the graph based on the button clicked by user
        in MainFrame class.
        :param event:
        :return:
        """
        main_frame = self.controller.frames[MainFrame]
        if main_frame.file_exist():
            graph = GraphHandler(main_frame.filename.get())
            image = None
            btn_txt = main_frame.get_button_text()  # Gets which button was clicked by user.
            # If it is task 2.
            if btn_txt[-2] == '2':
                # If document ID is provided.
                if not main_frame.entry_is_empty(main_frame.doc_uuid):
                    if btn_txt == 'task_2a':
                        graph.get_country_graph(main_frame.doc_uuid.get(), True)
                        image = Image.open("countries_graph.png")
                    elif btn_txt == 'task_2b':
                        graph.get_country_graph(main_frame.doc_uuid.get(), True)
                        graph.get_continent_graph(True)
                        image = Image.open("continents_graph.png")
                else:  # If no document ID is provided.
                    showwarning('No document UUID given', 'Document UUID is required')
                    self.controller.show_frame(MainFrame)
            # If it is task 3.
            elif btn_txt[-2] == '3':
                if btn_txt == 'task_3a':
                    graph.get_browser_data_graph(True)
                    image = Image.open("browser_data_graph.png")
                elif btn_txt == 'task_3b':
                    graph.get_browser_names_graph(True)
                    image = Image.open("browser_names_graph.png")
            # If it is task 6.
            elif btn_txt[-1] == '6':
                # If document ID is provided.
                if not main_frame.entry_is_empty(main_frame.doc_uuid):
                    graph.show_likes_graph(main_frame.doc_uuid.get(), main_frame.visitor_uuid.get(), True)
                    image = Image.open("likes_graph.dot.png")
                else:  # If no document ID is provided.
                    showwarning('No document UUID given', 'Document UUID is required')
                    self.controller.show_frame(MainFrame)
            # Display the results
            render = ImageTk.PhotoImage(image)
            self.img = tk.Label(self, image=render)
            self.img.image = render
            self.img.place(x=42, y=30)
            self.img.pack(fill=tk.BOTH, expand=tk.YES)
        else:  # If file related error happens, return to main page.
            self.controller.show_frame(MainFrame)


class DataTasks(tk.Frame):
    """
    This class displays the results of Task 4, 5 and 6.
    """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        button1 = ttk.Button(self, text="Back to Home",
                             command=lambda: self.go_back_home())
        button1.pack()
        self.controller = controller
        self.bind("<<Show>>", self.process_data)

    def go_back_home(self):
        """
        Destroys the TreeView to not show previous results the
        next time this class is called.
        """
        self.controller.show_frame(MainFrame)
        if self.tree:
            self.tree.destroy()

    def process_data(self, event):
        """
        Creates a TreeView and displays the result according to task selected.
        """
        main_frame = self.controller.frames[MainFrame]
        # If file is selected.
        if main_frame.file_exist():
            # If selection is task 4, then load DataHandler, otherwise
            # load GraphHandler class.
            task_4 = main_frame.get_button_text() == 'task_4'
            data = DataHandler(main_frame.filename.get())
            self.tree = ttk.Treeview(self)
            self.tree.pack(expand='YES', fill='both')
            # Set the column name based on task selected by user
            col_name = 'event_readtime' if task_4 else 'subject_doc_id'
            # Set the column ids for TreeView.
            self.tree['columns'] = ('rank', 'visitor_uuid', col_name)
            # TreeView column properties.
            self.tree['show'] = 'headings'
            self.tree.column('rank', anchor=tk.W, width=42, stretch='no')
            self.tree.column('visitor_uuid', anchor=tk.W, width=100)
            self.tree.column(col_name, anchor=tk.W, width=100)
            # Column names.
            self.tree.heading('rank', text='Rank', anchor=tk.W)
            self.tree.heading('visitor_uuid', text='Visitor UUID', anchor=tk.W)
            # Set the column text based on task selected by user
            col_text = 'Read Time' if task_4 else 'Document UUID'
            self.tree.heading(col_name, text=col_text, anchor=tk.W)
            # Populate the TreeView with results based on task selected.
            index = 1
            if task_4:
                for value in data.get_top_reader().iteritems():
                    self.tree.insert(parent='', index='end', iid=index, text='',
                                     values=(index, value[0], int(value[1])))
                    index += 1
            else:
                # If task 5 and document UUID is provided
                if not main_frame.entry_is_empty(main_frame.doc_uuid):
                    for value in data.get_top_ten_likes(main_frame.doc_uuid.get(),
                                                        main_frame.visitor_uuid.get()).iteritems():
                        self.tree.insert(parent='', index='end', iid=index, text='',
                                         values=(index, value[0][0], value[0][1]))
                        index += 1
                else:  # If no document UUID provided.
                    showwarning('No document UUID given', 'Document UUID is required')
                    self.controller.show_frame(MainFrame)
            self.tree.pack(side=tk.TOP, fill='x')
        else:  # Return to main page if no file is selected.
            self.controller.show_frame(MainFrame)
