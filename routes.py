from flask import Blueprint, render_template
import psutil
import platform
import os
import subprocess

bp = Blueprint('main', __name__)

def get_system_info():
    uname = platform.uname()
    uptime = subprocess.check_output(['uptime', '-p']).decode('utf-8').strip()
    cpu_load = psutil.cpu_percent(interval=1)
    cpu_temp = get_cpu_temperature()
    memory = psutil.virtual_memory()
    swap = psutil.swap_memory()
    storage = get_storage_info()
    wifi_status = get_wifi_status()

    return {
        'linux_version': uname.system + " " + uname.release,
        'hardware_version': uname.machine,
        'uptime': uptime,
        'cpu_load': cpu_load,
        'cpu_temperature': cpu_temp,
        'memory_usage': memory.percent,
        'swap_usage': swap.percent,
        'storage_usage': storage,
        'wifi_status': wifi_status
    }

def get_cpu_temperature():
    try:
        temp = psutil.sensors_temperatures()['cpu_thermal'][0].current
        return temp
    except Exception:
        return "N/A"

def get_storage_info():
    partitions = psutil.disk_partitions()
    storage_info = {}
    for partition in partitions:
        usage = psutil.disk_usage(partition.mountpoint)
        storage_info[partition.mountpoint] = usage.percent
    return storage_info

def get_wifi_status():
    try:
        result = subprocess.check_output(['iwgetid', '-r']).decode('utf-8').strip()
        return result if result else "Not connected"
    except Exception:
        return "Not connected"

@bp.route('/')
def index():
    system_info = get_system_info()
    return render_template('index.html', system_info=system_info)