import sys
import asyncio
import socket
from datetime import datetime

if len(sys.argv) != 2:
    print("Usage: hikimap [target]")
    sys.exit(1)

target = socket.gethostbyname(sys.argv[1])

print("hikimap 1.0 - (github.com/ryo-yamada/hikimap)")
print(f"Target - {target}")
print(f"Started - {datetime.now().strftime('%H:%M:%S')}")
print("-"*30)
print("PORT")

open_ports = []
sema = asyncio.Semaphore(1000)

async def scan_port(port):
    async with sema:
        try:
            r,w = await asyncio.wait_for(asyncio.open_connection(target, port), timeout=0.3)
            open_ports.append(port)
            print(port)
            w.close()
            await w.wait_closed()
        except:
            pass # closed port

async def main():
    tasks = []
    for port in range(1, 65536):
        tasks.append(scan_port(port))
    await asyncio.gather(*tasks)

asyncio.run(main())

print(f"\nDone: {len(open_ports)} open ports")