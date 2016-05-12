"""Bayes-ba(ye)sed personal belief updater"""


class Evidence:
    def __init__(self, belief: Belief, name=""):
        self.belief = belief
        self.likelyhoods = [0.0 for _ in range(len(belief.hypotheses))]
        self.probability = 0.0
        self.name = name

    def update(self, likelyhoods=None):
        if sum(likelyhoods) > 0.0:
            v = input("Warning! Are you sure you want to reset the likelyhoods of {}?"
                      .format(self.name))
            if v[0].lower() not in ("y", "i", "1"):
                return
        if not likelyhoods:
            likelyhoods = self.session()
        self.likelyhoods = likelyhoods

    def session(self):
        likelyhoods = []
        no_hyps = len(self.belief.hypotheses)
        for _ in range(no_hyps):
            likelyhood = -1.0
            while likelyhood < 0.0:
                chain = "What is the likelyhood of\n[{}]\ngiven [{}]?\n> "
                try:
                    likelyhood = float(input(chain))
                except ValueError:
                    likelyhood = -1.0
                if likelyhood > 1.0:
                    likelyhood = -1.0
            likelyhoods.append(likelyhood)

        assert len(likelyhoods) == no_hyps

        return likelyhoods

    def __str__(self):
        chain = """******************************
        Evidence {}
        with marginal likelyhood {}.
        ******************************""".format(self.name + " ", self.probability)
        return chain


class Hypotheses:
    def __init__(self, prior=0.5, name=""):
        self.name = name
        self.prior = prior
        self.probability = prior

    def __str__(self):
        chain = """------------------------------
        Hypotheses: {}
        Probability: {}
        ------------------------------""".format(self.name + " ", self.probability)
        return chain


class Belief:
    def __init__(self):
        self.hypotheses = []
        self.evidences = []

    def update(self):
        for e in self.evidences:
            e.update()

        for h in self.hypotheses:
            for e in self.evidences:
                h.probability *= e.likelyhood / e.marg_likelíhood

    def squash(self):
        ps = [h.probability for h in self.hypotheses]
        if sum(ps) == 1.0:
            return
        mx = max(ps)
        mn = min(ps)
        for lkh, h in zip(ps, self.hypotheses):
            h.likelyhood = ((lkh - mn) / (mx - mn))

    def add_evidence(self, name):
        self.evidences.append(Evidence(self, name))
        self.update()

    def remove_evidence(self, evidence: Evidence):
        self.evidences.remove(evidence)
        self.update()
