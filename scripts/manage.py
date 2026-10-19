#!/usr/bin/env python3
"""Manage this project's local server without installing a system service."""
import argparse
import json
import os
import signal
import subprocess
import sys
import time
import uuid
from pathlib import Path
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT/'.runtime'
URL = 'http://127.0.0.1:8765/'

def health():
    try:
        with urlopen(URL+'__health', timeout=1) as response:
            return json.load(response)
    except Exception:
        return None

def owned(info):
    try:
        state = json.loads((RUNTIME/'server.json').read_text())
        return info and info.get('app') == 'ai-weekly' and info.get('token') == state['token'] and info.get('pid') == state['pid']
    except (FileNotFoundError, ValueError, KeyError):
        return False

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['start','stop','status'])
    parser.add_argument('--open', action='store_true')
    args = parser.parse_args()
    info = health()
    if args.action == 'status':
        print('Running: '+URL if owned(info) else 'Stopped (or port is used by another service)')
        return
    if args.action == 'stop':
        if owned(info):
            os.kill(info['pid'], signal.SIGTERM)
            (RUNTIME/'server.json').unlink(missing_ok=True)
            print('AI Weekly server stopped.')
        else:
            print('No matching AI Weekly server to stop.')
        return
    if not (ROOT/'site/index.html').exists():
        subprocess.run([sys.executable,str(ROOT/'scripts/build.py')],check=True)
    if not owned(info):
        if info:
            raise SystemExit('Port 8765 belongs to another service. It was not changed.')
        RUNTIME.mkdir(exist_ok=True)
        token = uuid.uuid4().hex
        with (RUNTIME/'server.log').open('ab') as log:
            process = subprocess.Popen([sys.executable,str(ROOT/'scripts/serve.py'),'--token',token],cwd=ROOT,stdout=log,stderr=log,start_new_session=True)
        (RUNTIME/'server.json').write_text(json.dumps({'pid':process.pid,'token':token}))
        for _ in range(40):
            if owned(health()):
                break
            if process.poll() is not None:
                raise SystemExit('Server failed to start; see .runtime/server.log (port 8765 may be occupied).')
            time.sleep(.1)
        else:
            raise SystemExit('Server startup did not complete; see .runtime/server.log.')
    print(URL)
    if args.open:
        subprocess.run(['open','-a','Microsoft Edge',URL],check=True)

if __name__ == '__main__':
    main()
