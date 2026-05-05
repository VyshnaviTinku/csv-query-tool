import pandas as pd
import numpy as np

def load_csv(file_path):
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        raise Exception(f"Error loading CSV: {e}")


def apply_filters(df, filters):
    for f in filters:
        if "=" not in f:
            raise ValueError(f"Invalid filter format: {f}. Use col=value")

        col, val = f.split("=", 1)

        if col not in df.columns:
            raise ValueError(f"Column not found: {col}")

        df = df[df[col].astype(str) == val]

    return df


def compute_all_stats(df):
    results = {}

    numeric_cols = df.select_dtypes(include=[np.number]).columns

    if len(numeric_cols) == 0:
        return {"message": "No numeric columns found"}

    for col in numeric_cols:
        series = df[col].dropna()

        if len(series) == 0:
            continue

        results[col] = {
            "mean": float(series.mean()),
            "min": float(series.min()),
            "max": float(series.max()),
            "sum": float(series.sum()),
            "count": int(series.count())
        }

        # Smart mode handling
        mode_vals = series.mode()

        if len(mode_vals) == 0:
            results[col]["mode"] = None
        elif len(mode_vals) > 5:
            results[col]["mode"] = "No clear mode"
        else:
            results[col]["mode"] = [float(x) for x in mode_vals.tolist()]

    return results