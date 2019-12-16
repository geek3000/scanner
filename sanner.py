import socket
import requests
import subprocess
import shlex
import json
from termcolor import colored
headers = {"Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImp0aSI6ImRjMjFjMzc0LTMwNWMtNDI4ZS1hZDJhLWQ4YTBhNzZlNjUyMyJ9.eyJpc3MiOiJtYWN2ZW5kb3JzIiwiYXVkIjoibWFjdmVuZG9ycyIsImp0aSI6ImRjMjFjMzc0LTMwNWMtNDI4ZS1hZDJhLWQ4YTBhNzZlNjUyMyIsImlhdCI6MTU3NjUxODg3OSwiZXhwIjoxODkxMDE0ODc5LCJzdWIiOiIzOTM1IiwidHlwIjoiYWNjZXNzIn0.HSlavFMUQ56dzfsnI4YdmRdWOIIY1T5UzieQgNTgu2sgQsBCA9EgwVY9QocKLAWmm1UHQPw6k3hX1Sa3FEAPSg"}

def get_mac(ip):
    cmd=shlex.split("getmac -4 "+ip)
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    mac=process.stdout.read().decode()
    return mac

def get_devices():
    found=False
    host_name = socket.gethostname() 
    host_ip = socket.gethostbyname(host_name)
    print(colored("You are ip adress is: ", "blue")+colored(host_ip, "yellow"))
    
    start_ip_list=host_ip.split('.')
    start_ip_list.pop(-1)
    start_ip=''
    for part in start_ip_list:
        start_ip+=part+'.'
    

    for end_ip in range(100, 255):
        
        try:
            ip=start_ip+str(end_ip)
            print('')
            print(colored("Checking IP: ", "blue")+colored(ip, "yellow"))
            hostname=socket.gethostbyaddr(ip)
            
            print("**********************************************")
            print('')
            print(colored("IP Adress: ", "blue")+colored(ip, "yellow"))
            found=True
            print(colored("Hostname: ", "blue")+colored(hostname[0], "yellow"))
            mac=get_mac(ip)
            print(colored("MAC Adress: ", "blue")+colored(mac, "yellow"))
            url="https://api.macvendors.com/v1/lookup/"+mac
            try:
                vendor=json.loads(requests.get(url, headers=headers).text)['data']['organization_name']
                print(colored("The vendor: ", "blue")+colored(vendor, "yellow"))
            except:
                print(colored("can't get vendor", "red"))
        except:
            pass
    print(colored("End of scan", "green"))
    if not found:
        print(colored("Sorry you are alone", "red"))

    
get_devices()
