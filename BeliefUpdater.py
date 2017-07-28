"""Bayes-ba(ye)sed personal belief organizer"""

from utilities import *


class Evidence:

    def __init__(self, belief, name, likelyhoods=None):
        self.belief = belief
        self.likelyhoods = [0.0 for _ in range(len(belief.hypotheses))
                            ] if not likelyhoods else likelyhoods
        self.probability = 0.0  # AKA marginal likelyhoof
        self.name = name
        self.counted = False

    def __str__(self):
        chain = "******************************\nEvidence [{}]\n"
        chain += "with marginal likelyhood {}.\n".format(self.name + " ", self.probability)
        for h, lkh in zip(self.belief.hypotheses, self.likelyhoods):
            chain += "Probability given [{}]:\t{}.\n".format(h.name, lkh)
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
        for h in self.belief.hypotheses:
            prompt = "What is the likelyhood of {}\ngiven {}?\n> ".format(self.name, h.name)
            lkh = getprobability(prompt)
            likelyhoods.append(lkh)

        return likelyhoods

    def describe(self):
        print(self)


class Hypothesis:

    def __init__(self, prior=0.5, name=""):
        self.name = name
        self.prior = prior
        self.probability = prior

    def __str__(self):
        chain = "------------------------------\n"
        chain += "Hypotheses: [{}]\nProbability: {}\n".format(self.name + " ", self.probability)
        chain += "------------------------------"
        return chain


class Belief:

    def __init__(self, name, hypotheses=None):
        self.name = name
        self.hypotheses = hypotheses if hypotheses else []
        self.evidences = []
        self.describe()
        if not hypotheses:
            self.add_hypotheses()

    def add_hypotheses(self, hypotheses=None):
        if hypotheses is None:
            hypotheses = self._h_session()
            # print("DEBUG: received {} hypotheses!".format(len(hypotheses)))
        self.hypotheses = hypotheses

    def add_evidence(self):
        name, likelyhoods = self._e_session()
        self.evidences.append(Evidence(self, name, likelyhoods))
        self.update()

    def _e_session(self, name=None):
        i = len(self.evidences) + 1
        if not name:
            name = input("Name of the {}. evidence:\n> ".format(i))
        likelyhoods = []
        for hyp in self.hypotheses:
            likelyhoods.append(
                getprobability("What is the likelyhood of [{}]\ngiven [{}]?\n> "
                               .format(name, hyp.name)))

        return name, likelyhoods

    def _h_session(self):
        hypotheses = []
        while 1:
            cumulative_probability = 0.0
            i = len(self.hypotheses) + 1
            name = input("Please supply a name for the {}. hypotheses!\n> ".format(i))
            if name.lower() in ("stop", "exit", "off", "0", "") \
                    or cumulative_probability == 1.0:
                break
            prior = getprobability("Please give a prior probability for [{}]!\n> ".format(name))
            cumulative_probability += prior
            hypotheses.append(Hypothesis(prior, name))
            print()
        return hypotheses

    def update(self):
        n_hyps = len(self.hypotheses)
        priors = [h.probability for h in self.hypotheses]
        for e in self.evidences:
            if e.counted:
                print("*** [{}] already counted. Skipping! ***".format(e.name))
                continue
            if len(e.likelyhoods) == n_hyps:
                e.probability = sum([pri * lkh for pri, lkh in zip(priors, e.likelyhoods)])
            else:
                raise RuntimeError("Evidences are not up-to-date!")
            e.counted = True
            for i, h in enumerate(self.hypotheses):
                h.probability = (priors[i] * e.likelyhoods[i]) / e.probability
            print("Hyptheses have been updated!")
            for h in self.hypotheses:
                print(h)
                print()

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

    def describe(self):
        sep = "-" * 20
        print("Belief System Organizer")
        print(sep)
        print("Under examination:", self.name)
        print("Current Hypotheses:" + (" 0" if not self.hypotheses else ""))
        for h in self.hypotheses:
            print("- [{}]\nwith probability:\t{}".format(h.name, h.probability))
        print("Number of Evidences:", len(self.evidences))
        print(sep)


def initialize(name="Test"):
    system = Belief(name)
    return system
