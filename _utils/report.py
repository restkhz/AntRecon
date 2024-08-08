from _utils._utils import removeColor

def firstRecon(target,SERVICES_DICT,results, DIR):
    
    MD = f'# AntRecon REPORT: {target}\n'
    MD += 'NOTICE: You should always take notes when you find something.\n'
    MD += '[TOC]\n'
    MD += 'Please use a MD editor that supports `TOC`\n'
    MD += '## Services:\n'

    for key in SERVICES_DICT:
        SERVICE = SERVICES_DICT[key]
        port = SERVICE['port']
        name = SERVICE['name']
        product = SERVICE['product']
        version = SERVICE['version']
        details = SERVICE['details']
        MD+= f'### {port}: {name}\n'
        MD+= f'Running with: {product}/{version}\n'
        for detail in details:
            name = detail['name']
            MD+= f'#### Detail: {name}\n'
            MD+= f"""
```
{removeColor(detail['output'])}
```\n
"""
    f=open(f'{DIR}/report_{target}.md', 'w')
    f.write(MD)
    f.close()
    print(f'[+] You should have HALF of REPORT now: <AntRecon>/report_{target}.md')

def nmapRecon(target, DIR):
    f=open(f'./tempOutput/nmap_{target}','r')
    nmapResult = f.read()
    f.close()
    MD = ''
    MD += '## NMAP:\n'
    MD += '**NOTICE: Valuable scan results such as `SNMP`,`FTP` and `SMTP` may be included here. Vulnerability scan results may not very accurate. Dont waste your time on vulns.**\n'
    MD += '[args:]-T4 -sS -sU -p U:53,161,1194,T:1-65535 -sV -O --script "(default or auth or vuln or discovery) and not (http-enum or TLS-*)" --script-args mincvss=5.0 --script-timeout 240s'
    MD += f"""
```
{nmapResult}
```\n
"""
    f=open(f'{DIR}/report_{target}.md', 'a')
    f.write(MD)
    f.close()
    print(f'[*] You should have FULL REPORT now: <AntRecon>/report_{target}.md')


if __name__ == '__main__':
    nmapRecon('192.168.184.13')
