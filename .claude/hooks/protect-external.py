#!/usr/bin/env python3
import json, os, re, sys

data = json.loads(sys.stdin.read())
tool_input = data.get('tool_input', {})

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.normpath(os.path.join(SCRIPT_DIR, '..', '..'))
PROTECTED_DIR = os.path.join(PROJECT_ROOT, 'external')

file_path = tool_input.get('file_path', '')
if file_path:
    normalized = os.path.normpath(os.path.abspath(file_path))
    if normalized == PROTECTED_DIR or normalized.startswith(PROTECTED_DIR + os.sep):
        print("BLOCKED: The external/ directory is read-only. Files under external/event-stream/ and external/users-and-sessions/ must not be modified. These are fixed mock APIs used as integration targets for the kata exercise.")
        sys.exit(2)
    sys.exit(0)

command = tool_input.get('command', '')
if 'external/' not in command:
    sys.exit(0)

cmd = re.sub(r'^([A-Z_][A-Z0-9_]*=\S*\s+)+', '', command.lstrip())
leading = os.path.basename(re.split(r'[\s;|&]', cmd)[0]).lower()

READ_ONLY = {'cat', 'ls', 'grep', 'egrep', 'fgrep', 'rgrep', 'head', 'tail',
             'find', 'wc', 'file', 'stat', 'diff', 'less', 'more', 'sort', 'uniq'}

if leading not in READ_ONLY:
    print(f"BLOCKED: Bash command '{leading}' references external/ and is not on the read-only allowlist. The external/ directory must not be modified by shell commands.")
    sys.exit(2)

sys.exit(0)
