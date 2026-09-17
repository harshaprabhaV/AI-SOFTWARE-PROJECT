from pathlib import Path
from datetime import datetime
import json
import os

import psutil

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

try:
    from .prediction import (
        analyze_runtime,
        predict_anomaly,
        predict_failure,
        calculate_memory_leak_risk
    )

    from .optimization import optimize_runtime

except ImportError:

    from prediction import (
        analyze_runtime,
        predict_anomaly,
        predict_failure,
        calculate_memory_leak_risk
    )

    from optimization import optimize_runtime


# ============================================================
# PATHS
# ============================================================

PROJECT_DIR = Path(__file__).resolve().parent.parent

DEPENDENCY_PATH = (
    PROJECT_DIR /
    "data" /
    "dependency_data.json"
)

OUTPUT_DIR = (
    PROJECT_DIR /
    "outputs"
)

OUTPUT_DIR.mkdir(
    exist_ok=True
)


# ============================================================
# FASTAPI
# ============================================================

app = FastAPI(
    title="AI Software Reliability & Optimization System",
    description=(
        "AI-powered software reliability system for "
        "anomaly detection, failure risk, memory risk, "
        "dependency intelligence and optimization."
    ),
    version="1.0.0"
)


# ============================================================
# INPUT MODEL
# ============================================================

class RuntimeMetrics(BaseModel):

    cpu_usage: float = Field(
        ...,
        ge=0,
        le=100
    )

    memory_usage: float = Field(
        ...,
        ge=0,
        le=100
    )

    disk_usage: float = Field(
        ...,
        ge=0,
        le=100
    )

    cpu_mean_5: float = 0.0
    cpu_std_5: float = 0.0

    memory_mean_5: float = 0.0
    memory_std_5: float = 0.0

    disk_mean_5: float = 0.0

    cpu_change: float = 0.0
    memory_change: float = 0.0
    disk_change: float = 0.0

    cpu_trend: float = 0.0
    memory_trend: float = 0.0
    disk_trend: float = 0.0


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():

    return {
        "project": (
            "AI Software Reliability "
            "& Optimization System"
        ),
        "status": "running",
        "version": "1.0.0"
    }


# ============================================================
# PREDICTION
# ============================================================

@app.post("/predict")
def predict(metrics: RuntimeMetrics):

    data = metrics.model_dump()

    analysis = analyze_runtime(
        data,
        update_history=False
    )

    anomaly = analysis["anomaly"]
    failure = analysis["failure"]
    memory = analysis["memory"]

    optimization = optimize_runtime(
        cpu_usage=data["cpu_usage"],
        memory_usage=data["memory_usage"],
        disk_usage=data["disk_usage"],
        anomaly_risk=anomaly["anomaly_risk"],
        memory_leak_risk=memory["memory_leak_risk"]
    )

    result = {
        "timestamp": datetime.now().isoformat(),

        "runtime": {
            "cpu_usage": data["cpu_usage"],
            "memory_usage": data["memory_usage"],
            "disk_usage": data["disk_usage"]
        },

        "anomaly_detection": anomaly,

        "failure_prediction": failure,

        "memory_analysis": memory,

        "optimization": optimization
    }

    output_path = (
        OUTPUT_DIR /
        "latest_ai_decision.json"
    )

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            result,
            f,
            indent=4
        )

    return result


# ============================================================
# HEALTH ASSESSMENT
# ============================================================

@app.get("/health-assessment")
def health_assessment():

    return {
        "status": "operational",

        "modules": {
            "Anomaly Detection": "ACTIVE",
            "Failure Risk Prediction": "ACTIVE",
            "Memory Leak Risk": "ACTIVE",
            "Dependency Intelligence": "ACTIVE",
            "Self Optimization": "ACTIVE"
        }
    }


# ============================================================
# DEPENDENCIES
# ============================================================

