import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="VBT 1RM Profiling", layout="centered")

st.title("Velocity-Based Training (VBT) 1RM Profiling")
st.subheader("Multi-Point Load–Velocity Method")

st.write(
    """
    This app estimates **1RM using multiple load–velocity data points**.
    A linear load–velocity profile is created and extrapolated to
    **exercise-specific velocity at 1RM (V1RM)**.
    """
)

st.divider()

# -------------------------------------------------
# Exercise-specific V1RM values
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

st.info(f"📌 Reference velocity at 1RM for **{exercise}**: **{v1rm:.2f} m/s**")

with st.expander("📊 View V1RM Reference Values"):
    st.table(
        {
            "Exercise": list(V1RM_DATA.keys()),
            "Velocity at 1RM (m/s)": list(V1RM_DATA.values())
        }
    )

st.divider()

# -------------------------------------------------
# Number of data points
# -------------------------------------------------
num_points = st.slider(
    "Number of load–velocity data points",
    min_value=2,
    max_value=8,
    value=4
)

loads = []
velocities = []

st.subheader("Enter Load–Velocity Data")

for i in range(num_points):
    col1, col2 = st.columns(2)
    with col1:
        load = st.number_input(
            f"Load {i+1} (kg)",
            min_value=1.0,
            step=2.5,
            key=f"load_{i}"
        )
    with col2:
        velocity = st.number_input(
            f"Velocity {i+1} (m/s)",
            min_value=0.05,
            step=0.01,
            format="%.2f",
            key=f"vel_{i}"
        )
    loads.append(load)
    velocities.append(velocity)

# -------------------------------------------------
# Calculate profile
# -------------------------------------------------
if st.button("Generate Load–Velocity Profile"):

    loads = np.array(loads)
    velocities = np.array(velocities)

    if len(np.unique(loads)) < 2:
        st.error("Please enter at least two different loads.")
    else:
        # Linear regression: Load = a*Velocity + b
        a, b = np.polyfit(velocities, loads, 1)

        estimated_1rm = a * v1rm + b

        st.success("Profile Results")
        st.metric("Estimated 1RM", f"{estimated_1rm:.1f} kg")
        st.metric("Slope (kg per m/s)", f"{a:.1f}")

        # -------------------------------------------------
        # Plot
        # -------------------------------------------------
        v_range = np.linspace(min(velocities) * 0.8, max(velocities) * 1.2, 100)
        load_fit = a * v_range + b

        fig, ax = plt.subplots()

        ax.scatter(velocities, loads, color="blue", label="Measured Lifts", zorder=5)
        ax.plot(v_range, load_fit, label="Load–Velocity Profile")
        ax.scatter(
            v1rm,
            estimated_1rm,
            color="red",
            label="Estimated 1RM",
            zorder=6
        )

        ax.set_xlabel("Mean Concentric Velocity (m/s)")
        ax.set_ylabel("Load (kg)")
        ax.set_title(f"{exercise}: Load–Velocity Profile")
        ax.legend()
        ax.grid(True)

        st.pyplot(fig)

        st.caption(
            "Linear load–velocity relationship assumed.\n"
            "Best practice: use 40–80% 1RM loads with maximal intent."
        )

st.divider()

st.write(
    """
    **Applied Notes**
    - Multi-point profiling improves accuracy vs single-point estimates
    - Avoid grinding reps during profiling
    - Individual V1RM calibration further improves precision
    """
)
