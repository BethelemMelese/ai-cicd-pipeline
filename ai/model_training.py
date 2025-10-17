import json
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score, confusion_matrix

# ----------------------
# 1. Load Dataset
# ----------------------
def load_data():
    # Example dataset (replace with real or expanded synthetic data)
    import pandas as pd
    import numpy as np

    np.random.seed(42)
    data = {
        "execution_time": np.random.uniform(0.1, 5.0, 200),
        "lines_changed": np.random.randint(0, 100, 200),
        "recent_failures": np.random.randint(0, 5, 200),
        "priority": np.random.choice([0, 1], size=200, p=[0.8, 0.2])  # 20% failures
    }

    df = pd.DataFrame(data)
    return df

# ----------------------
# 2. Train Model
# ----------------------
def train_model(df):
    X = df[["execution_time", "lines_changed", "recent_failures"]]
    y = df["priority"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=200,
        class_weight="balanced",  # ✅ handle imbalance
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_train, y_train)

    # ----------------------
    # 3. Predict with Threshold Tuning
    # ----------------------
    probs = model.predict_proba(X_test)[:, 1]
    threshold = 0.3  # ✅ more sensitive to failing tests
    y_pred = (probs >= threshold).astype(int)

    # ----------------------
    # 4. Evaluate
    # ----------------------
    precision = precision_score(y_test, y_pred, zero_division=0)
    recall = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)
    accuracy = accuracy_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred).tolist()

    metrics = {
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "accuracy": accuracy,
        "confusion_matrix": cm
    }

    with open("metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)

    # Save model
    import joblib
    joblib.dump(model, "test_model.pkl")

    print("Training complete. Metrics:", metrics)

if __name__ == "__main__":
    df = load_data()
    train_model(df)
