from colorama import Style, Fore
import subprocess
from asyncio.subprocess import DEVNULL

def success(msg):
    return f"{Fore.GREEN}{msg}{Style.RESET_ALL}"

def error(msg):
    return f"{Fore.RED}{msg}{Style.RESET_ALL}"

def valid_victim(victim):
    """Ping the given IP/Domain to see if the victim is reachable."""

    cmd = f"ping -c 1 {victim}".split(' ')
    res = subprocess.run(cmd, stdout=DEVNULL, stderr=DEVNULL)

    return not res.returncode

def send_data(soc, data):
    """Send data to victim. There's only one `\n` character instead of two. """

    if not soc:
        raise TypeError("Socket does not exist.")

    soc.send(f"{data}\r\n".encode('utf-8')) 