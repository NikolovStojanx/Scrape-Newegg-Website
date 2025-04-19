import json
import os

def extract_data_proxy(proxy):
    host, port, username, password = proxy.strip().split(':')
    return {
        'smartproxy': host,
        'port': port,
        'username': username,
        'password': password
    }

project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(f"Project path: {project_path}")

proxies_file_path = os.path.join(project_path, 'data', 'proxies.txt')
print(f"Proxies file path: {proxies_file_path}")

try:
    with open(proxies_file_path, 'r') as f:
        proxies = [extract_data_proxy(p) for p in f if p.strip()]

    output_file_path = os.path.join(project_path, 'data', 'data.json')
    with open(output_file_path, "w") as file:
        json.dump(proxies, file, indent=4)

    print(f"Proxies successfully saved to: {output_file_path}")

except FileNotFoundError:
    print(f"Error: The file '{proxies_file_path}' was not found.")
except Exception as e:
    print(f"An error occurred: {e}")