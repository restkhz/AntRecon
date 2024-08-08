import subprocess
from _utils._utils import runProcess

def run(target, SERVICE):
    print(f"[*] Starting whatweb on {SERVICE['port']}...")
    url = 'https://' if SERVICE['name'] == 'ssl/http' else 'http://'
    url += target + ':' + str(SERVICE['port'])
    
    command = ['whatweb','-a', '3', url]
    resultStr = runProcess('whatweb', command)
    return [{(SERVICE['protocol'], SERVICE['port']): {'name':'WhatWeb', 'output':resultStr}}]
