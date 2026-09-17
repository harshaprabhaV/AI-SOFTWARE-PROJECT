import numpy as np


# ============================================================
# RESOURCE PRESSURE
# ============================================================

def calculate_resource_pressure(
    cpu_usage,
    memory_usage,
    disk_usage
):

    cpu = np.clip(float(cpu_usage), 0, 100)
    memory = np.clip(float(memory_usage), 0, 100)
    disk = np.clip(float(disk_usage), 0, 100)

    pressure = (
        0.4 * (cpu / 100.0) +
        0.3 * (memory / 100.0) +
        0.3 * (disk / 100.0)
    )

    return round(
        float(np.clip(pressure, 0, 1)),
        6
    )


# ============================================================
# RESOURCE ISSUES
# ============================================================

def identify_resource_issues(
    cpu_usage,
    memory_usage,
    disk_usage
):

    issues = []

    if float(cpu_usage) > 80:
        issues.append("HIGH_CPU")

    if float(memory_usage) > 80:
        issues.append("HIGH_MEMORY")

    if float(disk_usage) > 80:
        issues.append("HIGH_DISK")

    return issues


# ============================================================
# OPTIMIZATION RISK
# ============================================================

def calculate_optimization_risk(
    anomaly_risk,
    memory_leak_risk,
    resource_pressure
):

    risk = (
        0.5 * float(anomaly_risk) +
        0.3 * float(memory_leak_risk) +
        0.2 * float(resource_pressure)
    )

    return round(
        float(np.clip(risk, 0, 1)),
        6
    )


# ============================================================
# RECOMMENDATIONS
# ============================================================

def generate_recommendations(
    cpu_usage,
    memory_usage,
    disk_usage,
    anomaly_risk,
    memory_leak_risk
):

    recommendations = []

    cpu_usage = float(cpu_usage)
    memory_usage = float(memory_usage)
    disk_usage = float(disk_usage)
    anomaly_risk = float(anomaly_risk)
    memory_leak_risk = float(memory_leak_risk)

    if cpu_usage > 80:
        recommendations.append(
            "Scale CPU resources"
        )

    if memory_usage > 80:

        if memory_leak_risk > 0.70:

            recommendations.append(
                "Investigate possible memory leak"
            )

        else:

            recommendations.append(
                "Increase memory allocation"
            )

    if disk_usage > 80:

        recommendations.append(
            "Optimize disk usage"
        )

    if anomaly_risk > 0.70:

        recommendations.append(
            "Investigate abnormal runtime behaviour"
        )

    if not recommendations:

        recommendations.append(
            "No optimization required"
        )

    return recommendations


# ============================================================
# COMPLETE OPTIMIZATION
# ============================================================

def optimize_runtime(
    cpu_usage,
    memory_usage,
    disk_usage,
    anomaly_risk,
    memory_leak_risk
):

    resource_pressure = calculate_resource_pressure(
        cpu_usage,
        memory_usage,
        disk_usage
    )

    issues = identify_resource_issues(
        cpu_usage,
        memory_usage,
        disk_usage
    )

    optimization_risk = calculate_optimization_risk(
        anomaly_risk,
        memory_leak_risk,
        resource_pressure
    )

    recommendations = generate_recommendations(
        cpu_usage,
        memory_usage,
        disk_usage,
        anomaly_risk,
        memory_leak_risk
    )

    if optimization_risk >= 0.70:
        level = "HIGH"

    elif optimization_risk >= 0.40:
        level = "MEDIUM"

    else:
        level = "LOW"

    return {
        "resource_pressure": resource_pressure,
        "resource_pressure_percent": round(
            resource_pressure * 100,
            2
        ),
        "resource_issues": issues,
        "optimization_risk": optimization_risk,
        "optimization_level": level,
        "recommendations": recommendations
    }