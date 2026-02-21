import os
import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# import kagglehub
# handle = 'avinashnishad/<DATASET_SLUG>'x
# kagglehub.dataset_upload(handle, local_dataset_dir, version_notes='v0.0.1', ignore_patterns=["original/", "*.tmp"])


def get_current_directory():
    script_directory = os.path.dirname(os.path.abspath(__file__))
    local_dataset_dir = f"{script_directory}/dataset"
    return local_dataset_dir


def create_pizza_price_csv():
    data = [
        ["Diameter in Inches", "Prize in Dollars"],  # Heading
        [8, 10],  # Row 1
        [10, 13],  # Row 2
        [12, 16],  # Row 3
    ]
    with open(f"{get_current_directory()}/pizza_price.csv", "w", newline="") as file:
        writer = csv.writer(file)
        # Write all rows at once
        writer.writerows(data)


def load_csv_to_numpy():
    feature_names = np.loadtxt(
        f"{get_current_directory()}/pizza_price.csv",
        dtype=str,
        delimiter=",",
        max_rows=1,
    )
    data = np.loadtxt(
        f"{get_current_directory()}/pizza_price.csv",
        dtype=int,
        delimiter=",",
        skiprows=1,
    )
    pizza_data_dict = {"feature_names": feature_names.tolist(), "data": data}
    return dict(pizza_data_dict)


def load_numpy_to_dataframe(pizza_prize):
    return pd.DataFrame(data=pizza_prize["data"], columns=pizza_prize["feature_names"])


def line_plot_pizza_price(df):
    df.plot(x="Diameter in Inches", y="Prize in Dollars", title="Pizza Price")
    plt.show()


def scatter_plot_pizza_price(df):
    a = [200, 300, 400] # size
    b = ['red', 'green', 'blue'] # color

    plt.scatter(
        x=df["Diameter in Inches"],
        y=df["Prize in Dollars"],
        s=a,
        c=b,
        alpha=0.6,
        edgecolors='w',
        linewidths=1
    )
    plt.title("Pizza Price Scatter Plot")
    plt.xlabel("Diameter in Inches")
    plt.ylabel("Prize in Dollars")
    plt.show()


def main() -> None:
    print("Simple linear regression")
    create_pizza_price_csv()
    pizza_price = load_csv_to_numpy()
    df = load_numpy_to_dataframe(pizza_price)
    #line_plot_pizza_price(df)
    scatter_plot_pizza_price(df)
