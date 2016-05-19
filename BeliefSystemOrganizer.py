from tkinter import *


class App(Tk):
    def __init__(self):
        Tk.__init__(self, screenName="Bayesian Belief System Organizer")
        self.geometry("800x600")
        self.title("Bayesian Belief System Organizer")

        top_frame = Frame(self)
        top_frame.pack(fill=X)

        forms = ("Simple form", "Complete Hypotheses Space")
        self.mode_buttons = {tx: Label(top_frame, text=tx, width=53, bd=10, relief=RAISED)
                             for tx in forms}

        for col, tx in enumerate(forms):
            print("Col, tx =", str((col, tx)))
            b = self.mode_buttons[tx]
            b.grid(row=0, column=col)

        # sfrm, cfrm = forms

        # self.mode_buttons[sfrm].bind("<Button-1>", lambda x: self._build_mainframe(x, sfrm))
        # self.mode_buttons[cfrm].bind("<Button-1>", lambda x: self._build_mainframe(x, cfrm))

        self.mainframe = None
        self.mainframe_obj = None

        self._build_mainframe(None, "Simple form")

    def _build_mainframe(self, event, what):
        del event  # so IDE stops whining
        if self.mainframe == what:
            return

        def kill_old():
            self.mode_buttons[self.mainframe].configure(relief=RAISED)
            self.mainframe_obj.destroy()
            self.mainframe = None
            self.mainframe_obj = None

        def create_new():
            args = (self, what)
            self.mainframe = what
            self.mainframe_obj = SimpleFrame(*args) if what[0] == "S" else ComplexFrame(*args)
            self.mode_buttons[what].configure(relief=SUNKEN)

        if self.mainframe:
            kill_old()

        create_new()
        self.mainframe_obj.pack(fill=BOTH)

    class _HypTL(Toplevel):
        def __init__(self, master, hyp):
            Toplevel.__init__(self, master)
            self.title("Hypotheses settings")

            Label(self, text="Rename {} to:".format(hyp)).pack()
            self.e = Entry(self)
            self.e.insert(0, hyp)
            self.e.pack(fill=X)
            self.e.bind("<Return>", lambda x: self._callback(event=x, hyp=hyp))
            Button(self, text="OK", command=lambda: self._callback(event=None, hyp=hyp)
                   ).pack(fill=X)

        def _callback(self, event, hyp):
            del event  # so IDE stops whining
            self.master.hbuttons[hyp].configure(text=self.e.get(), relief=RAISED)
            self.destroy()

    class _EviTL(Toplevel):
        def __init__(self, master, evi):
            Toplevel.__init__(self, master)
            self.title("Evidence settings".format(evi))

            Button(self, text="OK", command=lambda: self._callback(evi)
                   ).pack(fill=X)

        def _callback(self, evi):
            self.master.ebuttons[evi].configure(relief=RAISED)


class SimpleFrame(Frame):
    def __init__(self, master, name, **kw):
        Frame.__init__(self, master, **kw)
        self.name = name

        self.hypothesis = StringVar(value="")

        title = Label(self, text="Hypothesis:", font=("Times New Roman", "18"),
                      bd=5, relief=RAISED)
        title.bind("<Button-1>", self._gethyp)
        title.pack(fill=X)
        hyp = Label(self, textvariable=self.hypothesis, font=("Times New Roman", "16"),
                    bg="white",
                    bd=5, relief=RAISED)
        hyp.bind("<Button-1>", self._gethyp)
        hyp.pack(fill=X)

        BayesRule(self, padx=42).pack()
        self._Members(self).pack()

    def _gethyp(self, event=None):
        del event  # so IDE stops whining
        tl = self._GetHypTL(self)
        tl.grab_set()

    class _Members(Frame):
        def __init__(self, master, **kw):
            Frame.__init__(self, master, **kw)
            xpnames = ("P(A|B)", "P(A)", "P(B|A)", "P(B)")
            xplanations = ("The Posterior Probability of the hypotheses, given the evidence",
                           "The Prior Probability of the hypothesis",
                           "The Likelyhood of the evidence given the hypotheses",
                           "The Marginal Likelyhood of the evidence")
            self.xpvals = {xpn: DoubleVar() for xpn in xpnames}

            xpnw, xplw, varw = 8, max([len(xpl) for xpl in xplanations]) - 15, 14
            bw = 3
            rl = RIDGE
            for rown, (xpn, xpl) in enumerate(zip(xpnames, xplanations)):
                entrystate = NORMAL if rown else "readonly"
                Label(self, text=xpn, width=xpnw, bd=bw, relief=rl, anchor=W, justify=LEFT
                      ).grid(row=rown, column=0)
                Entry(self, textvariable=self.xpvals[xpn], width=varw, state=entrystate
                      ).grid(row=rown, column=1, sticky="ew")
                Label(self, text=xpl, width=xplw, bd=bw, relief=rl, anchor=W, justify=LEFT
                      ).grid(row=rown, column=2)

    class _GetHypTL(Toplevel):
        def __init__(self, master):
            Toplevel.__init__(self, master)
            self.title("Name Your Hypothesis")
            Label(self, text="Please supply a name for the hypotheses!", width=40).pack()
            e = Entry(self, textvariable=self.master.hypothesis)
            e.bind("<Return>", lambda x: self.destroy())
            e.pack(fill=X)
            Button(self, text="OK", command=self.destroy).pack(fill=X)


class ComplexFrame(Frame):
    def __init__(self, master, name, **kw):
        Frame.__init__(self, master, **kw)
        self.name = name

        panel_cnf = {"bd": 3, "relief": RAISED}
        bayes = BayesRule(self)
        bayes.pack()
        main_panel = Frame(self)
        main_panel.pack()
        self._Panel_display(main_panel, "Hypotheses", cnf=panel_cnf).pack(side=LEFT, fill=Y)
        self._Panel_display(main_panel, "Evidences", cnf=panel_cnf).pack(side=LEFT, fill=Y)

    class _Panel_display(Frame):
        def __init__(self, master, what, cnf=None, **kw):
            assert what in ("Hypotheses", "Evidences")
            cnf = cnf if cnf else {}
            Frame.__init__(self, master, cnf, **kw)

            self.what = what

            Label(self, text=what, font=14, bd=4, relief=RIDGE).pack(fill=X)

            self.buttons = {h: Label(self, text=h, anchor=W, width=30, bd=3, relief=RAISED)
                            for h in (hypotheses if what[0] == "H" else evidences)}

            for who, button in self.buttons.items():
                button.bind("<Button-1>", lambda x: self._callback(event=x, who=who))
                button.pack()

            Button(self, text="Add new...", font=14).pack(fill=X)

        def _callback(self, event, who):
            del event  # so IDE stops whining
            for tx, bt in self.buttons.items():
                bt.configure(relief=(RAISED if tx == who else SUNKEN))
            print("UNDEVELOPED...")


class BayesRule(Frame):
    def __init__(self, master, font=36, **kw):
        Frame.__init__(self, master, bd=3, relief=RAISED, **kw)

        font = "Times New Roman", str(font)

        Label(self, text="P(A|B) =", font=font).pack(side=LEFT)

        rightside = Frame(self)
        rightside.pack(side=LEFT)

        Label(rightside, text="P(B|A)P(A)", font=font).pack(fill=X)
        Frame(rightside, height=2, bd=1, relief=RIDGE, bg="black").pack(fill=X)
        Label(rightside, text="P(B)", font=font).pack(fill=X)


hypotheses = tuple()
evidences = tuple()

App().mainloop()
