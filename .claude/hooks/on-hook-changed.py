#!/usr/bin/env python3
import json, os, subprocess, sys

data = json.loads(sys.stdin.read())
file_path = data.get('tool_input', {}).get('file_path', '')

if file_path:
    normalized = os.path.normpath(os.path.abspath(file_path))
    if normalized.endswith(os.sep + 'protect-external.py'):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        subprocess.run([sys.executable, os.path.join(script_dir, 'test-protect-external.py')])

sys.exit(0)
