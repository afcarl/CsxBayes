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
