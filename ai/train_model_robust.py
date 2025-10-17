# ai/train_model_robust.py
import os, json
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score, confusion_matrix

DATA_PATH = "data/combined_dataset.csv"
MODEL_OUT = "data/trained_model.pkl"
METRICS_OUT = "data/metrics.json"

def load_data(path=DATA_PATH):
    if not os.path.exists(path):
        raise FileNotFoundError(f"{path} not found. Generate it first (see scripts/generate_combined_dataset.py).")
    df = pd.read_csv(path)
    # Basic sanity checks
    if df.shape[0] < 10:
        raise ValueError("Not enough rows in dataset. Need at least ~30 rows to train a model.")
    return df

def prepare(df):
    feature_cols = ['past_runs','failures','avg_duration_s','code_change_size','failure_rate','flakiness']
    X = df[feature_cols].values
    y = df['failed_next'].values
    return X, y

def train_and_evaluate():
    df = load_data()
    X, y = prepare(df)
    # stratified split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    # scale numeric features (helps LR)
    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train)
    X_test_s = scaler.transform(X_test)

    models = {
        "logreg": LogisticRegression(max_iter=2000, solver='liblinear', random_state=42),
        "rf": RandomForestClassifier(n_estimators=200, random_state=42)
    }

    best_name = None
    best_model = None
    best_score = -1
    all_results = {}

    for name, model in models.items():
        if name == "logreg":
            model.fit(X_train_s, y_train)
            preds = model.predict(X_test_s)
        else:
            model.fit(X_train, y_train)
            preds = model.predict(X_test)

        precision = precision_score(y_test, preds, zero_division=0)
        recall = recall_score(y_test, preds, zero_division=0)
        f1 = f1_score(y_test, preds, zero_division=0)
        acc = accuracy_score(y_test, preds)
        cm = confusion_matrix(y_test, preds).tolist()

        all_results[name] = {
            "precision": round(float(precision),3),
            "recall": round(float(recall),3),
            "f1": round(float(f1),3),
            "accuracy": round(float(acc),3),
            "confusion_matrix": cm
        }

        score = f1 + 0.1*precision
        if score > best_score:
            best_score = score
            best_name = name
            if name == "logreg":
                best_model = ('logreg', model, scaler)
            else:
                best_model = ('rf', model, None)

    # Save best model and metrics
    os.makedirs('data', exist_ok=True)
    model_tag, model_obj, model_scaler = best_model
    # Save both model and scaler (if any)
    to_save = {"model_name": model_tag, "model": model_obj, "scaler": model_scaler}
    joblib.dump(to_save, MODEL_OUT)

    metrics = {
        "selected_model": model_tag,
        "metrics": all_results[model_tag],
        "all_models": all_results,
        "dataset_rows": int(df.shape[0])
    }
    with open(METRICS_OUT, 'w') as f:
        json.dump(metrics, f, indent=2)

    print("Training done. Saved model to", MODEL_OUT)
    print("Saved metrics to", METRICS_OUT)
    print(json.dumps(metrics, indent=2))

if __name__ == "__main__":
    train_and_evaluate()
