import os
import requests
import pandas as pd
import streamlit as st


# ============================================================
# CONFIGURATION
# ============================================================

API_URL = os.getenv(
    "API_URL",
    "http://127.0.0.1:8000"
)


st.set_page_config(
    page_title="AI Software Reliability",
    page_icon="🤖",
    layout="wide"
)


# ============================================================
# API HELPERS
# ============================================================

def get_api(endpoint):

    try:

        response = requests.get(
            f"{API_URL}{endpoint}",
            timeout=10
        )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException:

        return None


# ============================================================
# HEADER
# ============================================================

st.title(
    "🤖 AI Software Reliability & Optimization System"
)

st.caption(
    "AI-powered runtime monitoring, failure-risk "
    "analysis and optimization intelligence"
)

st.divider()


# ============================================================
# BACKEND STATUS
# ============================================================

health = get_api(
    "/health-assessment"
)

if health:

    st.success(
        "🟢 FastAPI backend connected"
    )

else:

    st.error(
        f"🔴 FastAPI backend unavailable: {API_URL}"
    )

    st.info(
        "Start FastAPI first using:\n\n"
        "python -m uvicorn backend.main:app --reload"
    )

    st.stop()


# ============================================================
# LIVE RUNTIME
# ============================================================

st.header("📊 Live Runtime")

runtime = get_api(
    "/runtime"
)

if runtime:

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "CPU Usage",
        f"{runtime['cpu_usage']:.2f}%"
    )

    c2.metric(
        "Memory Usage",
        f"{runtime['memory_usage']:.2f}%"
    )

    c3.metric(
        "Disk Usage",
        f"{runtime['disk_usage']:.2f}%"
    )

    c4.metric(
        "Processes",
        runtime["process_count"]
    )


# ============================================================
# AI ANALYSIS
# ============================================================

st.header("🧠 AI Reliability Analysis")

analysis = get_api(
    "/live-analysis"
)

if analysis:

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "System Status",
        analysis["status"]
    )

    c2.metric(
        "Anomaly Risk",
        f"{analysis['anomaly_risk'] * 100:.1f}%"
    )

    c3.metric(
        "Failure Risk",
        f"{analysis['failure_risk'] * 100:.1f}%"
    )

    c4.metric(
        "Memory Leak Risk",
        f"{analysis['memory_leak_risk'] * 100:.1f}%"
    )

    st.subheader(
        f"Decision: {analysis['decision']}"
    )

    st.info(
        analysis["explanation"]
    )


# ============================================================
# RISK BREAKDOWN
# ============================================================

if analysis:

    st.header("📈 Risk Breakdown")

    risk_df = pd.DataFrame(
        {
            "Risk": [
                "Anomaly",
                "Failure",
                "Memory Leak",
                "Resource Pressure",
                "Optimization"
            ],
            "Score": [
                analysis["anomaly_risk"] * 100,
                analysis["failure_risk"] * 100,
                analysis["memory_leak_risk"] * 100,
                analysis["resource_pressure"] * 100,
                analysis["optimization_risk"] * 100
            ]
        }
    )

    st.bar_chart(
        risk_df.set_index("Risk")
    )


# ============================================================
# OPTIMIZATION
# ============================================================

st.header("⚙️ AI Optimization")

if analysis:

    recommendations = analysis.get(
        "recommendations",
        []
    )

    for recommendation in recommendations:

        if recommendation == "No optimization required":

            st.success(
                f"✅ {recommendation}"
            )

        else:

            st.warning(
                f"⚠️ {recommendation}"
            )


# ============================================================
# DEPENDENCY INTELLIGENCE
# ============================================================

st.header("🔗 Dependency Intelligence")

dependencies = get_api(
    "/dependencies"
)

if dependencies:

    services = dependencies.get(
        "services",
        {}
    )

    rows = []

    for service, information in services.items():

        rows.append(
            {
                "Service": service,
                "Direct Dependencies":
                    information[
                        "direct_dependencies"
                    ],
                "Downstream Services":
                    information[
                        "downstream_services"
                    ],
                "Dependency Risk (%)":
                    round(
                        information[
                            "dependency_risk"
                        ] * 100,
                        2
                    )
            }
        )

    dependency_df = pd.DataFrame(
        rows
    )

    st.dataframe(
        dependency_df,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# MODULE STATUS
# ============================================================

st.header("🧩 AI Modules")

modules = health.get(
    "modules",
    {}
)

module_rows = []

for module, status in modules.items():

    module_rows.append(
        {
            "Module": module,
            "Status": status
        }
    )

module_df = pd.DataFrame(
    module_rows
)

st.dataframe(
    module_df,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# REFRESH
# ============================================================

st.divider()

if st.button(
    "🔄 Refresh Analysis"
):

    st.rerun()


st.caption(
    "AI Software Reliability & Optimization System"
)