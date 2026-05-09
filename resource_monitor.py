import streamlit as st
import psutil
import pandas as pd
import time
import platform
from datetime import datetime


# -------------------------------------------------
# Page configuration
# -------------------------------------------------
st.set_page_config(
    page_title="OS Resource Monitor Dashboard",
    page_icon="💻",
    layout="wide"
)


# -------------------------------------------------
# Dark theme CSS
# -------------------------------------------------
st.markdown(
    """
    <style>
    /* Main app background */
    .stApp {
        background-color: #0e1117;
        color: #fafafa;
    }

    /* Main content area */
    .block-container {
        background-color: #0e1117;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #111827;
    }

    [data-testid="stSidebar"] * {
        color: #f9fafb !important;
    }

    /* Headings and text */
    h1, h2, h3, h4, h5, h6, p, span, div, label {
        color: #f9fafb !important;
    }

    /* Metric cards */
    [data-testid="stMetric"] {
        background-color: #1f2937;
        border: 1px solid #374151;
        padding: 18px;
        border-radius: 14px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.35);
    }

    [data-testid="stMetricLabel"] {
        color: #d1d5db !important;
    }

    [data-testid="stMetricValue"] {
        color: #ffffff !important;
    }

    /* Dataframe */
    [data-testid="stDataFrame"] {
        background-color: #111827;
    }

    /* Divider */
    hr {
        border-color: #374151;
    }

    /* Alerts */
    .stAlert {
        border-radius: 12px;
    }

    /* Progress bars background */
    [data-testid="stProgress"] > div > div {
        background-color: #2563eb;
    }

    /* Charts */
    [data-testid="stVegaLiteChart"] {
        background-color: #111827;
        border-radius: 12px;
        padding: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# -------------------------------------------------
# Helper functions
# -------------------------------------------------
def bytes_to_gb(value):
    return value / (1024 ** 3)


def bytes_to_mb(value):
    return value / (1024 ** 2)


def get_disk_path():
    if platform.system() == "Windows":
        return "C:\\"
    return "/"


def get_os_info():
    return {
        "Operating System": platform.system(),
        "OS Version": platform.version(),
        "OS Release": platform.release(),
        "Machine Type": platform.machine(),
        "Processor": platform.processor() if platform.processor() else "Not available",
        "Python Version": platform.python_version()
    }


def get_uptime_info():
    boot_time = datetime.fromtimestamp(psutil.boot_time())
    uptime = datetime.now() - boot_time

    return {
        "Boot Time": boot_time.strftime("%Y-%m-%d %H:%M:%S"),
        "Uptime": str(uptime).split(".")[0]
    }


def get_cpu_info():
    cpu_freq = psutil.cpu_freq()

    return {
        "CPU Usage (%)": psutil.cpu_percent(interval=0.5),
        "Physical Cores": psutil.cpu_count(logical=False),
        "Logical Cores": psutil.cpu_count(logical=True),
        "Current Frequency": round(cpu_freq.current, 2) if cpu_freq else "Not available",
        "Minimum Frequency": round(cpu_freq.min, 2) if cpu_freq else "Not available",
        "Maximum Frequency": round(cpu_freq.max, 2) if cpu_freq else "Not available"
    }


def get_memory_info():
    memory = psutil.virtual_memory()

    return {
        "Total RAM (GB)": round(bytes_to_gb(memory.total), 2),
        "Used RAM (GB)": round(bytes_to_gb(memory.used), 2),
        "Available RAM (GB)": round(bytes_to_gb(memory.available), 2),
        "RAM Usage (%)": memory.percent
    }


def get_disk_info():
    disk_path = get_disk_path()
    disk = psutil.disk_usage(disk_path)

    return {
        "Disk Path": disk_path,
        "Total Disk (GB)": round(bytes_to_gb(disk.total), 2),
        "Used Disk (GB)": round(bytes_to_gb(disk.used), 2),
        "Free Disk (GB)": round(bytes_to_gb(disk.free), 2),
        "Disk Usage (%)": disk.percent
    }


def get_network_info():
    network = psutil.net_io_counters()

    return {
        "Data Sent (MB)": round(bytes_to_mb(network.bytes_sent), 2),
        "Data Received (MB)": round(bytes_to_mb(network.bytes_recv), 2),
        "Packets Sent": network.packets_sent,
        "Packets Received": network.packets_recv
    }


def get_battery_info():
    battery = psutil.sensors_battery()

    if battery is None:
        return {
            "Battery Available": "No",
            "Battery Percentage": "Not available",
            "Charging": "Not available",
            "Time Left": "Not available"
        }

    if battery.secsleft == psutil.POWER_TIME_UNLIMITED:
        time_left = "Charging / Unlimited"
    elif battery.secsleft == psutil.POWER_TIME_UNKNOWN:
        time_left = "Unknown"
    else:
        hours = battery.secsleft // 3600
        minutes = (battery.secsleft % 3600) // 60
        time_left = f"{hours}h {minutes}m"

    return {
        "Battery Available": "Yes",
        "Battery Percentage": f"{battery.percent}%",
        "Charging": "Yes" if battery.power_plugged else "No",
        "Time Left": time_left
    }


def get_process_info(limit=10):
    processes = []

    for process in psutil.process_iter(
        ["pid", "name", "cpu_percent", "memory_percent", "status"]
    ):
        try:
            processes.append(process.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    process_df = pd.DataFrame(processes)

    if process_df.empty:
        return process_df

    process_df["cpu_percent"] = process_df["cpu_percent"].fillna(0)
    process_df["memory_percent"] = process_df["memory_percent"].fillna(0)

    process_df = process_df.sort_values(
        by=["cpu_percent", "memory_percent"],
        ascending=False
    ).head(limit)

    process_df["cpu_percent"] = process_df["cpu_percent"].round(2)
    process_df["memory_percent"] = process_df["memory_percent"].round(2)

    return process_df


def show_warning_system(cpu_usage, ram_usage, disk_usage, battery_info):
    st.subheader("System Warnings")

    warning_found = False

    if cpu_usage >= 80:
        st.warning("High CPU usage detected. Too many processes or heavy computation may be running.")
        warning_found = True

    if ram_usage >= 80:
        st.warning("High RAM usage detected. System performance may slow down.")
        warning_found = True

    if disk_usage >= 90:
        st.warning("Disk storage is almost full. Free up space to avoid performance issues.")
        warning_found = True

    if battery_info["Battery Available"] == "Yes":
        battery_percent = int(battery_info["Battery Percentage"].replace("%", ""))

        if battery_percent <= 20 and battery_info["Charging"] == "No":
            st.warning("Low battery detected. Connect charger soon.")
            warning_found = True

    if not warning_found:
        st.success("No critical system warnings detected.")


# -------------------------------------------------
# Session state for live graphs
# -------------------------------------------------
if "history" not in st.session_state:
    st.session_state.history = pd.DataFrame(
        columns=[
            "Time",
            "CPU Usage (%)",
            "RAM Usage (%)",
            "Disk Usage (%)",
            "Data Sent (MB)",
            "Data Received (MB)"
        ]
    )


# -------------------------------------------------
# Sidebar controls
# -------------------------------------------------
st.sidebar.header("Dashboard Settings")

refresh_rate = st.sidebar.slider(
    "Refresh rate in seconds",
    min_value=1,
    max_value=10,
    value=2
)

max_history = st.sidebar.slider(
    "Graph history points",
    min_value=10,
    max_value=100,
    value=30
)

show_processes = st.sidebar.checkbox("Show Process Monitoring", value=True)
show_graphs = st.sidebar.checkbox("Show Live Graphs", value=True)
auto_refresh = st.sidebar.checkbox("Enable Auto Refresh", value=True)


# -------------------------------------------------
# Main dashboard title
# -------------------------------------------------
st.title("Real-Time OS Resource Monitor Dashboard")
st.write("Live monitoring of CPU, RAM, Disk, Network, Battery, Processes and OS Information.")

st.caption(f"Last Updated: {datetime.now().strftime('%H:%M:%S')}")


# -------------------------------------------------
# Collect live system data
# -------------------------------------------------
os_info = get_os_info()
uptime_info = get_uptime_info()
cpu_info = get_cpu_info()
memory_info = get_memory_info()
disk_info = get_disk_info()
network_info = get_network_info()
battery_info = get_battery_info()


# -------------------------------------------------
# Update graph history
# -------------------------------------------------
new_row = pd.DataFrame({
    "Time": [datetime.now().strftime("%H:%M:%S")],
    "CPU Usage (%)": [cpu_info["CPU Usage (%)"]],
    "RAM Usage (%)": [memory_info["RAM Usage (%)"]],
    "Disk Usage (%)": [disk_info["Disk Usage (%)"]],
    "Data Sent (MB)": [network_info["Data Sent (MB)"]],
    "Data Received (MB)": [network_info["Data Received (MB)"]]
})

st.session_state.history = pd.concat(
    [st.session_state.history, new_row],
    ignore_index=True
)

st.session_state.history = st.session_state.history.tail(max_history)


# -------------------------------------------------
# Main metric cards
# -------------------------------------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("CPU Usage", f"{cpu_info['CPU Usage (%)']}%")
    st.progress(cpu_info["CPU Usage (%)"] / 100)

with col2:
    st.metric("RAM Usage", f"{memory_info['RAM Usage (%)']}%")
    st.progress(memory_info["RAM Usage (%)"] / 100)

with col3:
    st.metric("Disk Usage", f"{disk_info['Disk Usage (%)']}%")
    st.progress(disk_info["Disk Usage (%)"] / 100)

with col4:
    st.metric("Battery", battery_info["Battery Percentage"])


st.divider()


# -------------------------------------------------
# Warning system
# -------------------------------------------------
show_warning_system(
    cpu_info["CPU Usage (%)"],
    memory_info["RAM Usage (%)"],
    disk_info["Disk Usage (%)"],
    battery_info
)


st.divider()


# -------------------------------------------------
# OS information and uptime
# -------------------------------------------------
st.subheader("Operating System Information")

os_col1, os_col2 = st.columns(2)

with os_col1:
    st.write(f"Operating System: {os_info['Operating System']}")
    st.write(f"OS Release: {os_info['OS Release']}")
    st.write(f"OS Version: {os_info['OS Version']}")
    st.write(f"Machine Type: {os_info['Machine Type']}")

with os_col2:
    st.write(f"Processor: {os_info['Processor']}")
    st.write(f"Python Version: {os_info['Python Version']}")
    st.write(f"System Boot Time: {uptime_info['Boot Time']}")
    st.write(f"System Uptime: {uptime_info['Uptime']}")


st.divider()


# -------------------------------------------------
# Live graphs
# -------------------------------------------------
if show_graphs:
    st.subheader("Live Usage Graphs")

    graph_data = st.session_state.history.set_index("Time")

    graph_col1, graph_col2 = st.columns(2)

    with graph_col1:
        st.write("CPU Usage Over Time")
        st.line_chart(graph_data[["CPU Usage (%)"]])

    with graph_col2:
        st.write("RAM Usage Over Time")
        st.line_chart(graph_data[["RAM Usage (%)"]])

    graph_col3, graph_col4 = st.columns(2)

    with graph_col3:
        st.write("Disk Usage Over Time")
        st.line_chart(graph_data[["Disk Usage (%)"]])

    with graph_col4:
        st.write("Network Data Sent and Received")
        st.line_chart(graph_data[["Data Sent (MB)", "Data Received (MB)"]])

    st.divider()


# -------------------------------------------------
# CPU, RAM, Disk, Network details
# -------------------------------------------------
st.subheader("Detailed Resource Information")

detail_col1, detail_col2 = st.columns(2)

with detail_col1:
    st.markdown("### CPU Information")
    st.write(f"Physical Cores: {cpu_info['Physical Cores']}")
    st.write(f"Logical Cores: {cpu_info['Logical Cores']}")
    st.write(f"CPU Usage: {cpu_info['CPU Usage (%)']}%")
    st.write(f"Current Frequency: {cpu_info['Current Frequency']} MHz")
    st.write(f"Minimum Frequency: {cpu_info['Minimum Frequency']} MHz")
    st.write(f"Maximum Frequency: {cpu_info['Maximum Frequency']} MHz")

    st.markdown("### RAM Information")
    st.write(f"Total RAM: {memory_info['Total RAM (GB)']} GB")
    st.write(f"Used RAM: {memory_info['Used RAM (GB)']} GB")
    st.write(f"Available RAM: {memory_info['Available RAM (GB)']} GB")
    st.write(f"RAM Usage: {memory_info['RAM Usage (%)']}%")

with detail_col2:
    st.markdown("### Disk Information")
    st.write(f"Disk Path Monitored: {disk_info['Disk Path']}")
    st.write(f"Total Disk: {disk_info['Total Disk (GB)']} GB")
    st.write(f"Used Disk: {disk_info['Used Disk (GB)']} GB")
    st.write(f"Free Disk: {disk_info['Free Disk (GB)']} GB")
    st.write(f"Disk Usage: {disk_info['Disk Usage (%)']}%")

    st.markdown("### Network Information")
    st.write(f"Data Sent: {network_info['Data Sent (MB)']} MB")
    st.write(f"Data Received: {network_info['Data Received (MB)']} MB")
    st.write(f"Packets Sent: {network_info['Packets Sent']}")
    st.write(f"Packets Received: {network_info['Packets Received']}")


st.divider()


# -------------------------------------------------
# Battery information
# -------------------------------------------------
st.subheader("Battery Information")

battery_col1, battery_col2, battery_col3, battery_col4 = st.columns(4)

with battery_col1:
    st.metric("Battery Available", battery_info["Battery Available"])

with battery_col2:
    st.metric("Battery Percentage", battery_info["Battery Percentage"])

with battery_col3:
    st.metric("Charging", battery_info["Charging"])

with battery_col4:
    st.metric("Time Left", battery_info["Time Left"])


# -------------------------------------------------
# Process monitoring
# -------------------------------------------------
if show_processes:
    st.divider()
    st.subheader("Process Monitoring")

    process_df = get_process_info(limit=10)

    if process_df.empty:
        st.warning("No process information available.")
    else:
        process_df = process_df.rename(columns={
            "pid": "PID",
            "name": "Process Name",
            "cpu_percent": "CPU Usage (%)",
            "memory_percent": "Memory Usage (%)",
            "status": "Status"
        })

        st.dataframe(process_df, use_container_width=True)

        st.caption(
            "Processes are sorted by CPU usage first and memory usage second. "
            "Some system processes may not be visible because of operating system permission restrictions."
        )


# -------------------------------------------------
# Auto refresh
# -------------------------------------------------
if auto_refresh:
    time.sleep(refresh_rate)
    st.rerun()