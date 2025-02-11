import platform
import psutil
import socket
import subprocess
import re
from datetime import datetime

system_info = platform.uname()
global_dev_name = system_info.node

def get_cpu_info():
    """Retrieve CPU information."""
    try:
        cpu_name = subprocess.check_output("wmic cpu get name", shell=True).decode().split('\n')[1].strip()
    except Exception:
        cpu_name = "Could not retrieve CPU name."
    
    cpu_cores = psutil.cpu_count(logical=False)
    logical_cores = psutil.cpu_count(logical=True)
    
    return (f"Processor: {cpu_name}\n"
            f"Physical Cores: {cpu_cores}\n"
            f"Logical Cores (Threads): {logical_cores}")


def get_memory_info():
    """Retrieve detailed memory information."""
    try:
        command = "wmic memorychip get Capacity, DeviceLocator, SMBIOSMemoryType, Manufacturer, PartNumber, Speed"
        output = subprocess.run(command, capture_output=True, text=True, shell=True).stdout.strip()

        # Mapping of SMBIOSMemoryType to DDR version
        ddr_versions = {"24": "DDR3", "26": "DDR4", "34": "DDR5"}

        # Formatting header
        memory_info = "\nMemory Information:\n" + "-" * 90 + "\n"
        memory_info += f"{'Capacity (GB)':<15}{'DeviceLocator':<15}{'DDR Version':<12}{'Manufacturer':<15}{'PartNumber':<20}{'Speed (MHz)':<10}\n"
        memory_info += "-" * 90 + "\n"

        # Process output lines (skip the first line which is the header)
        lines = output.split("\n")
        headers = re.split(r'\s{2,}', lines[0].strip())  # Extract column names
        data_lines = lines[1:]

        for line in data_lines:
            parts = re.split(r'\s{2,}', line.strip())

            if len(parts) < len(headers):  # Skip incomplete lines
                continue

            # Extract values based on column names
            try:
                capacity = int(parts[headers.index("Capacity")]) // (1024**3)  # Convert bytes to GB
            except ValueError:
                capacity = "Unknown"

            device_locator = parts[headers.index("DeviceLocator")]
            smbios_memory_type = parts[headers.index("SMBIOSMemoryType")] if "SMBIOSMemoryType" in headers else "Unknown"
            manufacturer = parts[headers.index("Manufacturer")]
            part_number = parts[headers.index("PartNumber")]
            speed = parts[headers.index("Speed")]

            # Determine DDR version
            ddr_version = ddr_versions.get(smbios_memory_type, "Unknown")

            # Append formatted memory details
            memory_info += f"{capacity:<15}{device_locator:<15}{ddr_version:<12}{manufacturer:<15}{part_number:<20}{speed:<10}\n"

        return memory_info
    except Exception as e:
        return f"Failed to retrieve memory information: {e}"




def get_disk_info():
    """Retrieve disk information."""
    disk_info = psutil.disk_partitions()
    disks = []
    for disk in disk_info:
        try:
            usage = psutil.disk_usage(disk.mountpoint)
            total_space = round(usage.total / (1024 ** 3), 2)
            disks.append(f"{disk.device} - {total_space} GB Total")
        except PermissionError:
            disks.append(f"{disk.device} - Access Denied")
    return "Storage:\n" + "\n".join(disks)

def get_gpu_info():
    """Retrieve GPU information."""
    try:
        gpu_info = subprocess.check_output("wmic path win32_videocontroller get name", shell=True).decode().split('\n')[1].strip()
    except Exception:
        gpu_info = "Could not retrieve GPU information."
    return f"Graphics Processor (GPU): {gpu_info}"

def get_system_info():
    """Retrieve general system information."""
    system_info = platform.uname()
    return (f"Operating System: {system_info.system} {system_info.release} (Version: {system_info.version})\n"
            f"System Name: {system_info.node}")

def get_battery_info():
    """Retrieve battery status."""
    if hasattr(psutil, "sensors_battery"):
        battery = psutil.sensors_battery()
        if battery:
            return (f"Battery Status: {battery.percent}% {'Charging' if battery.power_plugged else 'Not Charging'}\n"
                    f"Time Left: {round(battery.secsleft / 60, 2) if battery.secsleft != psutil.POWER_TIME_UNLIMITED else 'N/A'} minutes")
        else:
            return "No Battery Information Available"
    return "Battery Sensor Not Supported"

def get_network_info():
    """Retrieve network adapter and IP information."""
    addrs = psutil.net_if_addrs()
    network_info = []
    for interface, address_list in addrs.items():
        for addr in address_list:
            if addr.family == socket.AF_INET:  # IPv4
                network_info.append(f"Interface: {interface}, IP: {addr.address}")
            elif addr.family == socket.AF_INET6:  # IPv6
                network_info.append(f"Interface: {interface}, IPv6: {addr.address}")
    return "Network Information:\n" + "\n".join(network_info)

def get_boot_time():
    """Retrieve system boot time."""
    boot_time = datetime.fromtimestamp(psutil.boot_time())
    return f"Last Boot Time: {boot_time.strftime('%Y-%m-%d %H:%M:%S')}"

def save_to_file(content, filename="system_specs"):
    """Save the output to a file."""
    try:
        with open(f"{filename}.txt", "w") as file:
            file.write(content)
        return f"Specifications saved to {filename}"
    except Exception as e:
        return f"Failed to save to file: {e}"

# Running the checks
specs = "\nSystem Specifications:\n" + "-" * 30
specs += "\n" + get_system_info()
specs += "\n" + "-" * 30
specs += "\n" + get_cpu_info()
specs += "\n" + "-" * 30
specs += "\n" + get_memory_info()
specs += "\n" + "-" * 30
specs += "\n" + get_disk_info()
specs += "\n" + "-" * 30
specs += "\n" + get_gpu_info()
specs += "\n" + "-" * 30
specs += "\n" + get_battery_info()
specs += "\n" + "-" * 30
specs += "\n" + get_network_info()
specs += "\n" + "-" * 30
specs += "\n" + get_boot_time()
specs += "\n" + "-" * 30

print(specs)
print(save_to_file(specs,global_dev_name))
