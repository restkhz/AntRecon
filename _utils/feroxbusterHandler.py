import subprocess
from _utils._utils import runProcess

wordlist = './_utils/common.txt'

def run(target, SERVICE):
    output = f'./tempOutput/ferox_{target}'
    print(f"[*] Starting feroxbuster on {SERVICE['port']} with {wordlist}...It may take a while...")
    url = 'https://' if SERVICE['name'] == 'ssl/http' else 'http://'
    url += target + ':' + str(SERVICE['port'])
    command = [
        "feroxbuster",
        "-u", url,
        "-w", wordlist,
        "-d", '2',
        "-k",
        "-t", '30',
        "-q",
        "-E",
        "-x", 'pdf txt',
        "-C", '404'
        ]

    notice = '\nIf this was a web service, perhaps you might want to enumerate **subdomains or vhost**... If you have a domain name.'
    resultStr = runProcess('feroxbuster', command) + notice
    return [{(SERVICE['protocol'], SERVICE['port']): {'name':'feroxbuster', 'output':resultStr}}]
