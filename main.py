from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
'''
Orange - #ffb238
Red - #ea2b1f
Blue - #0197f6
Green - #6eeb83
Bg black - #1c1c1c
black - #282b28
black - #f7f9f9
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

    def setTitle(self, name=None):
        if name:
            self.master.title(name + " - Pyditor")
        else:
            self.master.title("Pyditor")

    def newFile(self):
        self.text_area.Text.delete(1.0, END)
        self.filename = None
        self.setTitle()

    def openFile(self):
        print(self.filename)
        self.filename = filedialog.askopenfilename(filetypes=[("All files", "*.*")])
        if self.filename:
            print(self.filename)
            self.text_area.Text.delete(1.0, END)
            with open(self.filename, "r") as f:
                self.text_area.Text.insert(1.0, f.read())
            self.setTitle(self.filename)

    def saveFile(self):
        if self.filename:
            try:
                with open(self.filename, "w") as f:
                    f.write(self.text_area.Text.get(1.0,END))
            except Exception as error:
                print(error)
        else:
            self.saveFileAs()

    def saveFileAs(self):
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




class MenuBar(object):
    def __init__(self, parent):
        self.bar = Menu(parent.master)
        parent.master.config(menu=self.bar)

        self.file_dropdown = Menu(self.bar, font=(parent.font, 12), bg="#282b28" , fg="#f7f9f9")
        self.file_dropdown.add_command(label="New", command=parent.newFile)
        self.file_dropdown.add_command(label="Open", command=parent.openFile)
        self.file_dropdown.add_command(label="Save", command=parent.saveFile)
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