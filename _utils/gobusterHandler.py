import subprocess
from _utils._utils import runProcess

# deprecated

wordlist = './_utils/common.txt'

def run(target, SERVICE):
    output = f'./tempOutput/gobuster_{target}'
    print(f"[*] Starting Gobuster on {SERVICE['port']}...")
    url = 'https://' if SERVICE['name'] == 'ssl/http' else 'http://'
    url += target + ':' + str(SERVICE['port'])
    command = [
        "gobuster",
        "dir",
        "-u", url,
        "-w", wordlist,
        "-o", output
        ]

    resultStr = 'NOTICE: '+ runProcess('gobuster', command)
    return [{(SERVICE['protocol'], SERVICE['port']): {'name':'Gobuster', 'output':resultStr}}]
