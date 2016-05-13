from tkinter import *


class App(Tk):
    def __init__(self):
        Tk.__init__(self, screenName="Bayesian Belief System Organizer")
        self.belief = StringVar()
        self.geometry("800x600")
        self.hbuttons = []
        self.build_gui()

    def build_gui(self):
        Label(self, text="Belief System Organizer", font=18).pack(fill=X)
        panels = Frame(self)
        panels.pack()

        leftpanel = Frame(self, bd=3, relief=RAISED)
        leftpanel.pack(side=LEFT, fill=BOTH)

        rightpanel = Frame(self, bd=3, relief=RAISED)
        rightpanel.pack(side=LEFT, fill=BOTH)

        self.hbuttons = [Label(leftpanel, text=h, bd=2, relief=RIDGE, anchor=W) for h in hypotheses]
        for hb in self.hbuttons:
            hb.pack(fill=X)





hypotheses = ("B effs SB", "B does not eff SB")


App().mainloop()
