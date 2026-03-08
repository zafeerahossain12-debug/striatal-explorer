# upgraded app.py
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------
# Page setup
# -----------------
st.set_page_config(page_title="Striatal Explorer", layout="wide")
st.title("Striatal Explorer App")
st.write("""
Interactive **conceptual simulation** of striatal network behavior under noise and assumptions.  
**Note:** This is exploratory; not biologically validated.
""")

# -----------------
# Sidebar Inputs
# -----------------
st.sidebar.header("Simulation Parameters")

noise_level = st.sidebar.slider(
    "Network Noise (σ)", 0.0, 1.0, 0.3, step=0.01,
    help="Simulated network noise; higher = more variability."
)

task = st.sidebar.selectbox(
    "Sensory/Motor Task",
    ["Visual", "Auditory", "Motor"]
)

assumption = st.sidebar.radio(
    "Assumption Mode",
    ["Hard Prohibition", "Conditional Suppression"],
    help="Hard Prohibition caps activation; Conditional Suppression allows higher activity."
)

# -----------------
# Striatal Calculations (Conceptual)
# -----------------
np.random.seed(42)  # reproducibility

# Task-specific baseline activation
if task == "Visual":
    baseline = 0.3 + 0.4 * np.sin(np.linspace(0, 3*np.pi, 100))
elif task == "Auditory":
    baseline = 0.5 + 0.3 * np.cos(np.linspace(0, 2*np.pi, 100))
else:  # Motor
    baseline = 0.2 + 0.6 * np.abs(np.sin(np.linspace(0, 2*np.pi, 100)))

# Add Gaussian noise
noise = np.random.normal(0, noise_level, size=baseline.shape)
activation = baseline + noise  # Equation: A_i = B_i + N_i

# Apply assumption capping
if assumption == "Hard Prohibition":
    activation = np.clip(activation, 0, 0.7)
else:
    activation = np.clip(activation, 0, 1.0)

# Compute error rate (deviation from baseline)
error_rate = np.abs(activation - baseline)  # Equation: E_i = |A_i - B_i|

# Heatmap: outer product of all 100 units
heatmap_data = np.outer(activation, activation)

# Summary Table
summary_table = pd.DataFrame({
    "Metric": ["Mean Error", "Max Error", "Min Error", "Network Noise"],
    "Value": [np.mean(error_rate), np.max(error_rate), np.min(error_rate), noise_level]
})

# -----------------
# Layout / Outputs
# -----------------
st.subheader("Error Rate Over Time")
st.line_chart(pd.DataFrame({"Error Rate": error_rate}))

st.subheader("Circuit Activation Heatmap (100x100 units)")
fig, ax = plt.subplots(figsize=(8,6))
sns.heatmap(heatmap_data, cmap="viridis", ax=ax)
st.pyplot(fig)

st.subheader("Summary Table")
st.table(summary_table)

# -----------------
# Conceptual Equations / Explanation
# -----------------
st.markdown("""
**Conceptual Equations:**
- `A_i = B_i + N_i` → simulated network activation = baseline + noise  
- `E_i = |A_i - B_i|` → conceptual error rate = deviation from baseline  
- `Hard Prohibition` caps activation to 0.7  
- `Conditional Suppression` allows full range up to 1.0  
- Heatmap `H = A ⊗ A` visualizes interactions among simulated units  

**Note:** This is a **conceptual simulation**, not biologically validated.
""")
