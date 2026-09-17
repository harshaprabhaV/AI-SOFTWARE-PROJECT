# 🤖 AI Software Reliability & Optimization System

> An AI-powered system for monitoring software runtime behaviour, detecting anomalies, predicting failure risk, identifying memory-growth risk, analysing service dependencies, and generating runtime optimization recommendations.

---

## 📌 Overview

Modern software systems generate large amounts of runtime data such as CPU usage, memory consumption, disk usage, application logs, error events, and service-level activity.

The **AI Software Reliability & Optimization System** analyses these signals using Machine Learning and rule-based intelligence to identify abnormal runtime behaviour and potential reliability issues.

The system combines:

- Machine Learning-based anomaly detection
- Failure-risk prediction
- Memory-growth / leak-risk analysis
- Service dependency intelligence
- Runtime resource optimization
- Live system monitoring
- AI-driven recommendations

The final application provides a **FastAPI backend** and an interactive **Streamlit dashboard**.

---

## 🎯 Problem Statement

Software failures are often preceded by changes in system behaviour such as:

- Increasing CPU utilization
- Rapid memory growth
- Increasing disk usage
- Abnormal log activity
- Increasing error pressure
- Unusual runtime patterns
- Dependency-related risks

Traditional monitoring systems mainly display metrics after problems occur.

This project aims to build an intelligent monitoring layer that can:

```text
Observe Runtime Behaviour
        ↓
Extract Features
        ↓
Detect Anomalies
        ↓
Estimate Failure Risk
        ↓
Analyse Memory Growth
        ↓
Analyse Service Dependencies
        ↓
Evaluate Resource Pressure
        ↓
Generate AI Recommendations
