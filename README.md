# Real-Time OS Resource Monitor Dashboard

A live **Operating System Resource Monitor Dashboard** built using **Python**, **Streamlit**, and **psutil**.  
This project displays real-time system statistics such as CPU usage, RAM usage, disk usage, network activity, battery status, running processes, operating system information, and system uptime.

---

## Project Overview

The main objective of this project is to demonstrate how an operating system monitors and manages system resources.  
The dashboard collects live resource data from the system and presents it in a clean, interactive web interface.

This project was developed as part of an **Operating System Mini Project / Innovation Activity**.

---

## Features

### Live Resource Monitoring

- Real-time CPU usage
- Real-time RAM usage
- Disk usage statistics
- Network data sent and received
- Battery information
- System uptime
- Operating system details
- Running process monitoring

### Visual Dashboard

- Live CPU usage graph
- Live RAM usage graph
- Live disk usage graph
- Live network usage graph
- Metric cards for quick overview
- Auto-refresh functionality
- Adjustable refresh rate
- Dark dashboard interface

### Warning System

The dashboard displays warnings when:

- CPU usage is very high
- RAM usage is very high
- Disk usage is near full
- Battery level is low

Operating System Concepts Demonstrated

This project demonstrates several core Operating System concepts:

1. CPU Management

The dashboard shows how much processing power is currently being used by running programs.

2. Memory Management

RAM usage shows how the operating system allocates memory to active processes.

3. Storage Management

Disk usage shows how storage resources are occupied and managed.

4. Process Management

The process table displays currently running processes along with their CPU and memory usage.

5. Network Monitoring

The dashboard shows data sent and received through the system network interface.

6. System Uptime

System uptime shows how long the operating system has been running since the last boot.

Dashboard Sections
Main Metrics

Displays quick real-time values for:

CPU usage
RAM usage
Disk usage
Battery percentage
System Warnings

Displays alerts when system resource usage crosses safe limits.

Operating System Information

Displays:

Operating system name
OS release
OS version
machine type
processor information
Python version
boot time
uptime
Live Usage Graphs

Displays live graphs for:

CPU usage over time
RAM usage over time
disk usage over time
network data sent and received
Detailed Resource Information

Displays detailed CPU, RAM, disk, and network information.

Process Monitoring

Displays top running processes sorted by CPU and memory usage.

Learning Outcomes

After completing this project, I learned:

How operating systems monitor hardware resources
How CPU, RAM, disk, and network usage can be tracked
How Python can access system-level information using psutil
How to build a live dashboard using Streamlit
How process monitoring works in an operating system
How system uptime and boot time are calculated
How cloud deployment differs from local execution
Future Enhancements

Possible improvements:

Add CPU temperature monitoring for supported systems
Add process search and filtering
Add export report as CSV
Add graphical comparison between CPU and RAM usage
Add login authentication
Add historical data storage
Add Docker support
Add custom alert thresholds

License

This project is created for educational purposes as part of an Operating System mini project.


