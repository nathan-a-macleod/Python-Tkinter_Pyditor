from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
'''
Orange - #ffb238
Yellow - #faff00
Red - #ff2b2b
Blue - #0197f6
Green - #6eeb83
Bg black - #1c1c1c
black - #282b28
white - #f7f9f9
'''
class App:
    def __init__(self, master):

        #BASIC STUFF
        self.master = master
        self.master.title("Pyditor")
        self.master.geometry("1280x720")

        self.font = "Consolas"
        self.filename = None

        self.menu_bar = MenuBar(self)
        #self.left_menu = LeftMenu(self)
        self.text_area = TextArea(self)

        self.highlight()

    def highlight(self):
        for tag in self.text_area.Text.tag_names():
            self.text_area.Text.tag_delete(tag)

        red_highlight = ["for", "while", "if", "else", "elif", "break", "continue", "return", "in", "is", "and", "or", "not", "class", "def", "self"]
        blue_highlight = ["int", "string", "float", "double", "long", "char", "var"]
        green_highlight = ["switch", "case", "this", "False", "false", "True", "true", "None", "none", "null", "Null"] # A test

        for word in red_highlight:  
            idx = "1.0"
            while True:
                length = IntVar()
                idx = self.text_area.Text.search(r'(?:^|\s)' + word + r'(?:\s|\()', idx, nocase=1, stopindex='end',count=length, regexp = True)
                if idx:
                    idx2 = self.text_area.Text.index("%s+%dc" % (idx, (length.get() - 1)))
                    self.text_area.Text.tag_add("red", idx, idx2)
                    self.text_area.Text.tag_config("red", foreground="#ff2b2b")
                    idx = idx2
                else: break

        for word in blue_highlight:  
            idx = "1.0"
            while True:
                length = IntVar()
                idx = self.text_area.Text.search(r'(?:^|\s)' + word + r'(?:\s|$)', idx, nocase=1, stopindex='end',count=length, regexp = True)
                if idx:
                    idx2 = self.text_area.Text.index("%s+%dc" % (idx, length.get()))
                    self.text_area.Text.tag_add("blue", idx, idx2)
                    self.text_area.Text.tag_config("blue", foreground="#0197f6")
                    idx = idx2
                else: break


        for word in green_highlight:  
            idx = "1.0"
            while True:
                length = IntVar()
                idx = self.text_area.Text.search(r'(?:^|\s)' + word + r'(?:\s|$)', idx, nocase=1, stopindex='end',count=length, regexp = True)
                if idx:
                    idx2 = self.text_area.Text.index("%s+%dc" % (idx, length.get()))
                    self.text_area.Text.tag_add("green", idx, idx2)
                    self.text_area.Text.tag_config("green", foreground="#74b543")
                    idx = idx2
                else: break

        root.after(10, self.highlight)
            
    def setTitle(self, name=None):
        if name:
            self.master.title(name + " - Pyditor")
        else:
            self.master.title("Pyditor")

    def newFile(self, *args):
        self.text_area.Text.delete(1.0, END)
        self.filename = None
        self.setTitle()

    def openFile(self, *args):
        print(self.filename)
        self.filename = filedialog.askopenfilename(filetypes=[("All files", "*.*")])
        if self.filename:
            print(self.filename)
            self.text_area.Text.delete(1.0, END)
            with open(self.filename, "r") as f:
                self.text_area.Text.insert(1.0, f.read())
            self.setTitle(self.filename)

    def saveFile(self, *args):
        if self.filename:
            try:
                with open(self.filename, "w") as f:
                    f.write(self.text_area.Text.get(1.0,END))
            except Exception as error:
                print(error)
        else:
            self.saveFileAs()

    def saveFileAs(self, *args):
        try:
            new_file = filedialog.asksaveasfilename(initialfile="Untitled.txt", filetypes=[("All files", "*.*")])
            with open(new_file, "w") as nf:
                nf.write(self.text_area.Text.get(1.0,END))
            self.filename = new_file
            self.setTitle(self.filename)

        except Exception as error:
            print(error)

    def aboutPopup(self):
        rootPopup = Tk()
        rootPopup.title("About")

        textLabel = Label(rootPopup, text="This text editor is a fork of 'https://github.com/NatanCostaWar/Python-Tkinter_Pyditor' made by ChilliTech.")
        textLabel.pack()
        closePopupButton = Button(rootPopup, text="OK", command=rootPopup.destroy, width=10)
        closePopupButton.pack()
        mainloop()

class TextArea(object):
    def __init__(self, parent):
        #MAIN TEXT AREA
        self.Text = Text(parent.master, font=(parent.font, 10), fg="#f7f9f9", bg="#1c1c1c", insertbackground="#f5f7f7")
        self.scroll = Scrollbar(parent.master, command=self.Text.yview)
        self.Text.configure(yscrollcommand=self.scroll.set)

        self.Text.pack(side=LEFT, fill=BOTH, expand=True)
        self.scroll.pack(side=RIGHT,fill=Y)

        self.shortcuts(parent)

    def shortcuts(self, parent):
        self.Text.bind('<Control-s>', parent.saveFile)
        self.Text.bind('<Control-S>', parent.saveFileAs)
        self.Text.bind('<Control-o>', parent.openFile)
        self.Text.bind('<Control-n>', parent.newFile)




class MenuBar(object):
    def __init__(self, parent):
        self.bar = Menu(parent.master, bg="#282b28", fg="#f7f9f9", relief=FLAT)
        parent.master.config(menu=self.bar)

        self.file_dropdown = Menu(self.bar, font=(parent.font, 10), bg="#282b28" , fg="#f7f9f9")
        self.file_dropdown.add_command(label="New", command=parent.newFile, accelerator="Ctrl-N")
        self.file_dropdown.add_command(label="Open", command=parent.openFile, accelerator="Ctrl-O")
        self.file_dropdown.add_command(label="Save", command=parent.saveFile, accelerator="Ctrl-S")
        self.file_dropdown.add_command(label="Save As", command=parent.saveFileAs, accelerator="Ctrl-Shift-S")
        
        self.bar.add_cascade(label="File", menu=self.file_dropdown)

        #self.button = Button(parent.master, text="X", fg="red", command=parent.master.quit)
        #self.button.pack(side=RIGHT)

        self.more_dropdown = Menu(self.bar, font=(parent.font, 10), bg="#282b28", fg="#f7f9f9")
        self.more_dropdown.add_command(label="About", command=parent.aboutPopup)

        self.bar.add_cascade(label="More", menu=self.more_dropdown)

root = Tk()
app = App(root)
root.mainloop()
