import subprocess
from scapy.all import ARP, Ether, srp
import os
import getmac
from urllib import *
import urllib.request


def manufacturer():
    try:
        try:
            nam = subprocess.Popen("sudo dmidecode -s system-manufacturer", shell=True, stdout=subprocess.PIPE)
            nam = nam.stdout.readline()
            nam = nam.decode("utf-8").split()[0]
        except:
            nam = subprocess.Popen("cat /sys/devices/virtual/dmi/id/sys_vendor", shell=True, stdout=subprocess.PIPE)
            nam = nam.stdout.readline()
            nam = nam.decode("utf-8").split()[0]
    except:
        nam = "unknown"

def product_nam():
    try:
        try:
            product_name = subprocess.Popen("sudo dmidecode -s baseboard-product-name", shell=True, stdout=subprocess.PIPE)
            product_name = product_name.stdout.readline()
            product_name = product_name.decode("utf-8").split()
            product_name = " ".join(product_name)
        except:
            product_name = subprocess.Popen("cat /sys/devices/virtual/dmi/id/product_name", shell=True, stdout=subprocess.PIPE)
            product_name = product_name.stdout.readline()
            product_name = product_name.decode("utf-8").split()[0]
    except:
        product_name = "unknown"
    
def my_mac():
    try:
        MAC = getmac.get_mac_address()
    except:
        MAC = "unknown"
    return MAC


def ip_all():
    try:
        IP_host = subprocess.Popen("hostname -i", shell=True, stdout=subprocess.PIPE)
        IP_host = IP_host.stdout.readline()
        IP_host = IP_host.decode("utf-8").split()[0]
    except:
        IP_host = "unknown"
    try:
        IP_All = subprocess.Popen("hostname -I", shell=True, stdout=subprocess.PIPE)
        IP_All = IP_All.stdout.readline()
        IP_All = IP_All.decode("utf-8").split()[0]
    except:
        IP_All = "unknown"
    return IP_All


def wifi_name():
    try:
        WifiName = subprocess.Popen("iwgetid -r", shell=True, stdout=subprocess.PIPE)
        WifiName = WifiName.stdout.readline()
        WifiName = WifiName.decode("utf-8").split()
        if WifiName == []:
            os.system("sudo service network-manager restart")
            WifiName = subprocess.Popen("iwgetid -r", shell=True, stdout=subprocess.PIPE)
            WifiName = WifiName.stdout.readline()
            WifiName = WifiName.decode("utf-8").split()[0]
        else:
            WifiName = WifiName[0]
    except:
        WifiName = "unknown"
    return WifiName


try:
    DNSs = os.popen("nmcli dev show | grep DNS | awk '{print $2}'")
    DNSs = DNSs.read().split("\n")
    num = 0
    for res in DNSs:
        if res == "":
            pass
        else:
            num += 1
            if num == 1:
                DNS1 = res
            elif num == 2:
                DNS2 = res
except:
    DNS1 = "unknown"
    DNS2 = "unknown"

def gateway_ip():
    try:
        Gateway = subprocess.Popen("ip route | grep default | awk '{print $3}'", shell=True, stdout=subprocess.PIPE)
        Gateway = Gateway.stdout.readline()
        Gateway = Gateway.decode("utf-8").split()[0]
    except:
        Gateway = "unknown"
    return Gateway

def wifi_password():
    try:
        SSID = wifi_name()
        if SSID == "unknown":
            password = "unknown"
        else:
            ShowProcess3 = subprocess.Popen(["nmcli", "-s", "-g", "802-11-wireless-security.psk", "connection", "show", SSID], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            password, erra = ShowProcess3.communicate()
            password = password.decode("utf-8").split()[0]
    except:
        password = "unknown"
    return password


def wifi_users():
    WhoList = [] 
    IPs = []
    MACs = []
    deviceNames = []

    MyIP = ip_all()
    MyMac = my_mac()
    name = manufacturer()
    product_name = product_nam()
    gateway = gateway_ip()+"/24"
    

    YourDeviceList = [MyIP, MyMac, f"{name} {product_name} (My device)"]
    start = 0
    time=10
    router_MAC=""
    while start <= time:
        start += 1

        eth = Ether(dst="ff:ff:ff:ff:ff:ff")
        arp = ARP(pdst=gateway)
        packet = eth/arp
        answ = srp(packet, timeout=0.5, verbose=False)[0]

        for res in answ:
            IP = res[1].psrc
            if IP not in IPs:
                IPs.append(IP)

            MAC = res[1].hwsrc
            if MAC not in MACs:
                MACs.append(MAC)
                try:
                    deviceName = urllib.request.urlopen(
                        f"http://api.macvendors.com/{MAC}")
                    deviceName = deviceName.read().decode("utf-8")
                    deviceNames.append(deviceName)
                except:
                    try:
                        deviceName = urllib.request.urlopen(
                            f"https://api.maclookup.app/v2/macs/{MAC}")
                        deviceName = deviceName.read().decode("utf-8")
                        deviceName = deviceName.split(",")
                        deviceName = deviceName[3]
                        deviceName = deviceName.replace(
                            'company":', "").replace('"', "")
                        if deviceName == "":
                            deviceName = "unknown"
                        deviceNames.append(deviceName)
                    except:
                        deviceName = "unknown"
                        deviceNames.append(deviceName)

    for i in range(0, len(IPs)):
        if IPs[i] == gateway_ip():
            router_MAC=MACs[i]
            WhoList.append([IPs[i],MACs[i],f"{deviceNames[i]} (router)"])
        else:
            WhoList.append([IPs[i],MACs[i],deviceNames[i]])

    WhoList.append(YourDeviceList)
    return WhoList,router_MAC

# print(DNS1)
# print(DNS2)
# print(Gateway)
# print(password)
w,r=wifi_users()
print(w)



