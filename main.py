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

        red_highlight = ["for","while", "if", "else"]
        blue_highlight = ["int", "string","float"]

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



class TextArea(object):
    def __init__(self, parent):
        #MAIN TEXT AREA
        self.Text = Text(parent.master, font=(parent.font, 16), fg="#f7f9f9", bg="#1c1c1c", insertbackground="#f7f9f9")
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
        self.bar = Menu(parent.master)
        parent.master.config(menu=self.bar)

        self.file_dropdown = Menu(self.bar, font=(parent.font, 12), bg="#282b28" , fg="#f7f9f9")
        self.file_dropdown.add_command(label="New", command=parent.newFile)
        self.file_dropdown.add_command(label="Open", command=parent.openFile)
        self.file_dropdown.add_command(label="Save", command=parent.saveFile, accelerator="Crtl+S")
        self.file_dropdown.add_command(label="Save As", command=parent.saveFileAs)
        
        self.bar.add_cascade(label="File", menu=self.file_dropdown)

        #self.button = Button(parent.master, text="X", fg="red", command=parent.master.quit)
        #self.button.pack(side=RIGHT)

class LeftMenu(object):
    def __init__(self, parent):
        self.label = Label(parent.master, text="Menu")
        self.label.pack(side=LEFT)




root = Tk()
app = App(root)
root.mainloop()