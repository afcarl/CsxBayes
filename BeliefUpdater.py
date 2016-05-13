"""Bayes-ba(ye)sed personal belief organizer"""

from utilities import *


class Evidence:
    def __init__(self, belief, name, likelyhoods=None):
        self.belief = belief
        self.likelyhoods = [0.0 for _ in range(len(belief.hypotheses))
                            ] if not likelyhoods else likelyhoods
        self.probability = 0.0
        self.name = name
        self.counted = False

    def __str__(self):
        chain = """******************************
        Evidence {}
        with marginal likelyhood {}.\n""".format(self.name + " ", self.probability)
        for h, lkh in zip(self.belief.hypotheses, self.likelyhoods):
            chain += "Probability given {} is {}.\n".format(h.name, lkh)
        chain += "******************************\n"

        return chain

    def set_likelyhoods(self, likelyhoods=None):
        assert 0.0 in self.likelyhoods, "Likelyhoods already set!"
        for i, h in enumerate(self.belief.hypotheses):
            if self.likelyhoods[i] != 0.0:
                continue
            p = getprobability("What is the likelyhood of {}\ngiven {} ? > "
                           .format(self.name, h.name))
            self.likelyhoods[i] = p

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

    def describe(self):
        print(self)


class Hypothesis:
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
    def __init__(self, hypotheses=None, evidences=None):
        self.hypotheses = hypotheses if hypotheses else []
        self.evidences = evidences if evidences else []

    def add_hypothesis(self, hypothesis=None):
        if hypothesis is None:
            hypothesis = self._h_session()

        self.hypotheses.append(hypothesis)

    def add_evidence(self, name, likelyhoods=None):
        self.evidences.append(Evidence(self, name, likelyhoods))

    def _h_session(self):
        i = len(self.hypotheses) + 1
        name = input("Please supply a name for the {}. hypotheses!\n> ".format(i))
        prior = getprobability("Please give a prior probability for {}!\n> ".format(name))
        hypothesis = Hypothesis(prior, name)
        return hypothesis

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

    def remove_evidence(self, name):
        self.evidences = [e for e in self.evidences if e.name != name]
        self.update()


if __name__ == '__main__':
    system = Belief()