@app.get("/dependencies")
def dependencies():

    if not DEPENDENCY_PATH.exists():

        raise HTTPException(
            status_code=404,
            detail=(
                "dependency_data.json "
                "not found"
            )
        )

    try:

        with open(
            DEPENDENCY_PATH,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    except json.JSONDecodeError:

        raise HTTPException(
            status_code=500,
            detail="Invalid dependency_data.json"
        )


# ============================================================
# LIVE RUNTIME
# ============================================================

@app.get("/runtime")
def runtime():

    return {
        "timestamp": datetime.now().isoformat(),

        "cpu_usage": round(
            psutil.cpu_percent(interval=1),
            2
        ),

        "memory_usage": round(
            psutil.virtual_memory().percent,
            2
        ),

        "disk_usage": round(
            psutil.disk_usage(
                os.path.abspath(
                    os.sep
                )
            ).percent,
            2
        ),

        "process_count": len(
            psutil.pids()
        )
    }


# ============================================================
# LIVE AI ANALYSIS
# ============================================================

@app.get("/live-analysis")
def live_analysis():

    cpu = psutil.cpu_percent(
        interval=1
    )

    memory = psutil.virtual_memory().percent

    disk = psutil.disk_usage(
        os.path.abspath(os.sep)
    ).percent

    data = {
        "cpu_usage": cpu,
        "memory_usage": memory,
        "disk_usage": disk
    }

    analysis = analyze_runtime(
        data,
        update_history=True
    )

    anomaly = analysis["anomaly"]
    failure = analysis["failure"]
    memory_result = analysis["memory"]

    optimization = optimize_runtime(
        cpu_usage=cpu,
        memory_usage=memory,
        disk_usage=disk,
        anomaly_risk=anomaly["anomaly_risk"],
        memory_leak_risk=memory_result[
            "memory_leak_risk"
        ]
    )

    anomaly_risk = anomaly["anomaly_risk"]
    resource_pressure = optimization[
        "resource_pressure"
    ]

    # --------------------------------------------------------
    # STATUS
    # --------------------------------------------------------

    if (
        anomaly_risk >= 0.70
        and resource_pressure >= 0.70
    ):

        status = "CRITICAL"

        explanation = (
            "Abnormal runtime behaviour is "
            "combined with high resource pressure."
        )

        decision = "IMMEDIATE INVESTIGATION"

    elif anomaly_risk >= 0.70:

        status = "ANOMALOUS"

        explanation = (
            "The runtime behaviour is statistically "
            "unusual and should be investigated."
        )

        decision = "INVESTIGATE ANOMALY"

    elif resource_pressure >= 0.70:

        status = "HIGH RESOURCE PRESSURE"

        explanation = (
            "System resources are under significant "
            "pressure."
        )

        decision = "OPTIMIZE RESOURCES"

    elif anomaly_risk >= 0.40:

        status = "MONITOR"

        explanation = (
            "The system shows some unusual behaviour. "
            "Continue monitoring."
        )

        decision = "CONTINUE MONITORING"

    else:

        status = "HEALTHY"

        explanation = (
            "Runtime metrics are currently within "
            "normal operating ranges."
        )

        decision = "NO ACTION REQUIRED"

    result = {

        "timestamp": datetime.now().isoformat(),

        "runtime": {
            "cpu_usage": round(cpu, 2),
            "memory_usage": round(memory, 2),
            "disk_usage": round(disk, 2),
            "process_count": len(
                psutil.pids()
            )
        },

        "anomaly_risk": anomaly_risk,

        "failure_risk": failure[
            "failure_probability"
        ],

        "memory_leak_risk": memory_result[
            "memory_leak_risk"
        ],

        "resource_pressure": resource_pressure,

        "optimization_risk": optimization[
            "optimization_risk"
        ],

        "status": status,

        "decision": decision,

        "explanation": explanation,

        "recommendations": optimization[
            "recommendations"
        ]
    }

    output_path = (
        OUTPUT_DIR /
        "latest_ai_decision.json"
    )

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            result,
            f,
            indent=4
        )

    return result