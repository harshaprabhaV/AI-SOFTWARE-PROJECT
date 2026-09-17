# 🤖 AI Software Reliability & Optimization System

An AI-powered software reliability platform that continuously analyzes application runtime behaviour to detect anomalies, predict failure risk, identify memory-growth risk, understand service dependencies, and generate optimization recommendations.

---

## 🚀 Key Features

### 1. Failure Prediction
Uses machine learning to analyze runtime behaviour and estimate whether the system is approaching an abnormal state.

### 2. Anomaly Detection
Detects unusual runtime patterns using Isolation Forest based on CPU, memory, disk usage and temporal behaviour.

### 3. Memory Leak Risk Detection
Analyzes memory pressure, memory trends and growth patterns to identify potential memory-related reliability issues.

### 4. Dependency Intelligence
Analyzes service dependencies and estimates the potential downstream impact of a service failure.

### 5. Self-Optimization
Combines runtime pressure, anomaly risk and memory risk to generate AI-driven optimization recommendations.

### 6. Live Runtime Monitoring
Collects real-time CPU, memory, disk and process information from the running environment.

### 7. Interactive Dashboard
Streamlit provides a visual interface for monitoring system health, risks, dependencies and recommendations.

---

## 🏗️ Architecture

```text
                    Docker Runtime
                         │
                         ▼
                Runtime Metrics
                         │
                         ▼
                    FastAPI
                         │
             ┌───────────┴───────────┐
             ▼                       ▼
       prediction.py          optimization.py
             │                       │
      ┌──────┼──────┐                │
      ▼      ▼      ▼                ▼
   Anomaly Failure Memory       Optimization
   Detection Risk   Risk           Engine
      │      │      │                │
      └──────┴──────┴────────────────┘
                         │
                         ▼
                 Streamlit Dashboard
                 