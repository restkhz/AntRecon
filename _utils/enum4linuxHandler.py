import subprocess
from _utils._utils import runProcess

def run(target, SERVICE):
    print(f"[*] Starting enum4linux...")
    command = [
        "enum4linux",
        "-a", target
        ]

    resultStr = runProcess('enum4linux', command)
    return [{(SERVICE['protocol'], SERVICE['port']): {'name':'enum4linux', 'output':resultStr}}]
