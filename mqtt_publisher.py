import paho.mqtt.client as mqtt
import psutil
import platform
from time import sleep
from pathlib import Path
import time

# Secrets read from devices
# node = Path('/.kubeedge_app_secrets/node.secret').read_text()
# port = int(Path('/.kubeedge_app_secrets/mqtt_port.secret').read_text())
# port = int(Path('/.kubeedge_app_secrets/mqtt_port.secret').read_text())
import socket

print(socket.gethostname())

node = 'test'
if socket.gethostname() == 'raspberrypi4':
    port = 1883
elif socket.gethostname() == 'raspberrypi3':
    port = 1884
else:
    port = 1883

# Send mosquitto messages through docker network
mqttBroker = "172.17.0.1"
client = mqtt.Client("device")
client.connect(mqttBroker, port)

while True:
    # Hardware info
    plat = platform.platform()
    arch = platform.machine()
    system = platform.system()

    # Temperature
    temp = psutil.sensors_temperatures()["cpu_thermal"][0].current
    # Memory
    total_mem = psutil.virtual_memory().total * 10**-9 # GB
    used_mem = psutil.virtual_memory().used * 10**-9 # GB
    perc_mem = psutil.virtual_memory().percent
    # CPU
    cpu = psutil.cpu_percent(interval=1)
    # Disk
    total_disk = psutil.disk_usage('/').total * 10**-9 # GB
    used_disk = psutil.disk_usage('/').used * 10**-9 # GB
    perc_disk = psutil.disk_usage('/').percent

    client.publish("data/TEMPERATURE", temp)
    print("Just published " + str(temp) + " to Topic TEMPERATURE from " + node)

    client.publish("data/MEMORY/total", total_mem)
    client.publish("data/MEMORY/used", used_mem)
    client.publish("data/MEMORY/perc", perc_mem)
    print("Just published " + str(total_mem) + " to Topic MEMORY from " + node)
    print("Just published " + str(used_mem) + " to Topic MEMORY from " + node)
    print("Just published " + str(perc_mem) + " to Topic MEMORY from " + node)

    client.publish("data/CPU", cpu)
    print("Just published " + str(cpu) + " to Topic CPU from " + node)

    client.publish("data/DISK/total", total_disk)
    client.publish("data/DISK/used", used_disk)
    client.publish("data/DISK/perc", perc_disk)
    print("Just published " + str(total_disk) + " to Topic DISK from " + node)
    print("Just published " + str(used_disk) + " to Topic DISK from " + node)
    print("Just published " + str(perc_disk) + " to Topic DISK from " + node)

    client.publish("data/HARDWARE/plat", plat)
    client.publish("data/HARDWARE/arch", arch)
    client.publish("data/HARDWARE/sys", system)
    print("Just published " + str(plat) + " to Topic HARDWARE from " + node)
    print("Just published " + str(arch) + " to Topic HARDWARE from " + node)
    print("Just published " + str(system) + " to Topic HARDWARE from " + node)

    time.sleep(10)
