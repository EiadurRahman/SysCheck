![alt text](<assets/syscheck.png>)

# System Information Script (Windows Only)

## Overview
This Python script retrieves detailed system information, including CPU, memory, disk, GPU, battery, network, and boot time details. It outputs the information to the console and saves it to a text file.

## Features
- **CPU Info**: Retrieves processor name, physical cores, and logical cores.
- **Memory Info**: Displays RAM capacity, manufacturer, DDR type, and speed.
- **Disk Info**: Shows available storage devices and total space.
- **GPU Info**: Retrieves graphics card details.
- **Battery Info**: Displays battery percentage and estimated time left.
- **Network Info**: Shows available network interfaces and IP addresses.
- **Boot Time**: Retrieves the last boot time.
- **File Saving**: Saves the system specifications to a text file named after the device.

## Requirements
- **Operating System**: Windows (This script uses `wmic`, which is Windows-specific.)
- **Python Modules**:
  - `platform`
  - `psutil`
  - `socket`
  - `subprocess`
  - `re`
  - `datetime`

To install missing dependencies, run:
```sh
pip install psutil
```

**Compiled will be available soon**

## Usage
1. Run the script using Python:
   ```sh
   python SysCheck.py
   ```
2. The system specifications will be displayed in the terminal and saved as a text file.

## Output Example
```
System Specifications:
------------------------------
Operating System: Windows 10 (Version: 10.0.19045)
System Name: MyPC
------------------------------
Processor: Intel(R) Core(TM) i7-9700K CPU @ 3.60GHz
Physical Cores: 8
Logical Cores (Threads): 16
------------------------------
Memory Information:
------------------------------------------------------------------------------------------
Capacity (GB)  DeviceLocator  DDR Version  Manufacturer   PartNumber            Speed (MHz)
------------------------------------------------------------------------------------------
16             DIMM0         DDR4        Kingston       HX426C16FB2         2666      
16             DIMM1         DDR4        Corsair        CMK16GX4M2B         3200      
------------------------------
Storage:
C:\ - 500 GB Total
D:\ - 1 TB Total
------------------------------
Graphics Processor (GPU): NVIDIA GeForce RTX 3060
------------------------------
Battery Status: 90% Not Charging
Time Left: 120 minutes
------------------------------
Network Information:
Interface: Wi-Fi, IP: 192.168.1.10
------------------------------
Last Boot Time: 2025-02-11 08:30:45
------------------------------
Specifications saved to MyPC.txt
```

## Notes
- **Windows-Only**: The script relies on `wmic`, which is deprecated in newer Windows versions but still available in many systems.
- **Permission Issues**: Running the script with admin privileges may be required to access certain system details.



