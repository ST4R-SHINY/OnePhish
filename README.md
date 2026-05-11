# ONE-PHISH TOOL BY ST4R-SHINY

> Cloudflare Tunnel, and profesional tool

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![Cloudflare](https://img.shields.io/badge/cloudflare-tunnel-orange)
![Status](https://img.shields.io/badge/status-beta-yellow)
![License](https://img.shields.io/badge/license-MIT-green)

---

# Overview

**ST4R-SHINY** is an educational Python utility that automates phishing exposure using **Cloudflare Tunnel** technology.

The project is designed for:

* phishing test
* Remote access 
* social engineer
* Secure tunnel experimentation
* phishing tool withouth templates
* Red-team environments

The tool automatically launches a phishing server and creates a temporary Cloudflare tunnel for phishing access.

---

# Features

* Automatic Cloudflare Tunnel deployment
* anonn tunnel
* iplogger
* phishing profesional
* without templates
* all login for phishing
* write url login / inject / phishing link
* Fast phishing tool

---

# Requirements

## Python Modules

```python id="f9u1op"
import os
import sys
import time
import threading
import subprocess
import re
import json
import urllib3
from http.server import HTTPServer, SimpleHTTPRequestHandler
```

---

# Installation

Clone repository:

```bash id="u2x91m"
git clone https://github.com/username/ST4R-SHINY.git
cd ST4R-SHINY
```

Install dependencies:

```bash id="c91slx"
pip install urllib3
```

---

# Cloudflare Tunnel Requirement

Download Cloudflare Tunnel binary:

Linux:

```bash id="4kq0aa"
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64
chmod +x cloudflared-linux-amd64
mv cloudflared-linux-amd64 cloudflared
```

Windows:

```bash id="88x2rq"
Download:
https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/
```

---

# Usage

Start ST4R-SHINY:

```bash id="g6md1s"
python main.py
```

Example execution flow:

```bash id="j3l0pk"
[+] Starting local HTTP server...
[+] Launching Cloudflare Tunnel...
[+] PHISHING URL:
https://random-subdomain.trycloudflare.com
```
---

# Educational Disclaimer

This project is intended strictly for:

* Laboratories
* Authorized testing
* Educational phishing practice
* this disclaimer its joke LOL :)

Users are responsible for complying with all applicable laws and authorization requirements.

# Author

Tool phishing pro By ST4R-SHINY
Phishing tool
