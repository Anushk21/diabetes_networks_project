from __future__ import annotations
from dataclasses import dataclass
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

NUMERIC_COLS = [
    "Pregnancies","Glucose","BloodPressure","SkinThickness","Insulin",
    "BMI","DiabetesPedigreeFunction","Age"
]

def make_feature_pipeline():
    pre = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(with_mean=True, with_std=True), NUMERIC_COLS)
        ],
        remainder="drop"
    )
    pipe = Pipeline(steps=[("pre", pre)])
    return pipe

def split_X_y(df: pd.DataFrame):
    X = df[NUMERIC_COLS].copy()
    y = df["Outcome"].astype(int).copy()
    return X, y
