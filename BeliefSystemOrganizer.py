from tkinter import *


class App(Tk):
    def __init__(self):
        Tk.__init__(self, screenName="Bayesian Belief System Organizer")
        self.belief = StringVar()
        self.geometry("800x600")
        self.hbuttons = []
        self.ebuttons = []
        self.build_gui()

    def build_gui(self):
        Label(self, text="Belief System Organizer", font=18).pack(fill=X)
        panels = Frame(self)
        panels.pack()

        leftpanel = Frame(self, bd=3, relief=RAISED)
        leftpanel.pack(side=LEFT)

        rightpanel = Frame(self, bd=3, relief=RAISED)
        rightpanel.pack(side=LEFT)

        w = 30

        self.hbuttons = [Label(leftpanel, text=h, anchor=W,
                               bd=2, relief=RIDGE, width=w)
                         for h in hypotheses]
        self.ebuttons = [Label(rightpanel, text=e, anchor=W,
                               bd=2, relief=RIDGE, width=w)
                         for e in evidences]
        for hb in self.hbuttons:
            hb.pack()
        for eb in self.ebuttons:
            eb.pack()


hypotheses = ("B effs SB", "B does not eff SB")
evidences = ("SB is Christian", "SB wears provocative clothes", "It is rumoured")

App().mainloop()
