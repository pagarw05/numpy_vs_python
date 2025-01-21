import streamlit as st
import numpy as np
import time
import plotly.graph_objects as go

# Functions for performance measurement
def measure_python_operation(size, operation):
    data1 = list(range(size))
    data2 = list(range(size))
    start_time = time.time()
    if operation == "Addition":
        result = [x + y for x, y in zip(data1, data2)]
    elif operation == "Multiplication":
        result = [x * y for x, y in zip(data1, data2)]
    elif operation == "Power":
        result = [x**2 for x in data1]
    return time.time() - start_time

def measure_numpy_operation(size, operation):
    data1 = np.arange(size)
    data2 = np.arange(size)
    start_time = time.time()
    if operation == "Addition":
        result = data1 + data2
    elif operation == "Multiplication":
        result = data1 * data2
    elif operation == "Power":
        result = data1**2
    return time.time() - start_time

# Streamlit App
st.title("📊 Interactive Performance Comparison: Pure Python vs. NumPy")
st.markdown(
    """
    **Explore how Pure Python compares to NumPy** in terms of performance for element-wise operations on arrays.
    Customize the array size, operation type, and observe how execution times differ.
    """
)

# Sidebar inputs
st.sidebar.header("🔧 Settings")
operation = st.sidebar.selectbox("Select Operation", ["Addition", "Multiplication", "Power"])
min_size = st.sidebar.number_input("Minimum Array Size", min_value=1000, value=10**4, step=1000, format="%d")
max_size = st.sidebar.number_input("Maximum Array Size", min_value=10000, value=10**7, step=10000, format="%d")
num_sizes = st.sidebar.slider("Number of Array Sizes", 2, 10, 5)

# Generate array sizes
array_sizes = np.logspace(np.log10(min_size), np.log10(max_size), num=num_sizes, dtype=int)

# Calculate execution times
st.subheader("📈 Calculating Execution Times...")
python_times = [measure_python_operation(size, operation) for size in array_sizes]
numpy_times = [measure_numpy_operation(size, operation) for size in array_sizes]

# Plot results using Plotly
st.subheader("📊 Performance Comparison Plot")
fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=array_sizes,
        y=python_times,
        mode="lines+markers",
        name="Pure Python",
        line=dict(color="#EF553B", width=3, dash="solid"),
        marker=dict(size=10, symbol="circle"),
    )
)
fig.add_trace(
    go.Scatter(
        x=array_sizes,
        y=numpy_times,
        mode="lines+markers",
        name="NumPy",
        line=dict(color="#636EFA", width=3, dash="dot"),
        marker=dict(size=10, symbol="square"),
    )
)

fig.update_layout(
    title=dict(
        text=f"Performance Comparison: {operation} (Pure Python vs. NumPy)",
        font=dict(size=20, color="#333333"),
    ),
    xaxis=dict(
        title="Array Size (log scale)",
        type="log",
        title_font=dict(size=16),
        tickfont=dict(size=14),
    ),
    yaxis=dict(
        title="Execution Time (log scale, seconds)",
        type="log",
        title_font=dict(size=16),
        tickfont=dict(size=14),
    ),
    legend=dict(
        title="Legend",
        title_font=dict(size=14),
        font=dict(size=12),
        bgcolor="rgba(255, 255, 255, 0.7)",
        bordercolor="gray",
        borderwidth=1,
    ),
    template="plotly_white",
    hovermode="x unified",
)
st.plotly_chart(fig, use_container_width=True)

# Display raw data
st.subheader("📋 Raw Data")
results_table = {
    "Array Size": array_sizes,
    "Pure Python (seconds)": python_times,
    "NumPy (seconds)": numpy_times,
}
st.table(results_table)

# Display insights
speedup = [python / numpy for python, numpy in zip(python_times, numpy_times)]
st.subheader("🔍 Insights")
st.markdown(
    f"""
    - NumPy was consistently faster than Pure Python across all array sizes.
    - Maximum speedup observed: **{max(speedup):.2f}x**.
    - Minimum speedup observed: **{min(speedup):.2f}x**.
    """
)