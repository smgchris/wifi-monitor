import subprocess
import time


def monitor():
    try:
        output = open("file.txt", "w")
        put_device_down = subprocess.call(["ifconfig", "wlp2s0", "down"])
        put_device_mon = subprocess.call(["iwconfig", "wlp2s0", "mode", "monitor"])
        put_device_up = subprocess.call(["iwconfig", "wlp2s0", "up"])
        start_device = subprocess.call(["airmon-ng", "start", "wlp2s0"])
        scanned_networks = subprocess.Popen(["airodump-ng","-w", "dumpOutput", "--output-format", "csv", "wlp2s0"], stdout=output)
        time.sleep(600)
        scanned_networks.terminate()

    except :
        print("Error:")

monitor()
