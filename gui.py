import tkinter as tk
from tkinter import font as tkfont
import argparse
from pomdp_runner import PomdpRunner
from util import RunnerParams
import json

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.shared_data = {
            "problema": tk.StringVar(),
            "algoritmo": tk.StringVar(),
            "presupuesto": tk.DoubleVar(),
            "intentos": tk.IntVar(),
            "modoEjecucion": tk.StringVar(),

        }
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
        for F in (StartPage, PageOne, PageTwo, PageThree, Tries, BudgetTries):
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
        b1 = tk.Button(self, text="Tigre", command=lambda: self.actualizaValorSigue("Tigre"))
        b1.config(image=tigerImage)
        b1.image = tigerImage
        b1.place(relx=0.1, rely=0.2)
        b2 = tk.Button(self, text="Tag", command=lambda: self.actualizaValorSigue("LaserTag"))
        b2.place(relx=0.7, rely=0.2)
        b2.config(image=tagImage)
        b2.image = tagImage
        b3 = tk.Button(self, text="Poison", command=lambda: self.actualizaValorSigue("Poison"))
        b3.place(relx=0.1, rely=0.6)
        b3.config(image=poisonImage)
        b3.image = poisonImage
        b4 = tk.Button(self, text="XXXX", command=lambda: self.actualizaValorSigue("XXXX"))
        b4.place(relx=0.7, rely=0.6)
        b4.config(image=poisonImage)
        b4.image = poisonImage

    def actualizaValorSigue(self, text):
        self.controller.shared_data["problema"] = text
        if(text == "Tigre" or text == "Poison"):
            self.controller.show_frame("BudgetTries")
        elif(text == "Tag"):
            self.controller.show_frame("Tries")
        else:
            self.controller.show_frame("PageOne")

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
        b1 = tk.Button(self, text="POMCP", font=controller.button_font, command=lambda: self.actualizaValorSigue("POMCP"))
        b1.place(relx=0.1, rely=0.4)
        b2 = tk.Button(self, text="PBVI", font=controller.button_font, command=lambda: self.actualizaValorSigue("PBVI"))
        b2.place(relx=0.7, rely=0.4)

    def actualizaValorSigue(self, text):
        self.controller.shared_data["algoritmo"] = text
        self.controller.show_frame("PageTwo")

class Tries(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Insert a budget", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        entry = tk.Entry(self, textvariable=self.controller.shared_data["intentos"])
        entry.place(relx=0.4, rely=0.5)
        entry.insert(0, "Insert tries (1-n)")

        b1 = tk.Button(self, text="Algorithms", font=controller.button_font_small, command=lambda: controller.show_frame("PageOne"))
        b1.place(relx=0.4, rely=0.6)


class BudgetTries(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Insert budget and tries", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        entryBudget = tk.Entry(self, textvariable=self.controller.shared_data["presupuesto"])
        entryBudget.place(relx=0.4, rely=0.3)
        entryBudget.insert(0, "Insert budget (1-n)")

        entryTries = tk.Entry(self, textvariable=self.controller.shared_data["intentos"])
        entryTries.place(relx=0.4, rely=0.5)
        entryTries.insert(0, "Insert number of tries (1-n)")

        b1 = tk.Button(self, text="Algorithms", font=controller.button_font_small, command=lambda: controller.show_frame("PageOne"))
        b1.place(relx=0.4, rely=0.6)


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
        b1 = tk.Button(self, text="Interactive execution", font=controller.button_font_small, command=lambda: self.actualizaValorSigue("Iterativo"))
        b1.place(relx=0.1, rely=0.4)
        b2 = tk.Button(self, text="Silent execution", font=controller.button_font_small, command=lambda: self.actualizaValorSigue("Silencioso"))
        b2.place(relx=0.7, rely=0.4)
        b3 = tk.Button(self, text="Benchmark execution", font=controller.button_font_small, command=lambda: self.actualizaValorSigue("Benchmark"))
        b3.place(relx=0.35, rely=0.7)

    def actualizaValorSigue(self, text):
        self.controller.shared_data["modoEjecucion"] = text
        #self.controller.show_frame("PageThree")
        EjecutaPOMDP.run(self)

class EjecutaPOMDP(tk.Frame):
    def run(self):
        problema = self.controller.shared_data["problema"]
        algoritmo = self.controller.shared_data["algoritmo"]
        budget = self.controller.shared_data["presupuesto"].get()
        max_play = self.controller.shared_data["intentos"].get()
        modo = self.controller.shared_data["modoEjecucion"]

        if(problema == "Tigre" or problema == "Veneno" ):
            if(budget =="Insert budget (1-n)"):
                budget = float('inf')

            if (max_play == "Insert number of tries (1-n)"):
                max_play = 100
        elif(problema == "LaserTag"):
            if (max_play == "Insert number of tries (1-n)"):
                max_play = 100

        parser = argparse.ArgumentParser()
        parser.add_argument('--config', type=str, default=algoritmo)
        parser.add_argument('--env', type=str, default=problema + ".POMDP")
        parser.add_argument('--budget', type=float, default=budget)
        parser.add_argument('--snapshot', type=bool, default=False)
        parser.add_argument('--logfile', type=str, default=None)
        parser.add_argument('--random_prior', type=bool, default=False)
        parser.add_argument('--max_play', type=int, default=max_play)

        args = vars(parser.parse_args())
        params = RunnerParams(**args)

        with open(params.algo_config) as algo_config:
            algo_params = json.load(algo_config)
            runner = PomdpRunner(params)

            runner.run(modo, problema, **algo_params)

class PageThree(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Output", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page", command=lambda: controller.show_frame("StartPage"))
        button.pack()

        txt = tk.Text(self, width=40, height=10)
        txt.insert(tk.END, 'HOLA')
        txt.pack()


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()