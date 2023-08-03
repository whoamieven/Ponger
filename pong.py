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

def get_asn_from_api(asn):
    url = f"http://ip-api.com/json/{ip}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data["as"]
    else:
        print(f"Failed to fetch ASN. Status code: {response.status_code}")
        return None

def print_help():
    print("Usage: pong.exe host port")
    print("Optional:")
    print("  -as         Shows ASN Informations (22 REQ Limit per IP)")
    print("  -h, --help  Show this help message and exit.")
    sys.exit(0)

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
    if len(sys.argv) == 2 and (sys.argv[1] == "-h" or sys.argv[1] == "--help"):
        print_help()

    if "-as" in sys.argv:
        show_asn = True
        sys.argv.remove("-as")
    else:
        show_asn = False

    if len(sys.argv) != 3:
        print("Error: Invalid number of arguments.")
        print_help()

    host = sys.argv[1]
    port = int(sys.argv[2])

    while True:
        response_time = measure_tcp_response_time(host, port, TIMEOUT)

        ip = socket.gethostbyname(host)
        isp = get_isp_from_api(ip)
        asn = get_asn_from_api(ip)

        if response_time is not None:
            if show_asn:
                print(f"Connected to {Fore.GREEN}{host}{Fore.RESET} ({Fore.MAGENTA}{asn}{Fore.RESET}) - time= {Fore.GREEN}{response_time:.2f}ms{Fore.RESET} - port={Fore.GREEN}{port}{Fore.RESET} - protocol={Fore.GREEN}TCP{Fore.RESET}")
            else:
                print(f"Connected to {Fore.GREEN}{host}{Fore.RESET} ({Fore.MAGENTA}{isp}{Fore.RESET}) - time= {Fore.GREEN}{response_time:.2f}ms{Fore.RESET} - port={Fore.GREEN}{port}{Fore.RESET} - protocol={Fore.GREEN}TCP{Fore.RESET}")
        else:
            print(f"{Fore.LIGHTRED_EX}Connection timed out{Fore.RESET}")
