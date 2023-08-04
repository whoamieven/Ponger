# non local imports ^_^
# if your reading this use auto-py-to-exe to convert this to an .exe file
from colorama import Fore, Back, Style
import asyncio
import time
import sys
import socket
import requests

x = 0
responses = []

async def get_isp_from_api(ip):
    url = f"http://ip-api.com/json/{ip}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data["isp"]
    else:
        print(f"Failed to fetch ISP information. Status code: {response.status_code}")
        return None
    pass


async def ping(host, port, x):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    timeout = 1
    try:
        client_socket.settimeout(timeout)

        await asyncio.sleep(1)

        start_time = time.time()
        client_socket.connect((host, port))
        end_time = time.time()

        response_time = (end_time - start_time) * 1000
        responses.insert(x,
                         f"time= {Fore.GREEN}{response_time:.2f}ms{Fore.RESET} - port={Fore.GREEN}{port}{Fore.RESET} ")
        return response_time

    except socket.timeout:
        responses.insert(x,
                         f"{Fore.RED}TIMED OUT{Fore.RESET} - port={Fore.RED}{port}{Fore.RESET} ")
        return None
    except socket.error as e:
        print(f"Error: {e}")
        return None
    finally:
        client_socket.close()


async def startup():

    global x
    host = sys.argv[1]
    ports = [int(c) for c in sys.argv[2].split(',')]
    ip = socket.gethostbyname(host)
    isp = await get_isp_from_api(ip)
    while True:
        for port in ports:
            x = x + 1
            asyncio.create_task(ping(host, port, x))
        all_tasks = asyncio.all_tasks()
        current_task = asyncio.current_task()
        all_tasks.remove(current_task)
        await asyncio.wait(all_tasks)
        print(f"Connected to {Fore.GREEN}{host}{Fore.RESET} ({Fore.MAGENTA}{isp}{Fore.RESET}) {''.join(responses)} ")
        responses.clear()
        x = 0

asyncio.run(startup())
