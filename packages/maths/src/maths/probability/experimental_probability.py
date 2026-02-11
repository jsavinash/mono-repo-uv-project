import matplotlib.pyplot as plt
import numpy as np
from collections import Counter


def rolling_dics_bar_plot():
    # 1. Simulate the experiment
    num_trials = 10
    # Generate random integers between 1 and 6 (inclusive) for the trials
    outcomes = np.random.randint(1, 7, size=num_trials)
    print(outcomes)
    # 2. Count the frequency of each outcome
    # Counter creates a dictionary of {outcome: count}
    frequency = Counter(outcomes)
    print(frequency)
    # 3. Calculate experimental probabilities
    # Divide each count by the total number of trials
    experimental_probabilities = {
        outcome: count / num_trials for outcome, count in frequency.items()
    }
    print(experimental_probabilities)
    # Ensure all possible outcomes are present for a complete plot (optional)
    all_outcomes = range(1, 7)
    print(all_outcomes)
    probabilities = [experimental_probabilities.get(o, 0) for o in all_outcomes]
    print(probabilities)
    # 4. Plot the results
    plt.figure(figsize=(8, 6))
    plt.bar(all_outcomes, probabilities, color="skyblue", edgecolor="black")

    # Add theoretical probability for comparison
    theoretical_prob = 1 / 6
    plt.axhline(
        y=theoretical_prob,
        color="r",
        linestyle="--",
        label=f"Theoretical Probability (1/6 ≈ {theoretical_prob:.3f})",
    )

    plt.xlabel("Dice Roll Outcome", fontsize=12)
    plt.ylabel("Experimental Probability", fontsize=12)
    plt.title("Experimental Probability of Rolling a Die", fontsize=14)
    plt.xticks(all_outcomes)
    plt.ylim(0, max(probabilities) * 1.1 or 0.2)  # Adjust y-limit
    plt.legend()
    plt.grid(axis="y", alpha=0.7)

    # Display the plot
    plt.show()
