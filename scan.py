import subprocess
import ipaddress
import sys
import platform

def ping_host(ip):
    try:
        if platform.system().lower()== "windows":
            response = subprocess.run(['ping', '-n', '1', '-w', '1000', str(ip)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            response = subprocess.run(['ping', '-c', '1', '-W', '1', str(ip)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if response.returncode == 0:
            if "time=" in response.stdout.decode():
                time_ms = round(float(response.stdout.decode().split("time=")[1].split()[0]), 2)
                return "Up", time_ms
        
        if response.returncode != 0:
            return "Down", "No response"
    except Exception as e:
        return "Error", str(e)

def scan_network(cidr):

    up_count = 0
    down_count = 0
    error_count = 0

    try:
        network = ipaddress.IPv4Network(cidr, strict=False)
    except ValueError:
        print("Error: Invalid CIDR notation.")
        sys.exit(1)

    print(f"Scanning network {cidr}")

    for ip in network.hosts():
        status, message = ping_host(ip)

        if status == "Up":
            up_count += 1
            print(f"{ip} - Up ({message}ms)")
        elif status == "Down":
            down_count += 1
            print(f"{ip} - Down ({message})")
        else:
            error_count += 1
            print(f"{ip} - Error ({message})")

    return up_count, down_count, error_count

def main():
    if len(sys.argv) != 2:
        print("Usage: python scan.py <CIDR>")
        sys.exit(1)

    cidr = sys.argv[1]
    try:
        up_count, down_count, error_count = scan_network(cidr)
        print("Scan complete.")
        print(f"Found {up_count} active hosts, {down_count} down, and {error_count} errors")
    except ValueError:
        print("Error: Invalid CIDR notation.")

if __name__ == "__main__":
        main()