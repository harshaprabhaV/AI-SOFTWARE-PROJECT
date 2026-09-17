from pathlib import Path
from collections import deque
import json
import joblib
import numpy as np


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "models"


# ============================================================
# LOAD MODELS
# ============================================================

ANOMALY_MODEL_PATH = MODEL_DIR / "anomaly_detection_model.pkl"
FAILURE_MODEL_PATH = MODEL_DIR / "failure_risk_model.pkl"

ANOMALY_FEATURES_PATH = MODEL_DIR / "anomaly_features.json"
FAILURE_FEATURES_PATH = MODEL_DIR / "failure_features.json"


if not ANOMALY_MODEL_PATH.exists():
    raise FileNotFoundError(
        f"Missing anomaly model: {ANOMALY_MODEL_PATH}"
    )

if not FAILURE_MODEL_PATH.exists():
    raise FileNotFoundError(
        f"Missing failure model: {FAILURE_MODEL_PATH}"
    )

if not ANOMALY_FEATURES_PATH.exists():
    raise FileNotFoundError(
        f"Missing anomaly feature file: {ANOMALY_FEATURES_PATH}"
    )

if not FAILURE_FEATURES_PATH.exists():
    raise FileNotFoundError(
        f"Missing failure feature file: {FAILURE_FEATURES_PATH}"
    )


anomaly_model = joblib.load(ANOMALY_MODEL_PATH)
failure_model = joblib.load(FAILURE_MODEL_PATH)


with open(ANOMALY_FEATURES_PATH, "r", encoding="utf-8") as f:
    anomaly_features = json.load(f)

with open(FAILURE_FEATURES_PATH, "r", encoding="utf-8") as f:
    failure_features = json.load(f)


# Some notebooks save feature names directly as a list,
# while others save them inside a dictionary.
if isinstance(anomaly_features, dict):
    anomaly_features = anomaly_features.get(
        "features",
        anomaly_features.get("feature_names", [])
    )

if isinstance(failure_features, dict):
    failure_features = failure_features.get(
        "features",
        failure_features.get("feature_names", [])
    )


# ============================================================
# LIVE HISTORY
# ============================================================

runtime_history = deque(maxlen=5)


# ============================================================
# UTILITY
# ============================================================

def safe_float(value, default=0.0):
    try:
        value = float(value)

        if np.isnan(value) or np.isinf(value):
            return default

        return value

    except (TypeError, ValueError):
        return default


def calculate_trend(values):
    """
    Simple linear trend using observation index.
    """

    values = list(values)

    if len(values) < 2:
        return 0.0

    x = np.arange(len(values), dtype=float)
    y = np.asarray(values, dtype=float)

    try:
        return float(np.polyfit(x, y, 1)[0])
    except Exception:
        return 0.0


# ============================================================
# FEATURE ENGINEERING
# ============================================================

def build_runtime_features(data, update_history=False):

    cpu = safe_float(data.get("cpu_usage"))
    memory = safe_float(data.get("memory_usage"))
    disk = safe_float(data.get("disk_usage"))

    if update_history:
        runtime_history.append(
            {
                "cpu": cpu,
                "memory": memory,
                "disk": disk
            }
        )

    history = list(runtime_history)

    # If this is a normal /predict request and history is empty,
    # use the supplied current observation.
    if not history:
        history = [
            {
                "cpu": cpu,
                "memory": memory,
                "disk": disk
            }
        ]

    cpu_values = [x["cpu"] for x in history]
    memory_values = [x["memory"] for x in history]
    disk_values = [x["disk"] for x in history]

    cpu_mean_5 = float(np.mean(cpu_values))
    memory_mean_5 = float(np.mean(memory_values))
    disk_mean_5 = float(np.mean(disk_values))

    cpu_std_5 = float(np.std(cpu_values))
    memory_std_5 = float(np.std(memory_values))

    if len(history) >= 2:

        cpu_change = cpu_values[-1] - cpu_values[-2]
        memory_change = memory_values[-1] - memory_values[-2]
        disk_change = disk_values[-1] - disk_values[-2]

    else:

        cpu_change = safe_float(data.get("cpu_change"))
        memory_change = safe_float(data.get("memory_change"))
        disk_change = safe_float(data.get("disk_change"))

    cpu_trend = calculate_trend(cpu_values)
    memory_trend = calculate_trend(memory_values)
    disk_trend = calculate_trend(disk_values)

    # Explicit values supplied by API take priority when present.
    if "cpu_mean_5" in data:
        cpu_mean_5 = safe_float(data["cpu_mean_5"], cpu_mean_5)

    if "cpu_std_5" in data:
        cpu_std_5 = safe_float(data["cpu_std_5"], cpu_std_5)

    if "memory_mean_5" in data:
        memory_mean_5 = safe_float(
            data["memory_mean_5"],
            memory_mean_5
        )

    if "memory_std_5" in data:
        memory_std_5 = safe_float(
            data["memory_std_5"],
            memory_std_5
        )

    if "disk_mean_5" in data:
        disk_mean_5 = safe_float(
            data["disk_mean_5"],
            disk_mean_5
        )

    if "cpu_change" in data:
        cpu_change = safe_float(
            data["cpu_change"],
            cpu_change
        )

    if "memory_change" in data:
        memory_change = safe_float(
            data["memory_change"],
            memory_change
        )

    if "disk_change" in data:
        disk_change = safe_float(
            data["disk_change"],
            disk_change
        )

    if "cpu_trend" in data:
        cpu_trend = safe_float(
            data["cpu_trend"],
            cpu_trend
        )

    if "memory_trend" in data:
        memory_trend = safe_float(
            data["memory_trend"],
            memory_trend
        )

    if "disk_trend" in data:
        disk_trend = safe_float(
            data["disk_trend"],
            disk_trend
        )

    features = {
        "cpu_usage": cpu,
        "memory_usage": memory,
        "disk_usage": disk,

        "cpu_mean_5": cpu_mean_5,
        "cpu_std_5": cpu_std_5,

        "memory_mean_5": memory_mean_5,
        "memory_std_5": memory_std_5,

        "disk_mean_5": disk_mean_5,

        "cpu_change": cpu_change,
        "memory_change": memory_change,
        "disk_change": disk_change,

        "cpu_trend": cpu_trend,
        "memory_trend": memory_trend,
        "disk_trend": disk_trend
    }

    return features


