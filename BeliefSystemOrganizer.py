from tkinter import *


class App(Tk):

    def __init__(self):
        Tk.__init__(self)
        self.geometry("800x600")
        self.title("Bayesian Belief System Organizer")

        top_frame = Frame(self)
        top_frame.pack()

        forms = ("Simple form", "Complete Hypothesis Space")
        self.mode_buttons = {tx: Label(top_frame, text=tx, width=31, bd=10, relief=RAISED,
                                       font=("Times New Roman", 16))
                             for tx in forms}

        for col, tx in enumerate(forms):
            b = self.mode_buttons[tx]
            b.grid(row=0, column=col)

        # sfrm, cfrm = forms

        # self.mode_buttons[sfrm].bind("<Button-1>", lambda x: self._build_mainframe(x, sfrm))
        # self.mode_buttons[cfrm].bind("<Button-1>", lambda x: self._build_mainframe(x, cfrm))

        self.mainframe = None
        self.mainframe_obj = None

        Frame(self, height=15, relief=RIDGE, bg="black", bd=10).pack(fill=X, pady=10)

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


class SimpleFrame(Frame):

    def __init__(self, master, name, **kw):
        Frame.__init__(self, master, **kw)

        self.name = name
        self.belief = Simple_Belief(self, BELIEF, HYPOTHESES)  # TODO: replace these constants

        def add_top_labels():
            widgets = []
            for chain in ("Hypothesis:", "Evidence:"):
                var = self.belief.hypothesis if chain[0] == "H" else self.belief.evidence
                widgets.append(Label(self, text=chain, font=("Times New Roman", "18"),
                                     bd=5, relief=RAISED))
                widgets.append(Entry(self, textvariable=var,
                                     font=("Times New Roman", "16"), bg="white", fg="black",
                                     bd=5, relief=RAISED))
                widgets[-1].bind("<FocusOut>", self.belief.set_labels)
                widgets[-1].bind("<Return>", self.belief.set_labels)

            for wdgt in widgets:
                wdgt.pack(fill=X)

        def add_bayes_panel():
            BayesRule(self, padx=42, pady=10).pack()
            self._Members(self).pack()

        def add_control_buttons():
            cbframe = Frame(self)
            cbframe.pack()

            w = 8

            Button(cbframe, text="Update", width=w).pack(side=LEFT)
            Button(cbframe, text="Clear", width=w).pack(side=LEFT)

        add_top_labels()
        add_bayes_panel()
        add_control_buttons()

    class _Members(Frame):
        def __init__(self, master, **kw):
            Frame.__init__(self, master, **kw)
            xpnames = ("P(A)", "P(B|A)", "P(B)", "P(A|B)")
            xplanations = ("The Prior Probability of the hypothesis",
                           "The Likelyhood of the evidence given the hypothesis",
                           "The Marginal Likelyhood of the evidence",
                           "The Posterior Probability of the hypothesis, given the evidence")
            vars = self.master.belief.vars

            xpnw, xplw, varw = 8, max([len(xpl) for xpl in xplanations]) - 15, 14
            insertw = 60
            bw = 3
            rl = RIDGE
            for rown, (xpn, xpl) in enumerate(zip(xpnames, xplanations)):
                entrystate = NORMAL if rown != 3 else "readonly"
                entryfg = "black" if rown == 3 else "white"

                rown *= 2
                insert = rown + 1
                Label(self, text=xpn, width=xpnw, bd=bw, relief=rl, anchor=W, justify=LEFT
                      ).grid(row=rown, column=0)
                Entry(self, textvariable=vars[xpn][0], width=varw, state=entrystate, foreground=entryfg
                      ).grid(row=rown, column=1, sticky="ew")
                Label(self, text=xpl, width=xplw, bd=bw, relief=rl, anchor=W, justify=LEFT
                      ).grid(row=rown, column=2)

                Label(self, textvariable=vars[xpn][1], width=insertw, relief=rl, anchor=W, justify=LEFT
                      ).grid(row=insert, column=0, columnspan=3, sticky="ew")


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

        self.simple(font)

    def simple(self, font):
        font = "Times New Roman", str(font)

        Label(self, text="P(A|B) =", font=font).pack(side=LEFT)

        rightside = Frame(self)
        rightside.pack(side=LEFT)

        Label(rightside, text="P(B|A)P(A)", font=font).pack(fill=X)
        Frame(rightside, height=2, bd=1, relief=RIDGE, bg="black").pack(fill=X)
        Label(rightside, text="P(B)", font=font).pack(fill=X)


class Simple_Belief(Frame):

    def __init__(self, master, name, hname):
        Frame.__init__(self, master)

        self.name = StringVar(value=name)
        self.hypothesis = StringVar(value=hname)
        self.evidence = StringVar(value="")

        self.prior = DoubleVar()
        self.priorl = StringVar()
        self.lkh = DoubleVar()
        self.lkhl = StringVar()
        self.mlkh = DoubleVar()
        self.mlkhl = StringVar()
        self.posterior = DoubleVar()
        self.posteriorl = StringVar()

        self.vars = {
            "P(A|B)": (self.posterior, self.posteriorl),
            "P(A)": (self.prior, self.priorl),
            "P(B|A)": (self.lkh, self.lkhl),
            "P(B)": (self.mlkh, self.mlkhl),
        }

        self.set_labels(None)

    def calc_posterior(self):
        self.posterior.set(
            (self.prior.get() * self.lkh.get()) / self.mlkh.get()
        )

    def step(self):
        self.prior.set(self.posterior.get())
        self.lkh.set(0.0)
        self.mlkh.set(0.0)
        self.posterior.set(0.0)

    def clear(self):
        self.prior.set(0.0)
        self.priorl.set("")
        self.lkh.set(0.0)
        self.lkhl.set("")
        self.mlkh.set(0.0)
        self.mlkhl.set("")
        self.posterior.set(0.0)
        self.posteriorl.set("")

    def set_labels(self, event):
        hname = self.hypothesis.get()
        ename = self.evidence.get()
        prior = "What is the probability of [{}]?".format(hname)
        lkh = "What is the likelyhood of [{}] given [{}]?".format(ename, hname)
        mlkh = "What is the likelyhood of [{}]?".format(ename)
        posterior = "The probability of [{}] given [{}]?".format(hname, ename)

        self.priorl.set(prior)
        self.lkhl.set(lkh)
        self.mlkhl.set(mlkh)
        self.posteriorl.set(posterior)


BELIEF = "Subject of protector angels"
HYPOTHESES = "Someone is looking after me"
EVIDENCE = "I dodged a bullet today"

hypotheses = tuple()
evidences = tuple()

app = App()
app.mainloop()
