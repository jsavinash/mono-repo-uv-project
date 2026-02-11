import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import binom
import numpy as np


def coin_flips_binomial_distribution():
    np.random.seed(12)

    n_flips = 10
    p_success = 0.5
    n_trials = 10

    fair_coin_flips = binom.rvs(n=n_flips, p=p_success, size=n_trials)

    counts = pd.crosstab(index="counts", columns=fair_coin_flips)
    print(counts)

    plt.figure(figsize=(8, 5))
    pd.DataFrame(fair_coin_flips).hist(range=(-0.5, 10.5), bins=11, ax=plt.gca())
    plt.title("Binomial Distribution of 10 Coin Flips (10,000 trials)")
    plt.xlabel("Number of Heads")
    plt.ylabel("Frequency")
    plt.grid(axis="y", alpha=0.75)
    plt.show()


def main() -> None:
    print("Hello from maths!")
    coin_flips_binomial_distribution()