# ============================================================
# ANOMALY DETECTION
# ============================================================

def predict_anomaly(data, update_history=False):

    features = build_runtime_features(
        data,
        update_history=update_history
    )

    row = np.array(
        [
            features.get(name, 0.0)
            for name in anomaly_features
        ],
        dtype=float
    ).reshape(1, -1)

    prediction = int(anomaly_model.predict(row)[0])

    decision_score = float(
        anomaly_model.decision_function(row)[0]
    )

    # Convert Isolation Forest score into an intuitive
    # 0-1 risk indicator.
    anomaly_risk = float(
        np.clip(
            -decision_score * 5,
            0.0,
            1.0
        )
    )

    return {
        "anomaly_detected": prediction == -1,
        "anomaly_label": prediction,
        "anomaly_score": round(decision_score, 6),
        "anomaly_risk": round(anomaly_risk, 6)
    }


# ============================================================
# FAILURE RISK
# ============================================================

def predict_failure(data, update_history=False):

    features = build_runtime_features(
        data,
        update_history=update_history
    )

    row = np.array(
        [
            features.get(name, 0.0)
            for name in failure_features
        ],
        dtype=float
    ).reshape(1, -1)

    prediction = int(
        failure_model.predict(row)[0]
    )

    if hasattr(failure_model, "predict_proba"):

        probability = float(
            failure_model.predict_proba(row)[0][1]
        )

    else:

        probability = float(prediction)

    return {
        "failure_predicted": prediction == 1,
        "failure_probability": round(
            probability,
            6
        )
    }


# ============================================================
# MEMORY LEAK / GROWTH RISK
# ============================================================

def calculate_memory_leak_risk(data):

    memory = safe_float(
        data.get("memory_usage")
    )

    memory_trend = safe_float(
        data.get("memory_trend")
    )

    memory_change = safe_float(
        data.get("memory_change")
    )

    memory_pressure = np.clip(
        memory / 100.0,
        0.0,
        1.0
    )

    # Positive memory movement indicates growth.
    growth_signal = np.clip(
        (
            max(memory_trend, 0.0) +
            max(memory_change, 0.0) / 10.0
        ) / 2.0,
        0.0,
        1.0
    )

    leak_risk = (
        0.5 * growth_signal +
        0.3 * memory_pressure +
        0.2 * float(
            memory_change > 2.0
        )
    )

    leak_risk = float(
        np.clip(
            leak_risk,
            0.0,
            1.0
        )
    )

    if leak_risk >= 0.70:
        level = "HIGH"

    elif leak_risk >= 0.40:
        level = "MEDIUM"

    else:
        level = "LOW"

    return {
        "memory_pressure": round(
            float(memory_pressure),
            6
        ),
        "memory_growth_signal": round(
            float(growth_signal),
            6
        ),
        "memory_leak_risk": round(
            leak_risk,
            6
        ),
        "memory_leak_level": level
    }


# ============================================================
# COMPLETE ANALYSIS
# ============================================================

def analyze_runtime(data, update_history=False):

    anomaly = predict_anomaly(
        data,
        update_history=update_history
    )

    failure = predict_failure(
        data,
        update_history=False
    )

    memory = calculate_memory_leak_risk(
        data
    )

    return {
        "anomaly": anomaly,
        "failure": failure,
        "memory": memory
    }