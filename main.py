import sys
import asyncio
import socket
from datetime import datetime

serviceGuesses = {}
try:
    with open("/etc/services", "r") as f:
        for line in f:
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            service, port_protocol = line.split()
            port, protocol = port_protocol.split("/")

            if protocol == "tcp":
                serviceGuesses[int(port)] = service
except FileNotFoundError:
    print("* Warning - /etc/services not found")

if len(sys.argv) != 2:
    print("Usage: hikimap [target]")
    sys.exit(1)

target = socket.gethostbyname(sys.argv[1])

print("hikimap 1.1 - (github.com/ryo-yamada/hikimap)")
print("* Service guesses are TCP only")
print(f"Target - {target}")
print(f"Started - {datetime.now().strftime('%H:%M:%S')}")
print("-"*30)
print("PORT   SERVICE")

open_ports = []
sema = asyncio.Semaphore(1000)

async def scan_port(port):
    async with sema:
        try:
            r,w = await asyncio.wait_for(asyncio.open_connection(target, port), timeout=0.3)
            open_ports.append(port)
            serviceGuess = serviceGuesses.get(port, "unknown")
            print(f"{port:<6} {serviceGuess}")
            w.close()
            await w.wait_closed()
        except:
            pass # closed port

async def main():
    await asyncio.gather(*(scan_port(port) for port in range(1, 65536)))

asyncio.run(main())

print(f"\nDone: {len(open_ports)} open ports")
