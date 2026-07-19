import mlflow  # Used for tracking experiments
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler


def machine_learning_life_cycle_on_iris():
    # 1. Problem Definition: Classify iris flowers into species based on features.
    # 2. Data Collection: Load the raw data.

    iris = load_iris()  # The Bunch data type in scikit-learn is a container object that extends Python dictionaries by allowing you to access its keys as object attributes.
    df = pd.DataFrame(data=iris.data, columns=iris.feature_names)
    df["species"] = iris.target_names[iris.target]

    # Data cleaning/prep (iris dataset is already clean)
    # Feature engineering (not strictly needed for iris, but conceptual step)

    # Define features (X) and target (y)
    X = df.drop("species", axis=1)
    y = df["species"]

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    # Feature Scaling (a common preprocessing step)
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    # Initialize MLflow (replace with a real MLflow tracking URI if running a server)
    mlflow.set_experiment("Iris_Classifier_Experiment")

    with mlflow.start_run():
        # 3. Model Selection: Using K-Nearest Neighbors (KNN)
        n_neighbors = 5
        model = KNeighborsClassifier(n_neighbors=n_neighbors)

        # 4. Model Training
        model.fit(X_train, y_train)

        # Log the parameter in MLflow
        mlflow.log_param("n_neighbors", n_neighbors)
        print(f"Model trained with n_neighbors={n_neighbors}")
    # 5. Model Evaluation
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    print(f"Accuracy on test set: {accuracy:.2f}")

    with mlflow.start_run():
        # Log the evaluation metric in MLflow
        mlflow.log_metric("accuracy", accuracy)
        # In a real scenario, you would also save the model as an artifact here
        # mlflow.sklearn.log_model(model, "knn_model")

    # 6. Deployment (Conceptual example of making a prediction in "production")
    def predict_species(sepal_length, sepal_width, petal_length, petal_width):
        # Preprocess the input features similar to training data
        features = scaler.transform(
            [[sepal_length, sepal_width, petal_length, petal_width]]
        )
        prediction = model.predict(features)
        return prediction[0]

    # Example prediction request
    new_data_point = [5.1, 3.5, 1.4, 0.2]
    prediction_result = predict_species(*new_data_point)
    print(f"Prediction for new data {new_data_point}: {prediction_result}")

    # 7. Monitoring & Maintenance (Conceptual)
    # In production, systems would continuously check performance metrics against a baseline
    # and trigger retraining if performance degrades due to data drift.


def main():
    print("Classify iris flowers into species based on features")
    machine_learning_life_cycle_on_iris()
