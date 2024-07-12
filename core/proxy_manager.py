import os
import random
import string
from rich.console import Console
from core.config_loader import load_config

console = Console()

config = load_config()
IPROYAL_LOG = config['settings']['iproyal_log']
IPROYAL_PASS = config['settings']['iproyal_pass']
IPROYAL_COUNTRY = config['settings']['iproyal_country']

def load_proxies(file_path='./data/proxy.txt'):
    if not os.path.exists(file_path):
        console.print(f"[red]File {file_path} not found.[/red]")
        raise FileNotFoundError(f"File {file_path} not found.")
    
    proxies = []
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                proxies.append(line)
    
    console.print(f"[green]Loaded {len(proxies)} proxies from {file_path}.[/green]")
    return proxies

def get_proxy(proxies):
    if not proxies:
        console.print("[red]No proxies available.[/red]")
        return None
    return proxies.pop(0)

def randstr(length):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for _ in range(length))

def gen_session_proxy():
    radncifri = randstr(8)
    final_proxies = f"{IPROYAL_LOG}:{IPROYAL_PASS}_country-{IPROYAL_COUNTRY}_session-{radncifri}_lifetime-24h@167.235.26.46:12321"
    return final_proxies
