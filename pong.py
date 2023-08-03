# non local imports ^_^
# if your reading this use auto-py-to-exe to convert this to an .exe file
import socket
import time
import sys
import requests
from colorama import Fore, Back, Style

TIMEOUT = 3

def get_isp_from_api(ip):
    url = f"http://ip-api.com/json/{ip}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data["isp"]
    else:
        print(f"Failed to fetch ISP information. Status code: {response.status_code}")
        return None
    pass

def measure_tcp_response_time(host, port, timeout):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.settimeout(timeout)

        time.sleep(1)

        start_time = time.time()
        client_socket.connect((host, port))
        end_time = time.time()

        response_time = (end_time - start_time) * 1000
        return response_time

    except socket.timeout:
        return None
    except socket.error as e:
        print(f"Error: {e}")
        return None
    finally:
        client_socket.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: pong.exe host port")
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])

    while True:
        response_time = measure_tcp_response_time(host, port, TIMEOUT)

        ip = socket.gethostbyname(host)
        isp = get_isp_from_api(ip)

        if response_time is not None:
            print(f"Connected to {Fore.GREEN}{host}{Fore.RESET} ({Fore.MAGENTA}{isp}{Fore.RESET}) - time= {Fore.GREEN}{response_time:.2f}ms{Fore.RESET} - port={Fore.GREEN}{port}{Fore.RESET} - protocol={Fore.GREEN}TCP{Fore.RESET}")
        else:
            print(f"{Fore.LIGHTRED_EX}Connection timed out{Fore.RESET}")