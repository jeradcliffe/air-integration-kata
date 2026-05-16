#!/usr/bin/env python3
import json, os, subprocess, sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
HOOK = os.path.join(SCRIPT_DIR, 'protect-external.py')

passed = 0
failed = 0

def run_hook(label, tool_input, expect):
    global passed, failed
    result = subprocess.run(
        [sys.executable, HOOK],
        input=json.dumps({'tool_input': tool_input}),
        capture_output=True,
        text=True,
    )
    code = result.returncode
    if expect == 'pass' and code == 0:
        print(f"OK    PASS [{code}] {label}")
        passed += 1
    elif expect == 'block' and code != 0:
        print(f"OK    BLOCK [{code}] {label}")
        passed += 1
    else:
        output = (result.stdout + result.stderr).strip()
        print(f"FAIL  expected={expect} actual={code} {label} — {output}")
        failed += 1

EXT = "external"

run_hook("cat external/",       {"command": f"cat {EXT}/event-stream/server.js"},                    "pass")
run_hook("ls external/",        {"command": f"ls {EXT}/"},                                           "pass")
run_hook("grep external/",      {"command": f"grep sessionId {EXT}/users-and-sessions/server.js"},   "pass")
run_hook("find external/",      {"command": f"find {EXT}/ -name '*.js'"},                            "pass")
run_hook("wc external/",        {"command": f"wc -l {EXT}/event-stream/server.js"},                  "pass")
run_hook("echo redirect",       {"command": f"echo x > {EXT}/event-stream/server.js"},               "block")
run_hook("cp to external/",     {"command": f"cp src/foo.js {EXT}/routes/foo.js"},                   "block")
run_hook("sed -i external/",    {"command": f"sed -i 's/x/y/' {EXT}/users-and-sessions/server.js"},  "block")
run_hook("sed external/",       {"command": f"sed 's/x/y/' {EXT}/users-and-sessions/server.js"},     "block")
run_hook("rm external/",        {"command": f"rm {EXT}/event-stream/data/events.json"},              "block")
run_hook("mkdir external/",     {"command": f"mkdir {EXT}/new-dir"},                                 "block")
run_hook("node external/",      {"command": f"node {EXT}/event-stream/server.js"},                   "block")
run_hook("npm test",            {"command": "npm test"},                                              "pass")
run_hook("Edit external/ file", {"file_path": f"{EXT}/event-stream/server.js"},                      "block")
run_hook("Edit src/ file",      {"file_path": "src/index.js"},                                       "pass")

print(f"\nprotect-external.py: {passed} passed, {failed} failed")
sys.exit(0 if failed == 0 else 1)
