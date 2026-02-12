import matplotlib.pyplot as plt
import statistics


def plot_measure_of_central_tendency():
    # 1. Sample Dataset: Student Ages
    ages = [20, 22, 21, 23, 22, 20, 20, 23, 22, 24, 21, 20, 25, 20, 22]

    # 2. Calculate Mean, Median, Mode
    mean_age = statistics.mean(ages)
    median_age = statistics.median(ages)
    mode_age = statistics.mode(ages)

    print(f"Student Age Statistics:")
    print(f"Mean: {mean_age:.2f}")
    print(f"Median: {median_age}")
    print(f"Mode: {mode_age}")

    # 3. Plotting
    plt.figure(figsize=(10, 6))

    # Create histogram
    plt.hist(
        ages,
        bins=range(min(ages), max(ages) + 2),
        edgecolor="black",
        color="skyblue",
        alpha=0.7,
        align="left",
    )

    # Add vertical lines for mean, median, mode
    plt.axvline(
        mean_age,
        color="red",
        linestyle="dashed",
        linewidth=2,
        label=f"Mean: {mean_age:.2f}",
    )
    plt.axvline(
        median_age,
        color="green",
        linestyle="dotted",
        linewidth=2,
        label=f"Median: {median_age}",
    )
    plt.axvline(
        mode_age,
        color="purple",
        linestyle="dashdot",
        linewidth=2,
        label=f"Mode: {mode_age}",
    )

    # Labels and Title
    plt.title("Student Age Distribution", fontsize=15)
    plt.xlabel("Age")
    plt.ylabel("Number of Students")
    plt.xticks(range(min(ages), max(ages) + 1))
    plt.legend()
    plt.grid(axis="y", alpha=0.5)

    # Show plot
    plt.show()
