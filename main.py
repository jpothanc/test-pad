import socket
import subprocess
import platform
import requests
import time

# Configuration
DOMAIN = "google.com"  # Replace with your LB domain
PORT = 80  # Change to 443 for HTTPS
TEST_URL = f"http://{DOMAIN}"  # Change to "https://" if needed


# Resolve all backend IPs for the domain
def get_backend_ips(domain):
    try:
        return list(set(socket.gethostbyname_ex(domain)[2]))
    except socket.gaierror:
        print(f"❌ Failed to resolve {domain}")
        return []

# Function to ping an IP address
def ping(ip):
    param = "-n" if platform.system().lower() == "windows" else "-c"
    try:
        result = subprocess.run(["ping", param, "1", ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.returncode == 0
    except Exception as e:
        print(f"⚠️ Error pinging {ip}: {e}")
        return False

# Function to test connection through LB
def test_backend_ips1(backend_ips):
    seen_ips = set()

    while len(seen_ips) < len(backend_ips):
        try:
            response = requests.get(TEST_URL, timeout=5)
            response_ip = socket.gethostbyname(DOMAIN)

            if response_ip in backend_ips:
                seen_ips.add(response_ip)
                print(f"✅ Backend {response_ip} responded!")

        except requests.RequestException:
            print("⚠️ Connection failed.")

        time.sleep(1)  # Prevent hammering the LB too fast

    print("🎉 Successfully tested all backend IPs!")



# Function to test all backend IPs
def test_backend_ips(backend_ips):
    seen_ips = set()

    while len(seen_ips) < len(backend_ips):
        for ip in backend_ips:
            if ip not in seen_ips and ping(ip):
                seen_ips.add(ip)
                print(f"✅ Backend {ip} is reachable!")

        time.sleep(1)  # Prevent excessive pinging

    print("🎉 Successfully pinged all backend IPs!")
# Run the script
backend_ips = get_backend_ips(DOMAIN)

if backend_ips:
    print(f"Found backend IPs: {backend_ips}")
    test_backend_ips(backend_ips)
else:
    print("No backend IPs found.")
