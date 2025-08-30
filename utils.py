def get_linux_version():
    import platform
    return platform.platform()

def get_hardware_version():
    import platform
    return platform.uname().machine

def get_uptime():
    import os
    return os.popen('uptime -p').read().strip()

def get_cpu_load():
    import psutil
    return psutil.cpu_percent(interval=1)

def get_cpu_temperature():
    try:
        import psutil
        return psutil.sensors_temperatures()['coretemp'][0].current
    except Exception:
        return "N/A"

def get_memory_usage():
    import psutil
    memory = psutil.virtual_memory()
    return memory.percent

def get_swap_usage():
    import psutil
    swap = psutil.swap_memory()
    return swap.percent

def get_storage_usage():
    import psutil
    disk_usage = psutil.disk_usage('/')
    return disk_usage.percent

def get_wifi_status():
    import subprocess
    try:
        result = subprocess.check_output(['iwgetid', '-r']).decode().strip()
        return result if result else "Not connected"
    except Exception:
        return "Wi-Fi not available"

def get_server_status():
    # Placeholder for server status checks
    return "All systems operational"