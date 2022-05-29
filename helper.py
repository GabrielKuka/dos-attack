from colorama import Style, Fore
import subprocess
from asyncio.subprocess import DEVNULL

def success(msg):
    return f"{Fore.GREEN}{msg}{Style.RESET_ALL}"

def error(msg):
    return f"{Fore.RED}{msg}{Style.RESET_ALL}"

def valid_victim(victim):
    cmd = f"ping -c 1 {victim}".split(' ')
    res = subprocess.run(cmd, stdout=DEVNULL, stderr=DEVNULL)

    return not res.returncode

def send_data(soc, data):
    soc.send(f"{data}\r\n".encode('utf-8')) 