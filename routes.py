from flask import Blueprint, render_template, jsonify
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
    cpu_freq = psutil.cpu_freq().current if psutil.cpu_freq() else "N/A"
    cpu_voltage = get_cpu_voltage()

    system_info = {
        'linux_version': uname.system + " " + uname.release,
        'hardware_version': uname.machine,
        'uptime': uptime,
        'cpu_load': cpu_load,
        'cpu_temperature': cpu_temp,
        'cpu_frequency': cpu_freq,
        'cpu_voltage': cpu_voltage,
        'memory_usage': memory.percent,
        'swap_usage': swap.percent,
        'storage_usage': storage,
        'wifi_status': wifi_status
    }
    return system_info

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

def get_cpu_voltage():
    try:
        # For Raspberry Pi, use vcgencmd if available
        result = subprocess.check_output(['vcgencmd', 'measure_volts']).decode('utf-8').strip()
        # Output is like: "volt=1.2000V"
        return result.split('=')[1] if '=' in result else result
    except Exception:
        return "N/A"

@bp.route('/')
def index():
    system_info = get_system_info()
    return render_template('index.html', system_info=system_info)

@bp.route('/api/system_info')
def api_system_info():
    system_info = get_system_info()
    return jsonify(system_info)