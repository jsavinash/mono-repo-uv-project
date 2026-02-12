import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm


def plot_data_range():

    # Sample data: Categories with their min and max values
    categories = ["Category A", "Category B", "Category C"]
    min_values = [10, 15, 5]
    max_values = [25, 30, 20]

    # Calculate the range (height of the bar) and the bottom position
    ranges = [max_values[i] - min_values[i] for i in range(len(categories))]
    bottoms = min_values

    plt.figure(figsize=(8, 5))
    # Plotting horizontal bars (barh)
    plt.barh(categories, ranges, left=bottoms, color="skyblue", edgecolor="black")

    plt.xlabel("Value Range")
    plt.ylabel("Categories")
    plt.title("Data Range Plot for Different Categories")
    plt.grid(axis="x", linestyle="--", alpha=0.6)
    plt.show()


def plot_variance():
    # 1. Define parameters for the individual normal distributions
    # Mean and standard deviation (std) for distribution 1
    mean1, std1 = -1, 1 
    # Mean and standard deviation for distribution 2 (different std, meaning different variance)
    mean2, std2 = 4, 3 # Changed std2 to 3 for a clear variance difference
    # Mixture weights (must sum to 1)
    w1, w2 = 0.7, 0.3 
    num_samples = 1000

    # 2. Generate samples
    samples = []
    for _ in range(num_samples):
        # Randomly choose a component based on weights
        if np.random.rand() < w1:
            # Sample from the first distribution
            sample = np.random.normal(mean1, std1)
        else:
            # Sample from the second distribution
            sample = np.random.normal(mean2, std2)
        samples.append(sample)

    samples = np.array(samples)

    # 3. Visualize the results
    plt.hist(samples, bins=50, density=True, alpha=0.6, color='g', label='Simulated Data Histogram')

    # Plot the theoretical mixture PDF for comparison
    x = np.linspace(min(samples), max(samples), 1000)
    pdf_mixture = w1 * norm.pdf(x, mean1, std1) + w2 * norm.pdf(x, mean2, std2)
    plt.plot(x, pdf_mixture, 'k-', linewidth=2, label='Theoretical Mixture PDF')

    plt.title('Mixture of Two Normal Distributions with Different Variances')
    plt.xlabel('Value')
    plt.ylabel('Density')
    plt.legend()
    plt.show()
