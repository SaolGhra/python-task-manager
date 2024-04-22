import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import pickle
import psutil
from tkinter import Menu


# Function to get CPU usage and temperature
def get_cpu_info():
    cpu_usage = psutil.cpu_percent()
    try:
        cpu_temp = psutil.sensors_temperatures()["coretemp"][0].current
    except AttributeError:
        cpu_temp = "Not available"
    return cpu_usage, cpu_temp


# Function to get GPU usage and temperature
def get_gpu_info():
    gpu_usage = psutil.virtual_memory().percent
    try:
        gpu_temp = psutil.sensors_temperatures()["nvidia"][0].current
    except AttributeError:
        gpu_temp = "Not available"
    return gpu_usage, gpu_temp


# Function to get RAM usage
def get_ram_info():
    # Get RAM usage
    ram_usage = psutil.virtual_memory().percent

    return ram_usage


# Function to get network usage
def get_network_info():
    # Get network usage
    network_usage = (
        psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv
    )

    return network_usage


# Function to get disk utilization
def get_disk_info():
    # Get disk utilization
    disk_util = psutil.disk_usage("/").percent

    return disk_util


# Function to get process information
def get_process_info():
    # Get process information
    process_info = []
    for process in psutil.process_iter(
        ["pid", "name", "cpu_percent", "memory_percent"]
    ):
        process_info.append(
            {
                "pid": process.info["pid"],
                "name": process.info["name"],
                "cpu_percent": process.info["cpu_percent"],
                "memory_percent": process.info["memory_percent"],
            }
        )
    return process_info


# Create a Tkinter window
window = tk.Tk()
window.geometry("800x600")
window.title("Task Manager")

# Create a notebook (tab control)
notebook = ttk.Notebook(window)

# Create the tasks tab
tasks_frame = tk.Frame(notebook)
notebook.add(tasks_frame, text="Processes")
# Create a listbox in the tasks tab
processes_listbox = tk.Listbox(tasks_frame)
processes_listbox.pack()


# Function to update the list of processes
def update_processes():
    # Clear the listbox
    processes_listbox.delete(0, tk.END)

    # Get the list of processes
    processes = get_process_info()

    # Add the processes to the listbox
    for process in processes:
        processes_listbox.insert(
            tk.END, f"{process['name']} ({process['cpu_percent']}%)"
        )

    # Schedule the function to run again after 1 second
    window.after(1000, update_processes)


# Call the function to start updating the list of processes
update_processes()

# Create the details tab
details_frame = tk.Frame(notebook)
notebook.add(details_frame, text="Details")

# Pack the notebook
notebook.pack(expand=True, fill="both")

# Create a menu
menu = tk.Menu(window)
window.config(menu=menu)

# Add items to the menu
file_menu = tk.Menu(menu)
menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Exit", command=window.quit)

# Create labels to display information in the details tab
cpu_label = tk.Label(details_frame, text="CPU Usage: ")
cpu_label.pack()

cpu_temp_label = tk.Label(details_frame, text="CPU Temperature: ")
cpu_temp_label.pack()

gpu_label = tk.Label(details_frame, text="GPU Usage: ")
gpu_label.pack()

gpu_temp_label = tk.Label(details_frame, text="GPU Temperature: ")
gpu_temp_label.pack()

ram_label = tk.Label(details_frame, text="RAM Usage: ")
ram_label.pack()

network_label = tk.Label(details_frame, text="Network Usage: ")
network_label.pack()

disk_label = tk.Label(details_frame, text="Disk Utilization: ")
disk_label.pack()


# Function to update the labels
def update_labels():
    cpu_usage, cpu_temp = get_cpu_info()
    gpu_usage, gpu_temp = get_gpu_info()
    ram_usage = get_ram_info()
    network_usage = get_network_info()
    disk_usage = get_disk_info()

    cpu_label.config(text=f"CPU Usage: {cpu_usage}%")
    cpu_temp_label.config(text=f"CPU Temperature: {cpu_temp}")
    gpu_label.config(text=f"GPU Usage: {gpu_usage}%")
    gpu_temp_label.config(text=f"GPU Temperature: {gpu_temp}")
    ram_label.config(text=f"RAM Usage: {ram_usage}%")
    network_label.config(text=f"Network Usage: {network_usage}")
    disk_label.config(text=f"Disk Utilization: {disk_usage}%")


# Schedule the update_labels function to run every second
window.after(1000, update_labels)

# Start updating the labels
update_labels()

# Run the Tkinter event loop
window.mainloop()
