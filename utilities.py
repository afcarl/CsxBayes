"""Some utilities for the Bayesian belief organizer"""


def getint(prompt: str) -> int:
    while 1:
        n = input(prompt)
        try:
            n = int(n)
        except ValueError:
            n = 0
        if n < 0:
            n = 0
        if n:
            return n


def getprobability(prompt: str) -> float:
    p = input(prompt)
    try:
        p = float(p)
    except ValueError:
        p = -1
    if p > 1.0:
        p = -1
    elif p < 0:
        p = -1
    if p != -1:
        return p
    else:
        print("Invalid number for probability! Assuming 0.5...")
        return 0.5


def bayes(prior: float, lkh: float, mlkh: float) -> float:
    if not valid(prior, lkh, mlkh):
        raise TypeError("Please supply valid probability values! [0.0, 1.0]")
    return (prior * lkh) / mlkh


def valid(*args) -> bool:
    """Returns True if every supplied argument is of type <float> and
    falls between 0.0 and 1.0 (it is a valid measure of probability)"""
    ok = True
    if not all([isinstance(x, float) for x in args]):
        ok = False
    if not all([0.0 < x < 1.0 for x in args]):
        ok = False
    return ok