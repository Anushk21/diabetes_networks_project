import pandas as pd
from pathlib import Path
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.metrics import classification_report
from joblib import dump
from preprocessing.feature_pipeline import make_feature_pipeline, split_X_y

BASE = Path(__file__).resolve().parents[1]

def main():
    data_path = BASE / "data" / "diabetes_sample.csv"
    models_dir = BASE / "models"
    models_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(data_path)
    X, y = split_X_y(df)

    # Feature scaling pipeline (fit on full small sample for demo purposes)
    pipe = make_feature_pipeline()
    Xt = pipe.fit_transform(X)

    # Base models
    dt = DecisionTreeClassifier(max_depth=4, random_state=42)
    svm = SVC(kernel="rbf", probability=True, gamma="scale", C=1.0, random_state=42)
    mlp = MLPClassifier(hidden_layer_sizes=(16,), max_iter=500, random_state=42)

    # Fit models
    dt.fit(Xt, y)
    svm.fit(Xt, y)
    mlp.fit(Xt, y)

    # Voting ensemble (soft voting)
    ensemble = VotingClassifier(
        estimators=[("dt", dt), ("svm", svm), ("mlp", mlp)],
        voting="soft"
    )
    ensemble.fit(Xt, y)

    # Save models and pipeline
    dump(pipe, models_dir / "feature_pipeline.joblib")
    dump(dt, models_dir / "decision_tree.joblib")
    dump(svm, models_dir / "svm.joblib")
    dump(mlp, models_dir / "mlp.joblib")
    dump(ensemble, models_dir / "ensemble_voting.joblib")

    # Simple evaluation (on training sample for demo)
    yhat = ensemble.predict(Xt)
    print(classification_report(y, yhat))

if __name__ == "__main__":
    main()
