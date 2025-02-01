import subprocess

def ping_host(ip):
    try:
        response = subprocess.run(['ping', '-c', '1', '-w', '1', str(ip)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if response.returncode == 0:
            time_ms = response.stdout.decode().split("time=")[1].split()[0]
            return "UP", time_ms
        else:
            return "DOWN", "No response"
    except subprocess.TimeoutExpired:
        return "Error", "Connection timeout"


