import tkinter as tk
from tkinter import font as tkfont
import time

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.button_font = tkfont.Font(family='Helvetica', size=18, weight="bold")
        self.button_font_small = tkfont.Font(family='Helvetica', size=10, weight="bold")

        self.title("POMDP by Lorenzo y Jose Manuel")
        self.geometry("450x300")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageOne, PageTwo, PageThree):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Choose a problem", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        # Imagenes para los problemas
        tigerImage = tk.PhotoImage(file="images/tiger.png")
        tagImage = tk.PhotoImage(file="images/tag.png")
        poisonImage = tk.PhotoImage(file="images/poison.png")

        # Botones
        b1 = tk.Button(self, text="Tigre", command=lambda: controller.show_frame("PageOne"))
        b1.config(image=tigerImage)
        b1.image = tigerImage
        b1.place(relx=0.1, rely=0.2)
        b2 = tk.Button(self, text="Tag", command=lambda: controller.show_frame("PageOne"))
        b2.place(relx=0.7, rely=0.2)
        b2.config(image=tagImage)
        b2.image = tagImage
        b3 = tk.Button(self, text="Poison", command=lambda: controller.show_frame("PageOne"))
        b3.place(relx=0.1, rely=0.6)
        b3.config(image=poisonImage)
        b3.image = poisonImage
        b4 = tk.Button(self, text="XXXX", command=lambda: controller.show_frame("PageOne"))
        b4.place(relx=0.7, rely=0.6)
        b4.config(image=poisonImage)
        b4.image = poisonImage


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Choose an algorithm", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()

        # Botones
        b1 = tk.Button(self, text="POMCP", font=controller.button_font, command=lambda: controller.show_frame("PageTwo"))
        b1.place(relx=0.1, rely=0.4)
        b2 = tk.Button(self, text="PBVI", font=controller.button_font, command=lambda: controller.show_frame("PageTwo"))
        b2.place(relx=0.7, rely=0.4)



class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Choose an execution mode", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()

        # Botones
        b1 = tk.Button(self, text="Interactive execution", font=controller.button_font_small, command=lambda: controller.show_frame("PageThree"))
        b1.place(relx=0.1, rely=0.4)
        b2 = tk.Button(self, text="Silent execution", font=controller.button_font_small, command=lambda: controller.show_frame("PageThree"))
        b2.place(relx=0.7, rely=0.4)
        b3 = tk.Button(self, text="Benchmark execution", font=controller.button_font_small, command=lambda: controller.show_frame("PageThree"))
        b3.place(relx=0.35, rely=0.7)

class PageThree(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Output", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()

        txt = tk.Text(self, width=40, height=10)
        txt.insert(tk.END, 'HOLA')
        txt.pack()


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()