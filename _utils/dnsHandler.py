import subprocess
from _utils._utils import runProcess

def run(target, SERVICE):
    command = [
        'dig',
        'axfr',
        '@'+target
        ]
    notice = '''
**NOTICE: You should try to enumerate manually once you have DOMAIN name and check your NMAP report.**
We only have `dig axfr @<DNS_IP>` here.\n
'''
    resultStr = notice + runProcess('dns dig axfr', command)
    return [{(SERVICE['protocol'], SERVICE['port']): {'name':'DNS dig', 'output':resultStr}}] 
