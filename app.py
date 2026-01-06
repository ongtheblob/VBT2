import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="VBT 1RM Estimator", layout="centered")

st.title("Velocity-Based Training (VBT) 1RM Estimator")
st.subheader("Exercise-Specific Velocity–Load Profiling")

st.write(
    """
    This app estimates **1RM from barbell velocity** using
    **exercise-specific velocity at 1RM (V1RM)** values
    derived from the literature.
    """
)

st.divider()

# -------------------------------------------------
# Literature-based V1RM values
# -------------------------------------------------
V1RM_DATA = {
    "Bench Press": 0.17,
    "Prone Bench Pull": 0.50,
    "Pull-Up": 0.23,
    "Seated Military Press": 0.19,
    "Lat Pulldown": 0.47,
    "Seated Cable Row": 0.40,
    "Squat": 0.30,
    "Deadlift": 0.15,
    "Hip Thrust": 0.25,
    "Leg Press": 0.21
}

exercise = st.selectbox("Select Exercise", list(V1RM_DATA.keys()))
v1rm = V1RM_DATA[exercise]

st.info(f"📌 Velocity at 1RM for **{exercise}**: **{v1rm:.2f} m/s**")

with st.expander("📊 View V1RM Reference Values"):
    st.table(
        {
            "Exercise": list(V1RM_DATA.keys()),
            "Velocity at 1RM (m/s)": list(V1RM_DATA.values())
        }
    )

st.divider()

# -------------------------------------------------
# User inputs
# -------------------------------------------------
load = st.number_input(
    "Load lifted (kg)",
    min_value=1.0,
    step=2.5
)

velocity = st.number_input(
    "Mean concentric velocity (m/s)",
    min_value=0.05,
    step=0.01,
    format="%.2f"
)

# -------------------------------------------------
# Calculation and graph
# -------------------------------------------------
if st.button("Estimate 1RM and Plot"):

    percent_1rm = (v1rm / velocity) * 100
    percent_1rm = min(percent_1rm, 105)

    estimated_1rm = load / (percent_1rm / 100)

    st.success("Estimated Results")
    st.metric("Estimated %1RM", f"{percent_1rm:.1f} %")
    st.metric("Estimated 1RM", f"{estimated_1rm:.1f} kg")

    velocities = np.linspace(v1rm, v1rm * 3.5, 50)
    percents = (v1rm / velocities) * 100

    fig, ax = plt.subplots()
    ax.plot(velocities, percents, label="Velocity–%1RM Curve")
    ax.scatter(velocity, percent_1rm, color="red", label="Your Lift", zorder=5)

    ax.set_xlabel("Mean Concentric Velocity (m/s)")
    ax.set_ylabel("Estimated %1RM")
    ax.set_ylim(0, 110)
    ax.set_title(f"{exercise}: Velocity-Based %1RM Estimation")
    ax.legend()
    ax.grid(True)

    st.pyplot(fig)

st.divider()

st.write(
    """
    **Notes**
    - V1RM values are population averages
    - Best used for daily autoregulation
    - Individual profiling improves accuracy
    """
)
